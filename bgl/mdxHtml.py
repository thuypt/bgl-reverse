import bgl
import gls
import os
from util import *

USE_LEXCIAL_CLASS=False

filenames=["lcfa","lcef","hwed","hwde"]
basepath="D:/bgl-reverse/local"

parser=gls.GlsContentParser()

errors=[]

def handlebritannicainvalid(data):
    return data.replace(" 'REPLACE' "," ").replace(" / "," ")

def htmlparserbackend(d,g):
    term=d.parseAsTerm()
    
    title=term.title.split('$')[0]
    if len(title)==0: # title length is 0, ignore it
        errors.append(term)
        return term.title
    
    parser.reset()
    
    parser.parts.append('<b>')            
    display=term.property.get(0x08,title)
    parser.feed(display)
    parser.parts.append('</b>')
    
    phonetic=term.property.get(0x1b)
    if phonetic!=None:
        parser.parts.append(" [")
        parser.feed(phonetic)
        parser.parts.append(']')
    parser.parts.append('<br/>\n')
    if USE_LEXCIAL_CLASS:
        lex=gls.LEXICAL_CLASS.get(term.property.get(0x02))
        if lex!=None:
            parser.parts.append(lex+' ')
    parts=parser.parts
    parser.reset()
    try:
        parser.feed(term.definition)
    except:
        parser.reset()
        try:
            #parser.feed(handlebritannicainvalid(term.definition))
            raise Exception()
        except:
            errors.append(term)
            return term.title
    
    g.put(term.title,parts+parser.parts)
    return term.title

def simplebackend(d,g):
    term=d.parseAsTerm()
    title=term.title.split('$')[0]
    if len(title)==0: # title length is 0, ignore it
        errors.append(term)
        return term.title
    parts=['<b>']+replaceCharsetTag(term.property.get(0x08,title))+['</b>']
    phonetic=term.property.get(0x1b)
    if phonetic!=None:
        parts.append(" [")
        parts+=replaceCharsetTag(phonetic)
        parts.append(']<br/>\n')
    lex=gls.LEXICAL_CLASS.get(term.property.get(0x02))
    if lex!=None:
        parts.append(lex)
    g.put(term.title,parts+replaceCharsetTag(term.definition))
    return term.title

for fn in filenames:
    resdir=basepath+"/"+fn
    inpath=resdir+".bgl"
    outpath=resdir+".txt"
    status=open(resdir+".status",'w',encoding='utf-8')
    errors=[]
    
    d=bgl.BGL(inpath)
    try:
        os.mkdir(resdir)
    except:
        pass
    gloss=gls.Glossary()
    
    while d.moveForward():
        if d.current[0]==1:
            status.writelines([
                htmlparserbackend(d,gloss)
                #simplebackend(d,gloss)
                ,'\n'])
        elif d.current[0]==2:
            resdata=d.parseAsResource()
            res=open(resdir+"/"+resdata.name,'wb')
            res.write(resdata.data)
            res.close()
    status.close()
    
    f=open(outpath,"w",encoding="utf-8")
    for k in gloss:
        f.write(k)
        f.write('\n')
        ent=gloss[k]
        for num in sorted(ent.keys()):
            f.writelines(ent[num])
            f.write('<hr/>\n')
        f.write('</>\n')
    f.close()

    if len(errors)>0:
        f=open(resdir+".log","w",encoding="utf-8")
        for term in errors:
            f.write(term.title)
            f.write('\n')
            f.write(term.definition)
            phone=term.property.get(0x1b)
            if phone!=None:
                f.write('\n')
                f.write(phone)
            display=term.property.get(0x08)
            if display!=None:
                f.write('\n')
                f.write(display)
            f.write('\n\n')
        f.close()

    f=open(resdir+".ifo","w",encoding="utf-8")
    prop=d.property
    f.writelines(["Title: ",prop.get(0x01,''),'\n'])
    f.writelines(["Author Name: ",prop.get(0x02,''),'\n'])
    f.writelines(["Author Email: ",prop.get(0x03,''),'\n'])
    f.writelines(["Description: ",prop.get(0x09,''),'\n'])
    f.close()
