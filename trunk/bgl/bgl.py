import io
import gzip

import util
import gls

from html.parser import HTMLParser

def unpack_block(data:memoryview,x:int)-> (memoryview,memoryview):
    """return a tuple (block_data,unprocessed)"""
    blk_len=util.unpack_ui(bytes(data[0:x]))
    return (data[x:x+blk_len],data[x+blk_len:])

def unpack_property(data:memoryview) -> (int,memoryview):
    return (util.unpack_ui(bytes(data[0:2])),data[2:])

def unpack_parameter(data:memoryview) -> (int,bytes):
    return (data[0],bytes(data[1:]))

def unpack_term_property(data:bytes) -> dict:
    """return dict(prop_id -> prop_value)"""
    prop={}
    while len(data)>1:
        spec=data[0]
        if spec<0x40:
            prop_id=0x0f&spec
            if (spec>>4)==0:
                prop_value=data[1]
                data=data[2:]
            else:
                (prop_value,data)=unpack_block(data,1)
        else:
            prop_id=data[1] # next byte as prop id
            v_len=spec-0x3f
            if v_len>0x10:
                (prop_value,data)=unpack_block(data[1:],1)
            else:
                prop_value=data[1:1+v_len]
                data=data[1+v_len:]
        prop[prop_id]=prop_value
    return prop

def unpack_term(data:memoryview) -> (memoryview, memoryview, list, dict):
    """return (title,definition,alternatives,properties)"""
    (title,data)=unpack_block(data,1)
    (definition,data)=unpack_block(data,2)
    alternatives=[]
    while len(data)>0:
        (alt_i,data)=unpack_block(data,1)
        alternatives.append(alt_i)

    (definition,rawprop)=util.mem_split(definition,0x14)
    return (title,definition,alternatives,unpack_term_property(bytes(rawprop)))

def unpack_res(data:memoryview) -> (memoryview,memoryview):
    return unpack_block(data,1)

class BGLReader(gzip.GzipFile):
    def __init__(self,path:str):
        f=open(path,'rb')
        BGLReader._seek_to_gz_header(f)
        gzip.GzipFile.__init__(self,fileobj=f)
        self._eof=False
        self._next_rec=None
        return
    
    @staticmethod
    def _seek_to_gz_header(f):
        header=util.read_ui(f,4)
        if header==0x12340001:
            f.seek(0x69)
        elif header==0x12340002:
            f.seek(0x69)
        else:
            raise IOError("invald header: {0:#x}".format(header))
        return

    def _read_rec_data(self,pspec:int) -> memoryview:
        """read record data with high nibble of spec"""
        if pspec<4:
            rec_len=util.read_ui(self,pspec+1)
        else:
            rec_len=pspec-4

        return memoryview(self.read(rec_len))

    def _read_rec(self) -> (int,memoryview):
        spec=util.read_ui(self,1)
        if spec==None:
            return None
        
        rec_type=spec&0x0f
        rec_data=self._read_rec_data(spec>>4)
        
        return (rec_type,rec_data)
        
    
    def next_rec(self) -> (int,memoryview):
        """read next record from a BGLFile, return a tuple (rec_type,data), None if eof"""
        if self.eof():
            return None
        else:
            rec=self._next_rec
            self._next_rec=None
            return rec
    
    def eof(self) -> bool:
        if self._eof:
            return True
        elif self._next_rec != None :
            return False
        else:
            self._next_rec=self._read_rec()
            if self._next_rec==None:
                self._eof=True
                return True
            else:
                return False

    def reset(self):
        self.seek(0)



def parse_property(data:dict)->dict:
    prop={}
    
    prop[0x1a]=gls.CHARSET[util.unpack_ui(bytes(data[0x1a]))]
    prop[0x1b]=gls.CHARSET[util.unpack_ui(bytes(data[0x1b]))]

    for prop_id in [0x01,0x02,0x03,0x04,0x05]:
        prop[prop_id]=bytes(data[prop_id]).decode('latin1')

    for prop_id in [0x0B,0x41]:
        prop[prop_id]=data[prop_id]
    
    return prop


