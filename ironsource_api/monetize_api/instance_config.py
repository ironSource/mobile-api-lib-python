# pylint: disable=too-many-lines
"""
Module for creating instances object
"""
from typing import Dict, List

from ironsource_api.monetize_api import Networks, AdUnits


class InstanceConfig:  # pylint: disable=missing-class-docstring
    """base class for Instance"""
    _instance_ad_source_name: Networks
    _instance_name: str
    _instance_ad_unit: AdUnits
    _status: bool
    _instance_id: int
    _rate: float

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, status: bool,
                 # pylint: disable=too-many-arguments
                 instance_id: int, rate: float = None):
        super().__init__()
        self._instance_id = instance_id
        self._instance_ad_unit = ad_unit
        self._instance_ad_source_name = ad_source
        self._instance_name = instance_name
        self._status = status
        self._rate = rate

    def get_ad_source(self) -> Networks:  # pylint: disable=missing-function-docstring
        return self._instance_ad_source_name.value

    def get_instance_id(self) -> int:  # pylint: disable=missing-function-docstring
        return self._instance_id

    def get_instance_name(self) -> str:  # pylint: disable=missing-function-docstring
        return self._instance_name

    def get_instance_ad_unit(self) -> str:  # pylint: disable=missing-function-docstring
        return self._instance_ad_unit.value

    def get_status(self) -> bool:  # pylint: disable=missing-function-docstring
        return self._status

    def get_rate(self) -> float:  # pylint: disable=missing-function-docstring
        return self._rate

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring #pylint: disable=missing-function-docstring
        pass

    def get_object(self) -> dict:
        """
        returns formatted dictionary for api request
        :return dict: formatted dictionary for the instance
        """
        obj = {'instanceName': self._instance_name,
               'status': 'active' if self._status else 'inactive'}

        if self._rate:
            obj['rate'] = self._rate

        return obj


class IronSourceBase(InstanceConfig):
    """IronSource Base Instance"""
    _application_key: str
    _instance_pricing: list = []

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, application_key: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, pricing: Dict[int, List[str]] = None):  # pylint: disable=too-many-arguments
        super().__init__(ad_source, instance_name, ad_unit, status, instance_id)
        self._application_key = application_key
        self._instance_pricing = []
        if pricing:
            for price, countries in pricing.items():
                self._instance_pricing.append(
                    {'eCPM': price, 'country': countries})

    def get_pricing_obj(self):  # pylint: disable=missing-function-docstring #pylint: disable=missing-function-docstring
        return self._instance_pricing

    def get_key(self):  # pylint: disable=missing-function-docstring
        return self._application_key

    def get_object(self):  # pylint: disable=missing-function-docstring #pylint: disable=missing-function-docstring
        obj = super().get_object()
        if self.get_pricing_obj():
            obj['pricing'] = self.get_pricing_obj()
        return obj


class IronSourceInstance(IronSourceBase):
    """Create IronSource Instance

        :param instance_name: name for the instance
        :type instance_name: str
        :param ad_unit: Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param application_key: Application key for the instance
        :type application_key: str
        :param pricing: dictionary of price and list of countries, defaults to None
        :type pricing: Dict[int, List[str]], optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, application_key: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 pricing: Dict[int, List[str]] = None, instance_id: int = -1):  # pylint: disable=too-many-arguments
        super().__init__(Networks.IronSource, instance_name,
                         ad_unit, application_key, status, instance_id, pricing)


class IronSourceBidding(IronSourceBase):
    """Create IronSource bidding instance

        :param instance_name:  name for the instance
        :type instance_name: str
        :param ad_unit: Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param application_key: Application key for the instance
        :type application_key: str
        :param pricing: dictionary of price and list of countries, defaults to None
        :type pricing: Dict[int, List[str]], optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, application_key: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 pricing: Dict[int, List[str]] = None, instance_id: int = -1):  # pylint: disable=too-many-arguments

        super().__init__(Networks.IronSourceBidding, instance_name,
                         ad_unit, application_key, status, instance_id, pricing)


