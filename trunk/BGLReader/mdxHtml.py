import bgl
import gls
for fn in ["chsen.bgl"]:
    d=bgl.BGL("D:\\bgl-reverse\\local\\"+fn)
    f=open(fn+".txt","w",encoding="utf-8")
    while d.moveForward():
        if d.current[0]==1:
            try:
                term=d.parseAsTerm()
            except Exception:
                print(d.current)
            title=term.title.split('$',1)[0]
            if len(title)==0:
                continue
            display=term.property.get(0x08,term.title.split('$')[0])
            f.writelines([title,'\n'])
            f.write('<b>'+display+'</b><br/>')
            phonetic=term.property.get(0x1b,'')
            if len(phonetic)>0:
                f.write('&#47;'+phonetic+'&#47;<br/>')
            f.write(gls.LEXICAL_CLASS.get(term.property.get(0x02),''))
            f.write('<br/>')
            f.write(term.definition)
            f.write('<br/>\n</>\n')
    f.close()
