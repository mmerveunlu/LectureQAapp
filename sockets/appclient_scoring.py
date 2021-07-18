""" This file contains functions to be used for sentence comparison """
#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

from libclient_scoring import Message

sel = selectors.DefaultSelector()


def create_request(sentence1, sentence2,action="search"):
    """ 
    creates the request from the client,      
    @action: string, the action name ex: search 
    @sentence1: string, the first sentence to be scored
    @sentence2: string, the second sentence to be scored
    """
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action,sentence1=sentence1,sentence2=sentence2),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + sentences1 + sentences1, encoding="utf-8"),
        )


def start_connection(host, port, request):
    """ 
    starts the connection from the client 
    to the given host on the port

    @host:IP,local etc, indicates the server adress
    @port: int, which port to connect
    @request: 
    """ 
    addr = (host, port)
    print("starting connection to", addr)
    # socket.socket creates a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    # connect_ex returns an error indicator 
    sock.connect_ex(addr)
    # The scoket is initially set to both read/write events
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


def run_client(host,port,sentence1,sentence2):
    """runs the client app with a given passage and question""" 
    response = None
    
    request = create_request(sentence1, sentence2)
    start_connection(host, port, request)
    try:
        while True:
            events = sel.select(timeout=10)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                    if message.response and message.response.get('result') is not None:
                        print("Run ", message.response.get('result'))
                        response = message.response.get('result')
                except Exception:
                    print("main: error: exception for: ", "{message.addr}:\n{traceback.format_exc()}")
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        #sel.close()
        print("Not closing")
    return response


# Example run
#sentence1 = 'Sentences are passed as a list of string.'
#sentence2 = 'The quick brown fox jumps over the lazy dog'
#run_client('10.2.1.55',12345,sentence1,sentence2)
