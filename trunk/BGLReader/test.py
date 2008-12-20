import bgl
import gls
d=bgl.BGL("D:\\bgl-reverse\\local\\chsen.BGL")
f=open("coed.txt","w",encoding="utf-8")
while d.moveForward():
    if d.current[0]==1:
        term=d.parseAsTerm()
        f.writelines(str([term.title,'\n',str(term.property)]))

f.close()
