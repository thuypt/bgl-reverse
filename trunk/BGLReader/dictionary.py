

class Definition:
    def __init__(self,hw,lex_cls=None):
        pass

class Article:
    def __init__(self,hw=None,etym=None,phon=None,defs=[],alt=[]):
        self.etym=etym
        self.hw=hw
        self.phon=phon
        self.defs=defs
        self.alt=alt

class Resource:
    def __init__(self,name,data):
        self.name=name
        self.data=data

    def save(self,path):
        pass
