

def parseInt(data):
    """parse a big-endian integer"""
    value=0;
    for byte in data:
        value=value<<8
        value=value+byte
    return value


def replaceCharsetTag(data,encoding='ascii'):
    """decode the data (bytes) and replace <charset c=T>****;</charset> with the char value"""
    loc=data.find(b'<charset c=')
    if loc==-1:
        return data.decode(encoding)
    else:
        return data[0:loc].decode(encoding)\
            +(b'\\u'+data[loc+13:loc+17]).decode('unicode_escape')\
            +replaceCharsetTag(data[loc+28:],encoding)

def replaceHTMLEntity(data):
    """replace &#***; to char, use with caution"""
    while True:
        loc=data.find(b'&#')
        if loc==-1:
            break
        end=data.find(b';',loc)
        data=data[0:loc]+bytes([int(data[loc+2:end])])+data[end+1:]
    return data