class AdColonyBase(InstanceConfig):
    """AdColony Instance"""
    _app_id: str
    _zone_id: str

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, app_id: str, zone_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):
        super().__init__(ad_source, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._zone_id = zone_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_zone_id(self):  # pylint: disable=missing-function-docstring
        return self._zone_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {'appID': self.get_app_id()}

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['zoneId'] = self.get_zone_id()
        return obj


class AdColonyInstance(AdColonyBase):
    """AdColony instance

        :param instance_name:  name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: AdColony App ID
        :type app_id: str
        :param zone_id: AdColony Zone ID
        :type zone_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, zone_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):
        super().__init__(Networks.AdColony, instance_name,
                         ad_unit, app_id, zone_id, status, instance_id, rate)


class AdColonyBidding(AdColonyBase):
    """AdColony Bidding instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: AdColony App ID
        :type app_id: str
        :param zone_id: AdColony Zone ID
        :type zone_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, zone_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):
        super().__init__(Networks.AdColonyBidding, instance_name,
                         ad_unit, app_id, zone_id, status, instance_id, rate)


class AdMobInstance(InstanceConfig):
    """AdMob instance

    :param instance_name: Name for the instance
    :type instance_name: str
    :param ad_unit:  Ad Unit that the instance will be used with
    :type ad_unit: AdUnits
    :param app_id: AdMob App ID
    :type app_id: str
    :param ad_unit_id: AdMob AdUnit ID
    :type ad_unit_id: str
    :param status: Instance is turned on or off, defaults to True
    :type status: bool, optional
    :param instance_id: instance id of the instance for update request, defaults to -1
    :type instance_id: int, optional
    :param rate: instance rate, defaults to None
    :type rate: float, optional
    """

    _app_id: str
    _ad_unit_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, ad_unit_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):
        super().__init__(Networks.AdMob, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._ad_unit_id = ad_unit_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_ad_unit_id(self):  # pylint: disable=missing-function-docstring
        return self._ad_unit_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {'appId': self.get_app_id()}

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['adUnitId'] = self.get_ad_unit_id()
        return obj


class AdManager(InstanceConfig):
    """Ad Manager instance

    :param instance_name: Name for the instance
    :type instance_name: str
    :param ad_unit:  Ad Unit that the instance will be used with
    :type ad_unit: AdUnits
    :param app_id: AdManager App ID
    :type app_id: str
    :param ad_unit_id: AdManager Ad Unit ID
    :type ad_unit_id: str
    :param status: Instance is turned on or off, defaults to True
    :type status: bool, optional
    :param instance_id: instance id of the instance for update request, defaults to -1
    :type instance_id: int, optional
    :param rate: instance rate, defaults to None
    :type rate: float, optional
    """
    _app_id: str
    _ad_unit_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, ad_unit_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):

        super().__init__(Networks.AdManager, instance_name,
                         ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._ad_unit_id = ad_unit_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_ad_unit_id(self):  # pylint: disable=missing-function-docstring
        return self._ad_unit_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {'appId': self.get_app_id()}

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['adUnitId'] = self.get_ad_unit_id()
        return obj


class AmazonInstance(InstanceConfig):
    """Amazon Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_key: Amazon Application Key
        :type app_key: str
        :param ec: Amazon EC
        :type ec: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_key: str
    _ec: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_key: str, ec: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Amazon, instance_name, ad_unit, status, instance_id, rate)
        self._app_key = app_key
        self._ec = ec

    def get_app_key(self):  # pylint: disable=missing-function-docstring
        return self._app_key

    def get_ec(self):  # pylint: disable=missing-function-docstring
        return self._ec

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {'appKey': self.get_app_key()}

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['ec'] = self.get_ec()
        return obj


class ApplovinInstance(InstanceConfig):
    """Applovin Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param sdk_key: Applovin SDK Key
        :type sdk_key: str
        :param zone_id: Applovin Zone ID
        :type zone_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _sdk_key: str
    _zone_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, sdk_key: str, zone_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):

        super().__init__(Networks.AppLovin, instance_name, ad_unit, status, instance_id, rate)
        self._sdk_key = sdk_key
        self._zone_id = zone_id

    def get_zone_id(self):  # pylint: disable=missing-function-docstring
        return self._zone_id

    def get_sdk_key(self):  # pylint: disable=missing-function-docstring
        return self._sdk_key

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {'sdkKey': self.get_sdk_key()}

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['zone_id'] = self.get_zone_id()
        return obj


