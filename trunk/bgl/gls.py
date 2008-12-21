"""format specification for BGL file"""
from html.parser import HTMLParser

# glossary parameter, may contain format identification information, at the beginning of a BGR
RC_GLSPARAM=0
# glossary property
RC_GLSPROP=3
# term
RC_GLSTERM1=0x1
RC_GLSTERMA=0xA
RC_GLSTERMB=0xB
# resource
RC_GLSRES=2

LEXICAL_CLASS = {
    0x30:'n.',
    0x31:'adj.',
    0x32:'v.',
    0x33:'adv.',
    0x34:'interj.',
    0x35:"pron.",
    0x36:"prep.",
    0x37:"conj.",
    0x38:"suff.",
    0x39:"pref.",
    0x3A:"art." 
    }

DERIVATION = (
    'V-0',# Verb
    'V-0.0',# Verb
    'V-0.1',# Infinivtive
    'V-0.1.1',# ?
    'V-1.0',
    'V-1.1',
    'V-1.1.1', # Present Simple
    'V-1.1.2', #Present Simple (3rd pers. sing.)
    'V-2.0',#
    'V-2.1',#
    'V-2.1.1',# Past Simple
    'V-3.0',#
    'V-3.1',#
    'V-3.1.1',# Present Participle
    'V-4.0',#
    'V-4.1',#
    'V-4.1.1',#Past Participle
    'V-5.0',#
    'V-5.1',#
    'V-5.1.1',#Future
    'V2-0',#
    'V2-0.0',#
    'V2-0.1',#Infinitive
    'V2-0.1.1',#
    'V2-1.0',#
    'V2-1.1',#
    'V2-1.1.1',#Present Simple (1st pers. sing.)
    'V2-1.1.2',#Present Simple (2nd pers. sing. & plural forms)
    'V2-1.1.3',#Present Simple (3rd pers. sing.)
    'V2-2.0',#
    'V2-2.1',#
    'V2-2.1.1',#Past Simple (1st & 3rd pers. sing.)
    'V2-2.1.2',#Past Simple (2nd pers. sing. & plural forms)
    'V2-3.0',#
    'V2-3.1',#
    'V2-3.1.1',#Present Participle
    'V2-4.0',#
    'V2-4.1',#
    'V2-4.1.1',#Past Participle
    'V2-5.0',#
    'V2-5.1',#
    'V2-5.1.1',#Future
    'N-0',#Noun
    'N-1.0',#
    'N-1.1',#
    'N-1.1.1',#Singular
    'N-2.0',#
    'N-2.1',#
    'N-2.1.1',#Plural
    'N4-1.0',#
    'N4-1.1',#
    'N4-1.1.1',#Singular Masc.
    'N4-1.1.2',#Singular Fem.
    'N4-2.0',#
    'N4-2.1',#
    'N4-2.1.1',#Plural Masc.
    'N4-2.1.2',#Plural Fem.
    'ADJ-0',#Adjective
    'ADJ-1.0',#
    'ADJ-1.1',#
    'ADJ-1.1.1',#Adjective
    'ADJ-1.1.2',#Comparative
    'ADJ-1.1.3',#Superlative
    )

LANGUAGE = (
    "English", 
    "French",
    "Italian",
    "Spanish",
    "Dutch",
    "Portuguese",
    "German",
    "Russian",
    "Japanese",
    "Traditional Chinese",
    "Simplified Chinese",
    "Greek",
    "Korean",
    "Turkish",
    "Hebrew",
    "Arabic",
    "Thai",
    "Other",
    "Other Simplified Chinese dialects",
    "Other Traditional Chinese dialects",
    "Other Eastern-European languages",
    "Other Western-European languages",
    "Other Russian languages",
    "Other Japanese languages",
    "Other Baltic languages",
    "Other Greek languages",
    "Other Korean dialects",
    "Other Turkish dialects",
    "Other Thai dialects",
    "Polish",
    "Hungarian",
    "Czech",
    "Lithuanian",
    "Latvian",
    "Catalan",
    "Croatian",
    "Serbian",
    "Slovak",
    "Albanian",
    "Urdu",
    "Slovenian",
    "Estonian",
    "Bulgarian",
    "Danish",
    "Finnish",
    "Icelandic",
    "Norwegian",
    "Romanian",
    "Swedish",
    "Ukrainian",
    "Belarusian",
    "Farsi",
    "Basque",
    "Macedonian",
    "Afrikaans",
    "Faeroese",
    "Latin",
    "Esperanto",
    "Tamazight",
    "Armenian"
    )

