#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

from .libclient import Message

sel = selectors.DefaultSelector()


def create_request(action, passage, question):
    """ 
    creates the request from the client,      
    @action: string, the action name ex: search 
    @passage: string, the passage to be searched 
    @question: string, the question to be answered
    """
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, passage=passage, question=question),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + passage + question, encoding="utf-8"),
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


def run_client(host,port,passage,question):
    """runs the client app with a given passage and question""" 
    # get the parameters from command line
    response = None
    action = "search"
    request = create_request(action, passage, question)
    start_connection(host, port, request)
    try:
        while True:
            events = sel.select(timeout=10)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                    if message.response and message.response.get('result') is not None:
                        # print("Run ", message.response.get('result'))
                        response = message.response.get('result')
                except Exception:
                    # print("main: error: exception for: ", "{message.addr}:\n{traceback.format_exc()}")
                    print("main: error: exception: Server is Busy!")
                    response = "Please wait, the server is busy!"
                    # message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        #sel.close()
        print("Not closing")
    return response

