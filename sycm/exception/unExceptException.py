class UnExceptDateException(Exception):
    def __init__(self, surpose_date, targe_date):
        self.message = '预期参数与实际参数不符：预期%s实际%s' % (surpose_date, targe_date)

    def __str__(self):
        return self.message
    
    