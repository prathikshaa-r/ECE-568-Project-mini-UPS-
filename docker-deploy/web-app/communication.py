import socket
import pdb
import io
import math
import time

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

#from amazon_ups_interface import *
#from ups_world_interface import *
#from amazon_mock_interface import *



def recvMod2(sock):
    var_int_buff = []
    pdb.set_trace()
    while True:
        buf = sock.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = sock.recv(msg_len)
    return whole_message

#https://groups.google.com/forum/#!topic/protobuf/4RydUI1HkSM
def recvMod(socket):
    # int length is at most 4 bytes long
    hdr_bytes = socket.recv(4)
    (msg_length, hdr_length) = _DecodeVarint32(hdr_bytes, 0)
    rsp_buffer = io.BytesIO()
    if hdr_length < 4:
        rsp_buffer.write(hdr_bytes[hdr_length:])
        # read the remaining message bytes
        msg_length = msg_length - (4 - hdr_length)
    while msg_length > 0:
        rsp_bytes = socket.recv(min(8096, msg_length))
        rsp_buffer.write(rsp_bytes)
        msg_length = msg_length - len(rsp_bytes)
    return rsp_buffer.getvalue()

            
def sendallMod(mess,sock):
    _EncodeVarint(sock.send, len(mess), None)
    sock.sendall(mess)
    return


def sendCommand(command, sock):
    mess = command.SerializeToString()
    sendallMod(mess,sock)
    