class ChartboostInstance(InstanceConfig):
    """Chartboost Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Charboost App ID
        :type app_id: str
        :param app_signature: Chartboost App Signature
        :type app_signature: str
        :param ad_location: Charboost Ad Location
        :type ad_location: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _app_signature: str
    _ad_location: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, app_signature: str,  # pylint: disable=too-many-arguments
                 ad_location: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Chartboost, instance_name,
                         ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._app_signature = app_signature
        self._ad_location = ad_location

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_app_signature(self):  # pylint: disable=missing-function-docstring
        return self._app_signature

    def get_ad_location(self):  # pylint: disable=missing-function-docstring
        return self._ad_location

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id(),
            'appSignature': self.get_app_signature()
        }

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['adLocation'] = self.get_ad_location()
        return obj


class CrossPromotionBidding(InstanceConfig):
    """Cross Promotion Bidding Instance"

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param traffic_id: Cross Promotion traffic ID
        :type traffic_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _traffic_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, traffic_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):

        super().__init__(Networks.CrossPromotionBidding,
                         instance_name, ad_unit, status, instance_id, rate)
        self._traffic_id = traffic_id

    def get_traffic_id(self):  # pylint: disable=missing-function-docstring
        return self._traffic_id

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['traffic_id'] = self.get_traffic_id()
        return obj


class CSJInstance(InstanceConfig):
    """CSJ Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: CSJ Application ID
        :type app_id: str
        :param slot_id: CSJ Slot ID
        :type slot_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _slot_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, slot_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):

        super().__init__(Networks.CSJ, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._slot_id = slot_id

    def get_slot_id(self):  # pylint: disable=missing-function-docstring
        return self._slot_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {'appID': self.get_app_id()}

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['slot_id'] = self.get_slot_id()
        return obj


class DirectDeals(InstanceConfig):
    """Direct Deals Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param traffic_id: Direct Deal Traffic ID
        :type traffic_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _traffic_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, traffic_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True,
                 instance_id: int = -1, rate: float = None):

        super().__init__(Networks.DirectDeals, instance_name,
                         ad_unit, status, instance_id, rate)
        self._traffic_id = traffic_id

    def get_traffic_id(self):  # pylint: disable=missing-function-docstring
        return self._traffic_id

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['traffic_id'] = self.get_traffic_id()
        return obj


class FacebookBase(InstanceConfig):
    """Facebook Base"""
    _app_id: str
    _user_access_token: str
    _placement_id: str

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, app_id: str, user_access_token: str,  # pylint: disable=too-many-arguments
                 placement_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):
        super().__init__(ad_source, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._user_access_token = user_access_token
        self._placement_id = placement_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_user_access_token(self):  # pylint: disable=missing-function-docstring
        return self._user_access_token

    def get_placement_id(self):  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id(),
            'userAccessToken': self.get_user_access_token()
        }

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['placement_id'] = self.get_placement_id()
        return obj


class FacebookInstance(FacebookBase):
    """Facebook Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Facebook App ID
        :type app_id: str
        :param user_access_token: Facebook User Access Token
        :type user_access_token: str
        :param placement_id: Facebook Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, user_access_token: str,  # pylint: disable=too-many-arguments
                 placement_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Facebook, instance_name, ad_unit, app_id,
                         user_access_token, placement_id, status, instance_id, rate)


class FacebookBidding(FacebookBase):
    """Facebook Bidding Instance

    :param instance_name: Name for the instance
    :type instance_name: str
    :param ad_unit:  Ad Unit that the instance will be used with
    :type ad_unit: AdUnits
    :param app_id: Facebook Application ID
    :type app_id: str
    :param user_access_token: Facebook User Access Token
    :type user_access_token: str
    :param status: Instance is turned on or off, defaults to True
    :type status: bool, optional
    :param instance_id: instance id of the instance for update request, defaults to -1
    :type instance_id: int, optional
    :param rate: instance rate, defaults to None
    :type rate: float, optional
    """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, user_access_token: str,  # pylint: disable=too-many-arguments
                 placement_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.FacebookBidding, instance_name, ad_unit,
                         app_id, user_access_token, placement_id, status, instance_id, rate)


class FyberInstance(InstanceConfig):
    """Fyber Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Fyber Application ID
        :type app_id: str
        :param ad_spot_id: Fyber Ad Spot ID
        :type ad_spot_id: str
        :param content_id: Fyber Content ID
        :type content_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _ad_spot_id: str
    _content_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, ad_spot_id: str,  # pylint: disable=too-many-arguments
                 content_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Fyber, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._ad_spot_id = ad_spot_id
        self._content_id = content_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_ad_spot_id(self):  # pylint: disable=missing-function-docstring
        return self._ad_spot_id

    def get_content_id(self):  # pylint: disable=missing-function-docstring
        return self._content_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id()
        }

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['adSoptId'] = self.get_ad_spot_id()
        obj['contentId'] = self.get_content_id()
        return obj


