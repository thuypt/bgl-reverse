"""some reusable functions"""
import re

def unpack_ui(data) -> int:
    """bytes to big-endian unsigned int"""
    value=0;
    for byte in data:
        value=value<<8
        value=value+byte
    return value

def read_ui(file,length:int) -> int:
    data=file.read(length)
    if len(data)!=length:
        return None
    return unpack_ui(data)

def decode(data:bytes,charset:str,fallback:str='latin1') -> str:
    """decode data to string with charset, and try fallback when errors occur"""
    ret=''
    while len(data)>0:
        try:
            ret+=data.decode(charset)
            break
        except UnicodeDecodeError as e:
            ret+=data[e.start:e.end].decode(fallback)
            data=data[e.end:]
    return ret

def mem_split(data:memoryview,delimiter:int)->(memoryview,memoryview):
    i=0
    data_len=len(data)
    while i<data_len:
        if data[i][0]==delimiter:
            break
        i=i+1
    return (data[0:i],data[i+1:])
