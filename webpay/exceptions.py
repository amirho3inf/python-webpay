"""
See APIError's at: https://webpay.bahamta.com/doc/api
"""


class DependencyError(Exception):
    pass


class APIError(Exception):
    error_key: str = ''

    def __init__(self, error_key: str, message: str):
        super(APIError, self).__init__(f'{error_key} {message}')
        self.error_key = error_key