class HyperMXInstance(InstanceConfig):
    """HyperMXInstance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param placement_id: HyperMX Placement ID
        :type placement_id: str
        :param distributor_id: HyperMX Distributor Id
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _distributor_id: str
    _placement_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, placement_id: str,  # pylint: disable=too-many-arguments
                 distributor_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.HyperMX, instance_name, ad_unit, status, instance_id, rate)
        self._distributor_id = distributor_id
        self._placement_id = placement_id

    def get_distributor_id(self):  # pylint: disable=missing-function-docstring
        return self._distributor_id

    def get_placement_id(self):  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'distributorId': self.get_distributor_id()
        }

    def get_object(self) -> dict:
        obj = super().get_object()
        obj['placementId'] = self.get_placement_id()
        return obj


class InMobiBase(InstanceConfig):
    """InMobi Base"""
    _placement_id: str

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, placement_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(ad_source, instance_name, ad_unit, status, instance_id, rate)
        self._placement_id = placement_id

    def get_placement_id(self):  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_object(self) -> dict:
        obj = super().get_object()
        obj['placementId'] = self.get_placement_id()
        return obj


class InMobiInstance(InMobiBase):
    """InMobi Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param placement_id: InMobi Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, placement_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.InMobi, instance_name,
                         ad_unit, placement_id, status, instance_id, rate)


class InMobiBidding(InMobiBase):
    """InMobi Bidding Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param placement_id: InMobi Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, placement_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.InMobiBidding, instance_name,
                         ad_unit, placement_id, status, instance_id, rate)


class LiftoffInstance(InstanceConfig):
    """Liftoff Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: LiftOff Application ID
        :type app_id: str
        :param ad_unit_id: LiftOff Ad Unit ID
        :type ad_unit_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _ad_unit_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, ad_unit_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.LiftOff, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._ad_unit_id = ad_unit_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_ad_unit_id(self):  # pylint: disable=missing-function-docstring
        return self._ad_unit_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id()
        }

    def get_object(self) -> dict:
        obj = super().get_object()
        obj['adUnitId'] = self.get_ad_unit_id()
        return obj


class MaioInstance(InstanceConfig):
    """Maio Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit: Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Maio App ID
        :type app_id: str
        :param media_id: Maio Media ID
        :type media_id: str
        :param zone_id: Maio ZoneID
        :type zone_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _media_id: str
    _zone_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, media_id: str,  # pylint: disable=too-many-arguments
                 zone_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Maio, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._media_id = media_id
        self._zone_id = zone_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_media_id(self):  # pylint: disable=missing-function-docstring
        return self._media_id

    def get_zone_id(self):  # pylint: disable=missing-function-docstring
        return self._zone_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id()
        }

    def get_object(self) -> dict:
        obj = super().get_object()
        obj['zoneId'] = self.get_zone_id()
        obj['mediaId'] = self.get_media_id()
        return obj


class MediaBrixInstance(InstanceConfig):
    """MediaBrix Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: MediaBrix App ID
        :type app_id: str
        :param reporting_property: MediaBrix Reporting property
        :type reporting_property: str
        :param zone: MediaBrix Zone
        :type zone: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    _app_id: str
    _reporting_property: str
    _zone: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, reporting_property: str,  # pylint: disable=too-many-arguments
                 zone: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):
        super().__init__(Networks.MediaBrix, instance_name,
                         ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._reporting_property = reporting_property
        self._zone = zone

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_reporting_property(self):  # pylint: disable=missing-function-docstring
        return self._reporting_property

    def get_zone(self):  # pylint: disable=missing-function-docstring
        return self._zone

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id(),
            'reportingProperty': self.get_reporting_property()
        }

    def get_object(self):  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['zone'] = self.get_zone()
        return obj