class GLSHTMLContentFilter(HTMLParser):
    
    def __init__(self,a_href,img_src):
        HTMLParser.__init__(self)
        self.parts=[]
        self.tags=[]
        self.transform_a_href=a_href
        self.transform_img_src=img_src

    def reset(self):
        HTMLParser.reset(self)
        self.parts=[]
        self.tags=[]
    
    def handle_entityref(self,name:str):
        self.parts.append('&'+name+';')

    def handle_charref(self,name):
        self.parts.append(chr(int(name)))
    
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=="font":
            color=attrs.get("color")
            if color!=None:
                self.parts.append("<font color='"+color+"'>")
                self.tags.append("font")
            else:
                # color tag is useless
                # by pushing None, the close tag will be ignored
                self.tags.append(None)
        elif tag=="a":
            self.parts.append("<a href='"+self.transform_a_href(attrs.get('href'))+"'>")
            self.tags.append('a')
        elif tag=="br":
            self.parts.append("<br/>")
        elif tag=="img":
            self.parts.append("<img src='"+self.transform_img_src(attrs.pop("src")))
            for k in attrs:
                self.parts.append("' "+k+"='"+attrs[k])
            self.parts.append("'/>")
        elif tag=="charset":
            self.tags.append("charset")
        else:
            # default action
            self.parts.append(self.get_starttag_text())
            self.tags.append(tag)
        return

    def handle_startendtag(self,tag,attrs):
        self.parts.append(self.get_starttag_text())
        return
    
    def handle_endtag(self,tag):
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
        return

class BGLParser:
    def __init__(self,reader:BGLReader):
        self.reader=reader
        reader.reset()
        self.raw_parameters={}
        self.raw_properties={}

        while True:
            rec=reader.next_rec()
            if rec[0]==gls.DELIMITER:
                break
            elif rec[0]==gls.PARAMETER:
                (k,v)=unpack_parameter(rec[1])
                self.raw_parameters[k]=v
            elif rec[0]==gls.PROPERTY:
                (k,v)=unpack_property(rec[1])
                self.raw_properties[k]=v
        self._parse_properties()
        self.handle_properties(self.properties)
        return

    def _parse_properties(self):
        self.properties={
            'source_charset':gls.CHARSET[bytes(self.raw_properties[0x1A])[0]],
            'target_charset':gls.CHARSET[bytes(self.raw_properties[0x1B])[0]],
            'title':bytes(self.raw_properties[0x01]).decode('latin1'),
            'description':bytes(self.raw_properties[0x09]).decode('latin1')
        }
        
        return
    
    def execute(self):
        html=GLSHTMLContentFilter(self.transform_a_href,self.transform_img_src)
        charset_s=self.properties['source_charset']
        charset_t=self.properties['target_charset']
        
        while not self.reader.eof():
            rec=self.reader.next_rec()
            html.reset()
            if rec[0] == gls.TERM_A:
                (title_r,definition_r,alternatives_r,properties_r)=unpack_term(rec[1])
                title=util.decode(bytes(title_r),charset_s)
                
                alternatives=[]
                for alt in alternatives_r:
                    alternatives.append( util.decode(bytes(alt), charset_s) )
                definition=util.decode(bytes(definition_r),charset_t)
                try:
                    html.feed(definition)
                    html.close()
                except:
                    self.handle_error(title,definition,alternatives,properties_r)
                    continue
                
                self.handle_term(
                    title,
                    html.parts,
                    alternatives,
                    properties_r)
            elif rec[0] == gls.RESOURCE:
                (name_r,data)=unpack_res(rec[1])
                self.handle_res(
                    bytes(name_r).decode('latin1'),
                    data)
                
        self.handle_exec_end()
        return

    def handle_term(self, title:str,def_frag:list,alternatives:list,properties:dict):
        pass

    def handle_res(self, name:str,data:bytes):
        pass
    
    def handle_error(self,title_r:bytes,definition_str:str,alternatives_r:list,properties:dict):
        pass

    def handle_properties(self,properties:dict):
        pass

    def handle_handle_exec_end(self):
        pass
    
    def transform_a_href(self,href:str) -> str:
        pass
    
    def transform_img_src(self,href:str) -> str:
        pass

        


    


