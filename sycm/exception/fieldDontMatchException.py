class FieldDontMatchException(Exception):
    def __init__(self,tr,tb):
        self.message = "字段长度不一致" +str(tr)+str(tb)

    def __str__(self):
        return self.message
    
    