class MyTarget(InstanceConfig):
    """MyTarget Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param slot_id: MyTarget Slot ID
        :type slot_id: str
        :param placement_id: MyTarget Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _slot_id: str
    _placement_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, slot_id: str,  # pylint: disable=too-many-arguments
                 placement_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.MyTarget, instance_name, ad_unit, status, instance_id, rate)
        self._slot_id = slot_id
        self._placement_id = placement_id

    def get_slot_id(self):  # pylint: disable=missing-function-docstring
        return self._slot_id

    def get_placement_id(self):  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_object(self) -> dict:
        obj = super().get_object()
        obj['slotId'] = self.get_slot_id()
        obj['PlacementID'] = self.get_placement_id()
        return obj


class TapJoyBase(InstanceConfig):
    """TapJoy Instance"""
    _sdk_key: str
    _api_key: str
    _placement_name: str

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, sdk_key: str, api_key: str,  # pylint: disable=too-many-arguments
                 placement_name: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):
        super().__init__(ad_source, instance_name, ad_unit, status, instance_id, rate)
        self._sdk_key = sdk_key
        self._api_key = api_key
        self._placement_name = placement_name

    def get_sdk_key(self):  # pylint: disable=missing-function-docstring
        return self._sdk_key

    def get_api_key(self):  # pylint: disable=missing-function-docstring
        return self._api_key

    def get_placement_name(self):  # pylint: disable=missing-function-docstring
        return self._placement_name

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'sdkKey': self.get_sdk_key(),
            'apiKey': self.get_api_key()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['placementName'] = self.get_placement_name()
        return obj


class TapJoyInstance(TapJoyBase):
    """TapJoy Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param sdk_key: TapJoy SDK Key
        :type sdk_key: str
        :param api_key: TapJoy API Key
        :type api_key: str
        :param placement_name: TapJoy Placement Name
        :type placement_name: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, sdk_key: str, api_key: str,  # pylint: disable=too-many-arguments
                 placement_name: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.TapJoy, instance_name, ad_unit,
                         sdk_key, api_key, placement_name, status, instance_id, rate)


class TapJoyBidding(TapJoyBase):
    """TapJoy Bidding Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param sdk_key: TapJoy SDK Key
        :type sdk_key: str
        :param api_key: TapJoy API Key
        :type api_key: str
        :param placement_name: TapJoy Placement Name
        :type placement_name: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, sdk_key: str, api_key: str,  # pylint: disable=too-many-arguments
                 placement_name: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.TapJoyBidding, instance_name, ad_unit,
                         sdk_key, api_key, placement_name, status, instance_id, rate)


class PangleBase(InstanceConfig):
    """Pangle Base Instance"""
    _app_id: str
    _slot_id: str

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, app_id: str, slot_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):
        super().__init__(ad_source, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._slot_id = slot_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_slot_id(self):  # pylint: disable=missing-function-docstring
        return self._slot_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appID': self.get_app_id()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['slotID'] = self.get_slot_id()
        return obj


class PangleInstance(PangleBase):
    """Pangle Instance
        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Pangle App ID
        :type app_id: str
        :param slot_id: Pangle Slot ID
        :type slot_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, slot_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Pangle, instance_name, ad_unit,
                         app_id, slot_id, status, instance_id, rate)


class PangleBidding(PangleBase):
    """Pangle Bidding Instance

    :param instance_name: Name for the instance
    :type instance_name: str
    :param ad_unit:  Ad Unit that the instance will be used with
    :type ad_unit: AdUnits
    :param app_id: Pangle App ID
    :type app_id: str
    :param slot_id: Pangle Slot ID
    :type slot_id: str
    :param status: Instance is turned on or off, defaults to True
    :type status: bool, optional
    :param instance_id: instance id of the instance for update request, defaults to -1
    :type instance_id: int, optional
    :param rate: instance rate, defaults to None
    :type rate: float, optional
    """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, slot_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.PangleBidding, instance_name,
                         ad_unit, app_id, slot_id, status, instance_id, rate)


class UnityAdsInstance(InstanceConfig):
    """Unity Ads Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param source_id: Unity Source ID
        :type source_id: str
        :param zone_id: Unity Zone ID
        :type zone_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _source_id: str
    _zone_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, source_id: str, zone_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.UnityAds, instance_name, ad_unit, status, instance_id, rate)
        self._source_id = source_id
        self._zone_id = zone_id

    def get_source_id(self):  # pylint: disable=missing-function-docstring
        return self._source_id

    def get_zone_id(self):  # pylint: disable=missing-function-docstring
        return self._zone_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'sourceId': self.get_source_id()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['zoneId'] = self.get_zone_id()
        return obj


class SmaatoInstance(InstanceConfig):
    """Smaato Bidding Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param application_name: Smaato Application Name
        :type application_name: str
        :param ad_space_id: Smaato Ad Space ID
        :type ad_space_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _application_name: str
    _ad_space_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, application_name: str, ad_space_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Smaato, instance_name, ad_unit, status, instance_id, rate)
        self._application_name = application_name
        self._ad_space_id = ad_space_id

    def get_application_name(self):  # pylint: disable=missing-function-docstring
        return self._application_name

    def get_ad_space_id(self):  # pylint: disable=missing-function-docstring
        return self._ad_space_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'applicationName': self.get_application_name()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['adspaceID'] = self.get_ad_space_id()
        return obj