GLS_PROP_NAME={
    0x01:"Title",
    0x02:"Author Name",
    0x03:"Author Email",
    0x04:"Copyright",
    0x07:"Source Language",
    0x08:"Target Language",
    0x09:"Description",
    0x0B:"Icon",
    0x0C:"Entry Count",
    0x1A:"Source Charset",
    0x1B:"Target Charset",
    0x27:"Word Class Name", # localized word class name
    0x33:"Creation Date",
    0x1C:"Last Updated",
    0x3B:"Morphological Derivation Type", # localized names of word variation type
    0x41:"Glossary Manual"
    }

CHARSET = {
    0x41: "ISO-8859-1", #Default
    0x42: "ISO-8859-1", #Latin
    0x43: "ISO-8859-2", #Eastern European
    0x44: "ISO-8859-5", #Cyriilic
    0x45: "ISO-8859-14",#Japanese
    0x46: "big5",       #Traditional Chinese
    0x47: "gbk",        #Simplified Chinese
    0x48: "CP1257",     #Baltic
    0x49: "CP1253",     #Greek
    0x4A: "ISO-8859-15",#Korean
    0x4B: "ISO-8859-9", #Turkish
    0x4C: "ISO-8859-9", #Hebrew
    0x4D: "CP1256",     #Arabic
    0x4E: "CP874"       #Thai
    }

TERM_PROP_NAME={
    0x08: "Display Name",
    0x1b: "Transcription",
    0x02: "Lexcial Class",
    
    }
    
class GlsTerm:
    def __init__(self,title,definition,prop,tail):
        self.title=title
        self.definition=definition
        self.property=prop
        self.tail=tail

class GlsResource:
    def __init__(self,name,data):
        self.name=name
        self.data=data

class GlsContentParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.parts=[]
        self.tags=[]

    def reset(self):
        HTMLParser.reset(self)
        self.parts=[]
        self.tags=[]

    def handle_charref(self,name):
        self.parts.append(chr(int(name)))
    
    def handle_starttag(self,tag,attrs):
        #print("start: "+tag)
        attrs=dict(attrs)
        if tag=="font":
            color=attrs.get("color")
            if color!=None:
                self.parts.append("<font color='"+color+"'>")
                self.tags.append("font")
            else:
                self.tags.append(None)
        elif tag=="a":
            self.parts.append("<a href='")
            href=attrs.get('href')
            self.parts.append("entry://")
            self.parts.append(href.split("://")[1])
            self.parts.append("'>")
            self.tags.append('a')
        elif tag=="br":
            self.parts.append("<br/>")
        elif tag=="img":
            self.parts.append("<img")
            self.parts.append(" src='/")
            self.parts.append(attrs.pop("src"))
            self.parts.append("'")
            #print(attrs)
            for k in attrs:
                self.parts.append(" "+k+"='"+attrs[k]+"'")
            self.parts.append('/>')
        elif tag=="charset":
            self.tags.append("charset")
        else:
            self.parts.append("<"+tag+">")
            self.tags.append(tag)

    def handle_startendtag(self,tag,attrs):
        #print("start end: "+tag)
        self.parts.append("<")
        self.parts.append(tag)
        for k in attrs:
            self.parts.append(" "+k+"='"+v+"'")
        self.parts.append("/>")
    
    def handle_endtag(self,tag):
        #print("end: "+tag)
        if len(self.tags)==0:
            return
        if self.tags[-1]==None and tag=='font': # eliminate font tag with only face attribute
            self.tags.pop()
            return
        if self.tags[-1]!=tag: # if tag is invalid, ignore it
            return
        if self.tags[-1]=='charset':
            self.tags.pop()
            return
        self.tags.pop()
        self.parts.append('</'+tag+'>')

    def handle_data(self,data):
        if len(self.tags)==0:
            self.parts.append(data)
            return
        lasttag=self.tags[-1];
        if lasttag=="charset":
            self.parts.append(chr(int(data[0:4],16)))
        else:
            self.parts.append(data)
    

class Glossary(dict):
    def __init__(self):
        dict.__init__(self)
    
    def put(self,k,parts):
        if k[-1]!='$':
            title=k
            num=0
        else:
            (title,*num)=k.rsplit('$',2)
            try:
                num=int(num[0])
            except:
                title=k
                num=0
        if self.get(title)==None:
            self[title]={num:parts}
        else:
            self[title][num]=parts

