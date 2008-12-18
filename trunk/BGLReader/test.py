import bgl
d=bgl.BGL("D:\\bgl-reverse\\local\\enchs.BGL")
while d.moveForward():
    if d.current[0]==1:
        term=d.parseAsTerm()
        print([term.title,term.property,term.tail])
