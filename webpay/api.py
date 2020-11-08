"""
Webpay API interface
full documentation at: https://webpay.bahamta.com/doc/api
"""

import re
import json
from pathlib import Path
from typing import Optional
from .exceptions import APIError, DependencyError


def get_version():
    """
    Read version from __init__ file
    """
    txt = (Path(__file__).parent / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


class WebpayBase:
    BASE_URL = "https://webpay.bahamta.com/api"
    DOCS_URL = "https://webpay.bahamta.com/doc/api"
    USER_AGENT = f"Webpay Python library - {get_version()}"

    def __init__(self, api_key: str):
        self._API_KEY = api_key

    def _request(self,
                 method: str,
                 params: str):
        """
        Make HTTP API requests

        :param method: Webpay API methods
        :param params: request parameters in query string format
        :return: dict
        """
        pass

    def payment(self,
                reference: str,
                amount_irr: int,
                callback_url: str,
                payer_mobile: Optional[str] = None,
                trusted_pan: Optional[str] = None):
        """
        Create a new payment
        Payment URL will be returned

        :param reference: unique payment ID
        :param amount_irr: payment amount in rial
        :param callback_url: callback url starting with 'http' or 'https'
        :param payer_mobile: payer phone number
        :param trusted_pan: range of valid cards to payment
        :return: str
        """
        pass

    def verify(self,
               reference: str,
               amount_irr: int):
        """
        Verify a payment
        Payment data will be returned if there was no error

        :param reference: unique payment ID
        :param amount_irr: payment amount in rial
        :return: dict
        """
        pass


class WebpayAPI(WebpayBase):
    """
    Webpay API class

    :param api_key: api_key provided by Webpay
    :raises DependencyError: if "requests" was not installed
    """

    def __init__(self, api_key: str):
        super(WebpayAPI, self).__init__(api_key)
        try:
            import requests
            self._requests = requests
        except ImportError:
            raise DependencyError(
                'Module "requests" must be installed to use WebpayAPI')

    def _request(self,
                 method: str,
                 params: str):

        query_string = f'?api_key={self._API_KEY}&{params}'
        headers = {"user-agent": self.USER_AGENT}
        url = self.BASE_URL + method + query_string
        jdata = self._requests.get(url, headers=headers).json()

        if jdata.get("ok") is False:
            error_key = jdata.get("error")
            raise APIError(error_key, f'\n(Read docs at: {self.DOCS_URL})')
        return jdata.get("result", {})

    def payment(self,
                reference: str,
                amount_irr: int,
                callback_url: str,
                payer_mobile: Optional[str] = None,
                trusted_pan: Optional[str] = None):

        method = '/create_request'
        params = f'reference={reference}&amount_irr={amount_irr}&callback_url={callback_url}'
        if payer_mobile is not None:
            params += f'&payer_mobile={payer_mobile}'
        if trusted_pan is not None:
            params += f'&trusted_pan={trusted_pan}'

        res = self._request(method, params)
        return res.get('payment_url')

    def verify(self,
               reference: str,
               amount_irr: int):

        method = '/confirm_payment'
        params = f'reference={reference}&amount_irr={amount_irr}'

        res = self._request(method, params)
        return res


class AsyncWebpayAPI(WebpayBase):
    """
    Webpay API class with async methods

    :param api_key: api_key provided by Webpay
    :raises DependencyError: if "aiohttp" was not installed
    """

    def __init__(self, api_key: str):
        try:
            import aiohttp
            self._aiohttp = aiohttp
        except ImportError:
            raise DependencyError(
                'Module "aiohttp "must be installed to use AsyncWebpayAPI')
        super(AsyncWebpayAPI, self).__init__(api_key)

    async def _request(self,
                       method: str,
                       params: str):

        query_string = f'?api_key={self._API_KEY}&{params}'
        headers = {"user-agent": self.USER_AGENT}
        url = self.BASE_URL + method + query_string
        async with self._aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                jdata = json.loads(await resp.text())

        if jdata.get("ok") is False:
            error_key = jdata.get("error")
            raise APIError(error_key, f'\n(Read docs at: {self.DOCS_URL})')
        return jdata.get("result", {})

    async def payment(self,
                      reference: str,
                      amount_irr: int,
                      callback_url: str,
                      payer_mobile: Optional[str] = None,
                      trusted_pan: Optional[str] = None):

        method = '/create_request'
        params = f'reference={reference}&amount_irr={amount_irr}&callback_url={callback_url}'
        if payer_mobile is not None:
            params += f'&payer_mobile={payer_mobile}'
        if trusted_pan is not None:
            params += f'&trusted_pan={trusted_pan}'

        res = await self._request(method, params)
        return res.get('payment_url')

    async def verify(self,
                     reference: str,
                     amount_irr: int):

        method = '/confirm_payment'
        params = f'reference={reference}&amount_irr={amount_irr}'

        res = await self._request(method, params)
        return res