class SnapInstance(InstanceConfig):
    """Snap Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Snap Application ID
        :type app_id: str
        :param slot_id: Snap Slot ID
        :type slot_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _slot_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, slot_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Snap, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._slot_id = slot_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_slot_id(self):  # pylint: disable=missing-function-docstring
        return self._slot_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'AppId': self.get_app_id()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['SlotID'] = self.get_slot_id()
        return obj


class SuperAwesomeInstance(InstanceConfig):
    """SuperAwesome Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: SuperAwesome Application ID
        :type app_id: str
        :param placement_id: SuperAwesome Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _placement_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, placement_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.SuperAwesome, instance_name,
                         ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._placement_id = placement_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_placement_id(self):  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['placementId'] = self.get_placement_id()
        return obj


class TencentInstance(InstanceConfig):
    """Tencent Instance
        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Tencent Application ID
        :type app_id: str
        :param placement_id: Tencent Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _placement_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, placement_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Tencent, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._placement_id = placement_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_placement_id(self):  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'appId': self.get_app_id()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['placementId'] = self.get_placement_id()
        return obj


class YahooBidding(InstanceConfig):
    """Yahoo Bidding Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Yahoo Application ID
        :type app_id: str
        :param site_id: Yahoo Site ID
        :type site_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """
    _app_id: str
    _site_id: str

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, site_id: str,  # pylint: disable=too-many-arguments
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.YahooBidding, instance_name,
                         ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._site_id = site_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_site_id(self):  # pylint: disable=missing-function-docstring
        return self._site_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'siteId': self.get_app_id()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['placementId'] = self.get_site_id()
        return obj


class VungleBase(InstanceConfig):
    """Vungle Base"""
    _app_id: str
    _reporting_api_id: str
    _placement_id: str

    def __init__(self, ad_source: Networks, instance_name: str, ad_unit: AdUnits, app_id: str, reporting_api_id: str,  # pylint: disable=too-many-arguments
                 placement_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):
        super().__init__(ad_source, instance_name, ad_unit, status, instance_id, rate)
        self._app_id = app_id
        self._reporting_api_id = reporting_api_id
        self._placement_id = placement_id

    def get_app_id(self):  # pylint: disable=missing-function-docstring
        return self._app_id

    def get_reporting_api_id(self):  # pylint: disable=missing-function-docstring
        return self._reporting_api_id

    def get_placement_id(self):  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_app_data_obj(self):  # pylint: disable=missing-function-docstring
        return {
            'AppID': self.get_app_id(),
            'reportingAPIId': self.get_reporting_api_id()
        }

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        obj = super().get_object()
        obj['PlacementId'] = self.get_placement_id()
        return obj


class VungleInstance(VungleBase):
    """Vungle Instance

        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Vungle Application ID
        :type app_id: str
        :param reporting_api_id: Vungle Reporting API ID
        :type reporting_api_id: str
        :param placement_id: Vungle Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, reporting_api_id: str,  # pylint: disable=too-many-arguments
                 placement_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.Vungle, instance_name, ad_unit, app_id,
                         reporting_api_id, placement_id, status, instance_id, rate)


class VungleBidding(VungleBase):
    """Vungle Bidding Instance
        :param instance_name: Name for the instance
        :type instance_name: str
        :param ad_unit:  Ad Unit that the instance will be used with
        :type ad_unit: AdUnits
        :param app_id: Vungle Application ID
        :type app_id: str
        :param reporting_api_id: Vungle Reporting API ID
        :type reporting_api_id: str
        :param placement_id: Vungle Placement ID
        :type placement_id: str
        :param status: Instance is turned on or off, defaults to True
        :type status: bool, optional
        :param instance_id: instance id of the instance for update request, defaults to -1
        :type instance_id: int, optional
        :param rate: instance rate, defaults to None
        :type rate: float, optional
        """

    def __init__(self, instance_name: str, ad_unit: AdUnits, app_id: str, reporting_api_id: str,  # pylint: disable=too-many-arguments
                 placement_id: str,
                 status: bool = True, instance_id: int = -1, rate: float = None):

        super().__init__(Networks.VungleBidding, instance_name, ad_unit,
                         app_id, reporting_api_id, placement_id, status, instance_id, rate)
