"""some reusable functions"""
import re

def parseInt(data):
    """parse as a big-endian integer"""
    value=0;
    for byte in data:
        value=value<<8
        value=value+byte
    return value

def decode(data,charset,default='latin1'):
    """decode data to string with charset, and try default when errors occur"""
    ret=''
    while len(data)>0:
        try:
            ret+=data.decode(charset)
            break
        except UnicodeDecodeError as e:
            ret+=data[e.start:e.end].decode(default)
            data=data[e.end:]
    return ret

PAT_CHARSET_TAG=re.compile("\\<charset[^\\>]*\\>(?P<value>[0-9A-Fa-f]{4});\\<\\/charset\\>",re.IGNORECASE)

def replaceCharsetTag(oldstr):
    """replace <charset c=...>****;</charset> with an indicated char"""
    ret=[]
    if len(oldstr)==0:
        return ""
    itr=PAT_CHARSET_TAG.finditer(oldstr)
    lastpos=0
    for m in itr:
        ret.append(oldstr[lastpos:m.start()])
        ret.append(chr(int(m.group('value'),16)))
        lastpos=m.end()
    ret.append(oldstr[lastpos:])
    return ret
