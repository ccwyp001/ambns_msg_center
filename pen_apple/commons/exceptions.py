from . import httpcodes

class BaseException(Exception):
    http_code = httpcodes.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = '0000000'
    message = '请勿直接使用此异常类型'

    def __init__(self, errors=None):
        self.errors = errors

    def to_dict(self):
        data = {}
        data['code'] = self.business_code
        data['message'] = self.message
        if self.errors is not None:
            data['errors'] = self.errors
        return data


class OperationSuccess(BaseException):
    http_code = httpcodes.HTTP_200_OK
    business_code = '100000'
    message = '成功'


class DataValidateError(BaseException):
    http_code = httpcodes.HTTP_401_UNAUTHORIZED
    business_code = '100001'
    message = '数据验证错误'


class Querying(BaseException):
    http_code = httpcodes.HTTP_200_OK
    business_code = '100100'
    message = '正在查询，结果未返回'


class ScriptError(BaseException):
    http_code = httpcodes.HTTP_200_OK
    business_code = '100400'
    message = '执行结果异常，请重试'


class AccountLoadError(BaseException):
    http_code = httpcodes.HTTP_401_UNAUTHORIZED
    business_code = '101001'
    message = '账号加载失败'


class AccountLoginFailed(BaseException):
    status = httpcodes.HTTP_401_UNAUTHORIZED
    business_code = '101002'
    message = '账号或密码错误'


class InsufficientPrivilege(BaseException):
    http_code = httpcodes.HTTP_403_FORBIDDEN
    business_code = '101003'
    message = '账号权限不足'


class UserDoesNotExist(BaseException):
    http_code = httpcodes.HTTP_404_NOT_FOUND
    business_code = '102001'
    message = '用户不存在'


class UserAlreadyExist(BaseException):
    http_code = httpcodes.HTTP_400_BAD_REQUEST
    business_code = '102002'
    message = '用户已存在'


class PartnerDoesNotExist(BaseException):
    http_code = httpcodes.HTTP_404_NOT_FOUND
    business_code = '103001'
    message = '合作伙伴不存在'


class SuperUserDoesNotExist(BaseException):
    http_code = httpcodes.HTTP_404_NOT_FOUND
    business_code = '104001'
    message = '管理员不存在'


class SSHVerificationFailed(BaseException):
    http_code = httpcodes.HTTP_400_BAD_REQUEST
    business_code = '105001'
    message = '连接失败'


class InspectItemDoesNotExist(BaseException):
    http_code = httpcodes.HTTP_404_NOT_FOUND
    business_code = '200001'
    message = '巡检项不存在'


class ItemDoesNotExist(BaseException):
    http_code = httpcodes.HTTP_404_NOT_FOUND
    business_code = '200001'
    message = '请求数据不存在'


class DataCommitError(BaseException):
    http_code = httpcodes.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = '200002'
    message = '数据提交失败'


class ErrorTemplate(BaseException):
    http_code = httpcodes.HTTP_400_BAD_REQUEST
    business_code = '200003'
    message = '当前系统仅支持标准版模板'


class KeepCommitError(BaseException):
    http_code = httpcodes.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = '300001'
    message = '保存现场失败'


class Connect(BaseException):
    http_code = httpcodes.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = '300003'
    message = '连接失败'


class ConnectCommitError(BaseException):
    http_code = httpcodes.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = '300002'
    message = ''


class QueryFail(BaseException):
    http_code = httpcodes.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = '400000'
    message = '查询失败'

class KeepErro(BaseException):
    http_code = httpcodes.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = '300006'
    message = '保存现场失败'
