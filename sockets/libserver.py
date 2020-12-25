import sys
import selectors
import json
import io
import struct
from datetime import datetime
from utils import run_model, load_model, run_loaded_model
from appmodel import MyArguments, MODEL_CLASSES

def request_search(passage,question,pretrained):
    """runs the model for given passage and question
    Args: 
     @passage: string,the title of the lecture
     @question: string, the question
    Returns:
     @answer: string, the predicted answer
    """
    # answer = run_model(passage,question)
    answer = run_loaded_model(passage, question,pretrained)

    return answer

class PreTrainedModel:
    def __init__(self,model_path):
        # pre-trained model parameters
        args_dict = { "data_dir":"",
                  "data":"",
                  "model_name_or_path":model_path,
                  "max_seq_length":256,
                  "predict_file":"",
                  "version_2_with_negative":False,
                  "max_query_length":64,
                  "threads":1,
                  "doc_stride":128,
                  "local_rank":-1,
                  "n_gpu":1,
                  "per_gpu_eval_batch_size":8,
                  "eval_batch_size":8,
                  "output_dir":"",
                  "model_type":"bert",
                  "do_lower_case":False,
                  "device":"cpu",
                  "n_best_size":2,
                  "max_answer_length":96
        }
        self.args = MyArguments(args_dict)
        args.model_type = args.model_type.lower()
        config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]
        config = config_class.from_pretrained(args.model_name_or_path)
    
        self.tokenizer = tokenizer_class.from_pretrained(args.model_name_or_path,
                                                 do_lower_case=args.do_lower_case)
        self.model = model_class.from_pretrained(args.model_name_or_path,
                                                 from_tf=bool(".ckpt" in args.model_name_or_path),
                                                 config=config)
        

class Message:
    def __init__(self, selector, sock, addr, pretrained):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False
        self.pretrained = pretrained

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        """ reads the data from the socket 
        and stores it in a receive buffer 
        """
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        """if there is a data in send buffer, calls send """
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _create_response_json_content(self):
        action = self.request.get("action")
        if action == "search":
            passage = self.request.get("passage")
            question = self.request.get("question")
            answer = request_search(passage, question, pretrained)
            content = {"result": answer}
        else:
            content = {"result": f'Error: invalid action "{action}".'}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def process_events(self, mask):
        """ calls read/write depending on the mask
        @mask: an event mask of operations 
        """ 
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        """ 
         reads the message
        """
        # reads the data from socket and stores it
        # in a receive buffer
        self._read()
        # There are three components of the header
        # so there are three checks
        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        """ 
        writes the message 
        """
        # first checks for the request
        if self.request:
            if not self.response_created:
                # if one exists and the response is not created
                self.create_response()

        self._write()

    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                "error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                "error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_protoheader(self):
        """the fixed-length header is processed
        The fixed length header is 2-byte integer, contains 
            the length of the json header.   
        """
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            # unpack the length, reads the value, decode it and stores it.
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        """ processes the json header """
        # jsonheader_len is read by process_protoheader()
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            # decode and deserialize JSON header into a dictionary
            # since Json header is defined as Unicode with UTF-8,
            # it is hardcoded in the function
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    def process_request(self):
        """reads the content of the message """
        # when content-length bytes are available
        # in the bufferm the request can be processed 
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            # if the content type is Json, it decodes and deserializes it 
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print("received request", repr(self.request), "from", self.addr)
        else:
            # if the content type is not Json, it assumes as binary,
            # simply prints it
            # Binary or unknown content-type
            self.request = data
            print(
                f'received {self.jsonheader["content-type"]} request from',
                self.addr,
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self):
        """ creates response, writes the response to the send buffer """
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message
