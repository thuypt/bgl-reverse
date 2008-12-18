import BGR
d=BGR.BGR("D:\\eb.bgr")
while d.readnparse()==None:
    pass
while not d.eof:
    print(d.read())