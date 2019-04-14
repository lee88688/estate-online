from flask import jsonify


class ApiResult(object):
    def __init__(self, **kwargs):
        self.success = True
        self.message = ''
        self.result = {}
        self.__dict__.update(kwargs)

    def make_response(self):
        response = {
            'success': self.success,
            'message': self.message,
            'result': self.result
        }
        return jsonify(response)

    def __repr__(self):
        title = 'success' if self.success else 'failure'
        return f'<response {title}({self.message})>'


class ApiRequest(object):
    def __init__(self, request):
        self.request = request


parameter_error = ApiResult(success=False, message='parameter error!')
