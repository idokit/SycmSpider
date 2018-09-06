class UnExceptDateException(Exception):
    def __init__(self, surpose_date, targe_date):
        self.message = '预期参数与实际参数不符：预期%s实际%s' % (surpose_date, targe_date)

    def __str__(self):
        return self.message


class FieldDontMatchException(Exception):
    def __init__(self, tr, tb):
        self.message = "字段长度不一致" + str(tr) + str(tb)

    def __str__(self):
        return self.message


class SessionExpiredException(Exception):
    def __init__(self, url=None):
        self.message = r"会话过期：页面被重定向{}".format(url)

    def __str__(self):
        return self.message


class LackOfDataException(Exception):
    def __init__(self, url=None):
        self.message = r"数据缺失{}".format(url)

    def __str__(self):
        return self.message


class SycmBusyException(Exception):
    def __init__(self, url=None):
        self.message = r"服务器繁忙{}".format(url)

    def __str__(self):
        return self.message


class OtherException(Exception):
    def __init__(self, text=None):
        self.message = r"未察觉的错误{}".format(text)

    def __str__(self):
        return self.message
