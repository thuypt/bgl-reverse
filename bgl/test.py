import bgl
import gls

d=bgl.BGL("D:\\bgl-reverse\\local\\ChsEn.BGL")
f=open("out.txt","w",encoding="utf-8")
while d.moveForward():
    if d.current[0]==1:
        term=d.parseAsTerm()
        f.writelines([term.title,'\n',str(term.property),'\n',term.definition,'\n'])

