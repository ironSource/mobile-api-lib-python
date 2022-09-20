"""IronSource API"""
from ironsource_api.monetize_api.monetize_api import MonetizeAPI

from ironsource_api.promote_api.promote_api import PromoteAPI


class IronSourceAPI:
    """IronSource API"""
    promote_api_instance: PromoteAPI = None
    monetize_api_instance: MonetizeAPI = None
    __user = None
    __token = None
    __secret = None

    def monetize_api(self) -> MonetizeAPI:
        """returns Monetize API"""
        if not self.monetize_api_instance:
            self.monetize_api_instance = MonetizeAPI()
            if self.__user \
                    and self.__token \
                    and self.__secret:
                self.monetize_api_instance.set_credentials(user=self.__user,
                                                           token=self.__token,
                                                           secret=self.__secret)
        return self.monetize_api_instance

    def promote_api(self) -> PromoteAPI:
        """returns Promote API"""
        if not self.promote_api_instance:
            self.promote_api_instance = PromoteAPI()
            if self.__user \
                    and self.__token \
                    and self.__secret:
                self.promote_api_instance.set_credentials(user=self.__user,
                                                          token=self.__token,
                                                          secret=self.__secret)
        return self.promote_api_instance

    def set_credentials(self, user: str, token: str, secret: str):
        """sets credentials for the APIs"""
        self.__user = user
        self.__token = token
        self.__secret = secret
        if self.monetize_api_instance:
            self.monetize_api_instance.set_credentials(user=user, token=token, secret=secret)
        if self.promote_api_instance:
            self.promote_api_instance.set_credentials(user=user, token=token, secret=secret)
