from api.schemas.common import ResponseModel

def success(data = None) -> ResponseModel:
    return ResponseModel(data=data)

def failure(status :int,errmsg:str,data = None) -> ResponseModel:
    return ResponseModel(status=status, errmsg=errmsg, data=data)