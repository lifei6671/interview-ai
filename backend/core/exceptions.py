# custom_exceptions.py
class BusinessException(Exception):
    """业务异常基类（所有业务异常都继承它）"""
    status_code = 400
    errmsg:str = "处理异常"

    def __init__(self, errmsg:str|None=None,status_code:int|None=None):
        if errmsg is not None:
            self.errmsg = errmsg
        if status_code is not None:
            self.status_code = status_code

        super().__init__(self.errmsg)

class ResourceNotFoundError(BusinessException):
    """资源不存在异常（对应 HTTP 404）"""
    status_code = 404
    errmsg = "请求的资源不存在"

class ResourceDuplicateError(BusinessException):
    """资源重复异常"""
    status_code = 400
    errmsg = "参数格式错误或不完整"