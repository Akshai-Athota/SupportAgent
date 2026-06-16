class kbResponse():
    response:str
    source:str
    intent:str
    category:str

    def __init__(self,response:str,source:str=None,intent:str=None,category:str=None):
        self.response=response
        self.source=source
        self.category=category
        self.intent=intent