"""
Base Class for Monetize and Promote APIs
"""
from datetime import datetime
import base64
import json
from .utils import get_bearer_auth, get_basic_auth


class BaseAPI:
    """IronSource Base API"""
    __username = None
    __token = None
    __secret = None
    __auth_token = None
    __expiration = None

    ################
    # Authentication
    ################
    def set_credentials(self, user: str, token: str, secret: str):
        """sets the API credentials
        :param user: - user name from the platform
        :type user: str
        :param token: - token from the platform
        :type token: str
        :param secret: - secret from the platform
        :type secret: str
        """
        if (self.__username != user or self.__secret != secret or self.__token != token):
            self.__auth_token = ''
            self.__expiration = -1

        self.__username = user
        self.__token = token
        self.__secret = secret



    async def get_bearer_auth(self):
        """
        parse and save token in session
        :return str: temporary bearer token
        """
        if (self.__auth_token and datetime.fromtimestamp(round(self.__expiration / 1000)) > datetime.utcnow()):
            return self.__auth_token
        token = await get_bearer_auth(secret=self.__secret,token=self.__token)
        if token:
            base64_str = token.split('.')[1]
            token_info_str = base64.b64decode(base64_str.encode()+ b'==')
            token_obj = json.loads(token_info_str)
            self.__expiration = token_obj['exp']
            self.__auth_token = token
            return token

    def get_basic_auth(self):
        """

        :return: basic token
        :rtype: str
        """
        return get_basic_auth(username=self.__username,secret=self.__secret)
