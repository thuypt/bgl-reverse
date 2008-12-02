import codecs

RC_META=0 # meta ???
RC_INFO=3 # info
RC_NULL_1=6  # end of dict meta and info, entries and resources will follow

RC_ENTRY_1=0x1
RC_ENTRY_A=0xA
RC_ENTRY_B=0xB

RC_RES=2
RC_NULL_2=4
RC_EOF=5


WordClass = {
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

WordVariation = (
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

InfoName={
    0x01:"Glossary Name",
    0x02:"Author",
    0x03:"Author Email",
    0x04:"Copyright",
    0x07:"Source Language",
    0x08:"Target Language",
    0x09:"Description",
    0x0B:"Icon",
    0x0C:"Entry Count",
    0x1A:"Source Encoding",
    0x1B:"Target Encoding",
    0x27:"Word Class Name", # localized word class name
    0x3B:"Morphological Derivation Type", # localized names of word variation type
    0x41:"Manuel"
    }

LANG = (
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

Charset = [
    "ISO-8859-1", #Default
    "ISO-8859-1", #Latin
    "ISO-8859-2", #Eastern European
    "ISO-8859-5", #Cyriilic
    "ISO-8859-14",#Japanese
    "BIG5",       #Traditional Chinese
    "GB2312",     #Simplified Chinese
    "CP1257",     #Baltic
    "CP1253",     #Greek
    "ISO-8859-15",#Korean
    "ISO-8859-9", #Turkish
    "ISO-8859-9", #Hebrew
    "CP1256",     #Arabic
    "CP874"       #Thai
    ]

def parseInt(data):
    """parse a big-endian integer"""
    value=0;
    for byte in data:
        value=value<<8
        value=value+byte
    return value

def readRecord(f):
    hdr=f.read(1)[0]
    high_nibble=hdr>>4
    rec_type=hdr&0x0F
    
    if high_nibble>=4:
        rec_len=high_nibble-4
    else:
        rec_len=parseInt(f.read(high_nibble+1))
    return (rec_type,f.read(rec_len))

def parseBlock_A(data,size):
    blk_len=parseInt(data[0:size])
    return (data[size:size+blk_len],data[size+blk_len:])

def parseBlock_B(data,size):
    """return a tuple (spec,parsed,unparsed)"""
    return (data[0],data[1:size+1],data[size+1:])

def parseDefMeta(meta):
    """return a tuple (word_class,display_name,word_variation, alternatives)"""
    defmeta={}
    while len(meta)>0:
        spec=meta[0]
        if (spec == 0x06) or (spec == 0x02):
            defmeta[spec]=meta[1]
            meta=meta[2:]
            continue
        elif spec == 0x13: # unknown
            defmeta[spec]=meta[1]
            meta=meta[2:]
            continue
        elif spec == 0xC7:
            defmeta[spec]=None
            meta=meta[1:]
        elif spec == 0x50:
            spec = meta[1]
            (defmeta[spec],meta)=parseBlock_A(meta[2:],1)
            continue
        elif spec == 0x60:
            spec = meta[1]
            (defmeta[spec],meta)=parseBlock_A(meta[2:],2)
        elif spec == 0x18: # display name
            (defmeta[spec],meta)=parseBlock_A(meta[1:],1)
            continue
        elif (spec>>4)==4:
            (spec,data,meta)=parseBlock_B(meta[1:],(spec&0x0F)+1)
            defmeta[0x4000+spec]=data
            continue
        else:
            print([meta])
            raise Exception("unknown data: "+str(spec)+"\n"+str(defmeta))
    return defmeta

def parseInfo(data):
    return (parseInt(data[0:2]),data[2:])

def parseMeta(data):
    return (parseInt(data[0:1]),data[1:])

def parseEntry(data):
    (hw,data)=parseBlock_A(data,1)
    (defs,data)=parseBlock_A(data,2)
    if len(data)>0:
        entry_tail=parseBlock_A(data,1)[0]
    else:
        entry_tail=b''
    
    (def_text,*def_meta)=defs.split(b'\x14',1)
    if len(def_meta)>0:
        def_meta=def_meta[0]
    else:
        def_meta=b''
    return (hw,def_text,parseDefMeta(def_meta),entry_tail)

def replaceHTMLEntity(data):
    """replace &#***; to char, use with caution"""
    while True:
        loc=data.find(b'&#')
        if loc==-1:
            break
        end=data.find(b';',loc)
        data=data[0:loc]+bytes([int(data[loc+2:end])])+data[end+1:]
    return data

def replaceCharsetTag(data,encoding):
    """decode the data and replace <charset c=T>****;</charset> with the char value"""
    loc=data.find(b'<charset c=')
    if loc==-1:
        return codecs.decode(data,encoding)
    else:
        end=data.find(b'</charset>',loc)
        return codecs.decode(data[0:loc],encoding)\
            +codecs.decode(b'\\u'+data[loc+13:loc+17],'unicode_escape')\
            +replaceCharsetTag(data[end+10:],encoding)

class Record:
    def __init__(self,path):
        self.path=path
        self.file=open(path,'rb')
        self.eof=False
        return

    def read(self):
        if self.eof:
            return (None,None)
        rec=readRecord(self.file)
        if rec[0]==RC_EOF:
            self.eof
        return rec

class BGL(Record):
    
    def __init__(self,path):
        Record.__init__(self,path)
        rawinfo={}
        rawmeta={}
        while True:
            rec=self.read()
            if rec[0]==RC_NULL:
                break
            if rec[0]==RC_META:
                (meta,data)=parseMeta(rec[1])
                rawmeta[meta]=data
                continue
            elif rec[0]==RC_INFO:
                (info,data)=parseInfo(rec[1])
                rawinfo[info]=data
                continue
        
        self.rawinfo=rawinfo
        self.rawmeta=rawmeta
        self.info=self.parseInfo()
        return

    def readnparse(self):
        rec=self.read()
        if rec[0]==RC_ENTRY_1:
            ent=parseEntry(rec[1])
            phone=ent[2].get(0x1B)
            if phone!=None:
                ent[2][0x1B]=replaceCharsetTag(replaceHTMLEntity(phone),"ISO-8859-1")
            return (
                replaceCharsetTag(ent[0],self.info["Source Encoding"]),
                replaceCharsetTag(ent[1],self.info["Target Encoding"]),
                ent[2],
                replaceCharsetTag(ent[3],self.info["Source Encoding"]))

        return ent

    def parseInfo(self):
        rawmeta=self.rawmeta
        rawinfo=self.rawinfo
        info={}
        info["Default Encoding"]=Charset[rawmeta[0x08][0]-65]
        info["Glossary Name"]=rawinfo[0x01]
        info["Author"]=rawinfo[0x02]
        info["Author Email"]=rawinfo[0x03]
        info["Copyright"]=rawinfo[0x04]
        info["Source Language"]=LANG[parseInt(rawinfo[0x07])]
        info["Target Language"]=LANG[parseInt(rawinfo[0x08])]
        info["Description"]=rawinfo[0x09]
        info["Entry Count"]=parseInt(rawinfo[0x0C])        
        info["Source Encoding"]=Charset[parseInt(rawinfo[0x1A])-65]
        info["Target Encoding"]=Charset[parseInt(rawinfo[0x1B])-65]
        return info


