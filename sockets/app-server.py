#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    """ 
    gets the new socket object and 
    registers it with the selector

    @sock:
    """
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    # put the socket non-blocking mode
    conn.setblocking(False)
    # after a message is created, it's associated with a socket
    message = libserver.Message(sel, conn, addr)
    # sel.register is initially set to be monitored for read events
    # Once the request has been read, it will listen for write events
    sel.register(conn, selectors.EVENT_READ, data=message)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
# socket.socket creates a socket object
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# next lines enables to server listen on the specific port
# and accepts the connections
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
# to configure the socket in non-blocking mode
lsock.setblocking(False)
# registers the socket to be monitored with sel.select()
# for listening sockets we want read events: EVENT_READ
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        # waits for the events
        # sel.select() blocks until there are sockets
        # ready for I/O
        events = sel.select(timeout=None)
        # events is a list of tuples (key,event) for each socket
        #  .key: SelectorKey, contains a  fileobj attribute
        #  .mask: is an event mask of the operations
        for key, mask in events:
            if key.data is None:
                # if key.data is None, it is from listening socket
                # accept it
                accept_wrapper(key.fileobj)
            else:
                # if key.data is not None,
                # it's a client socket, already accepted
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
