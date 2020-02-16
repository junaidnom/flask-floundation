from enum import Enum


class ResponseCodesEnum(Enum):
    Success = 200
    Created = 201
    Invalid_Argument = 400
    Unauthorized = 401
    Forbidden = 403
    Not_Found = 404
    Im_A_Teapot = 418
    Internal_Server_Error = 500


def request_response_codes(**args):
    codes = {}
    if args:
        for arg in args:
            codes[arg.value] = arg.name.replace("_", " ")
    else:
        for data in ResponseCodesEnum:
            codes[data.value] = data.name.replace("_", " ")
    return codes


def generic_response(status=200, message="Success", data=None):
    return {"status": status, "message": message, "data": data}, status
