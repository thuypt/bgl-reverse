# Introduction #


# Details #

## RecordBlock ##

RecordBlock consists of a leading big-endian unsigned integer N and following N bytes of data and is used in construction of a Record

RecordBlock(x) indicates a Block structure with the length value N consisting of x bytes.

So following code can parse a RecordBlock structure:

```
# python 3.0 compatible
def parseRecordBlock(data,x):
   """return a tuple (blockdata,tail)"""
  length=parseInt(data[0:x])
  return (data[x:x+length],data[x+length:])
```
## PropertyBlock ##