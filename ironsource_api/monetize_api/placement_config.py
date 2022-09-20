"""
Module for creating placements object
"""
import logging

from . import AdUnits


class Capping():
    """
    Capping Class
    """
    _enabled: bool
    _limit: int
    _interval: str

    def __init__(self, limit: int, interval: str, enabled: bool):
        """Capping Class

        :param limit: Capping limit (max 1000).
        :type limit: int
        :param interval: Capping interval: 'd' - days or 'h' - hours
        :type interval: str
        :param enabled: True is enabled, False is disabled.
        :type enabled: bool
        :raises TypeError: When wrong type was set
        :raises ValueError: when limit or interval values are wrong
        """
        if not isinstance(enabled, bool):
            raise TypeError(
                f"enabled must be type boolean, not {type(enabled)}.")

        if limit > 1000:
            logging.warning(
                'limit is greater than 1000, it will be reduced to 1000')
            limit = 1000

        if interval not in ['d', 'h']:
            raise ValueError('interval must be `d` for days or `h` for hours')

        self._enabled = enabled
        self._limit = limit
        self._interval = interval

    def get_enabled(self) -> bool:  # pylint: disable=missing-function-docstring
        return self._enabled

    def get_limit(self) -> int:  # pylint: disable=missing-function-docstring
        return self._limit

    def get_interval(self) -> str:  # pylint: disable=missing-function-docstring
        return self._interval

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        return {'enabled': 1 if self.get_enabled() else 0,
                'cappingLimit': self.get_limit(),
                'cappingInterval': self.get_interval()}


class Pacing():
    """Pacing Class
    """
    _enabled: bool
    _minutes: float

    def __init__(self, minutes: float, enabled: bool):
        """_summary_

        :param minutes: Minimum gap in minutes between ad delivery (max 1000).
        :type minutes: float
        :param enabled: True is enabled, False is disabled.
        :type enabled: bool
        :raises TypeError: when enabled type is wrong.
        """
        if not isinstance(enabled, bool):
            raise TypeError(
                f"enabled must be type boolean, not {type(enabled)}.")
        if minutes > 1000:
            logging.warning(
                'minutes is greater than 1000, it will be reduced to 1000')
            minutes = 1000

        self._enabled = enabled
        self._minutes = minutes

    def get_enabled(self) -> bool:  # pylint: disable=missing-function-docstring
        return self._enabled

    def get_minutes(self) -> int:  # pylint: disable=missing-function-docstring
        return self._minutes

    def get_object(self) -> dict:  # pylint: disable=missing-function-docstring
        return {'enabled': 1 if self._enabled else 0,
                'pacingMinutes': self._minutes}


class Placement():  # pylint: disable=too-many-instance-attributes
    """
    Placement Object
    """

    _ad_unit: AdUnits
    _name: str
    _placement_id: int
    _ad_delivery: bool  # maybe should be renamed to enabled
    _item_name: str
    _reward_amount: int
    _capping: Capping
    _pacing: Pacing

    def __init__(
        self, ad_unit: AdUnits, ad_delivery: bool, name: str = None,
        placement_id: int = None, item_name: str = None, reward_amount: int = None,
        capping: Capping = None, pacing: Pacing = None
    ):
        """_summary_

        :param ad_unit:  Ad Unit for placement
        :type ad_unit: AdUnits
        :param ad_delivery: Ad delivery is turned on or off
        :type ad_delivery: bool
        :param name: placement unique name - only required for add_placements method
        :type name: str, optional
        :param placement_id: Placement unique identifier - not used for add_placements method
        :type placement_id: int, optional
        :param item_name: Reward name (max 30 chars) - rewardedVideo only
        :type item_name: str, optional
        :param reward_amount:  Amount of items to gift for a single ad view (max 2000000000) - rewardedVideo only
        :type reward_amount: int, optional
        :param capping: Capping for placement, defaults to None
        :type capping: Capping, optional
        :param pacing: pacing for placement, defaults to None
        :type pacing: Pacing, optional
        :raises ValueError:
        :raises TypeError:
        """

        if ad_unit not in [AdUnits.RewardedVideo, AdUnits.Interstitial, AdUnits.Banner]:
            raise ValueError(
                'ad_unit must be RewardedVideo, Interstitial, or Banner.')

        if not isinstance(ad_delivery, bool):
            raise TypeError(
                f"ad_delivery must be type boolean, not {type(ad_delivery)}.")

        if placement_id and not isinstance(placement_id, int):
            raise TypeError(
                f"placement_id must be type int, not {type(placement_id)}.")

        if name and not isinstance(name, str):
            raise TypeError(f"name must be type str, not {type(name)}.")

        if name and len(name) > 30:
            logging.warning(
                'length of name is greater than 30 chars, it will be trimmed')
            name = name[:29]

        # check logic here, why not placement_id?
        if ad_unit == AdUnits.RewardedVideo and (not item_name and not reward_amount) and not placement_id:
            raise ValueError(
                'item_name and reward_amount are mandatory when ad_unit is Rewarded Video')

        if item_name and len(item_name) > 30:
            logging.warning(
                'length of item_name is greater than 30 chars, it will be trimmed')
            item_name = item_name[:29]

        if reward_amount and reward_amount > 2000000000:
            logging.warning(
                'reward_amount is greater than 2000000000, it will be reduced')
            reward_amount = 2000000000

        if reward_amount and reward_amount % 1 > 0:
            logging.warning(
                'reward_amount should be int, it will be converted')
            reward_amount = int(round(reward_amount, 0))

        self._ad_unit = ad_unit
        self._name = name
        self._placement_id = placement_id
        self._ad_delivery = ad_delivery
        self._item_name = item_name
        self._reward_amount = reward_amount
        self._capping = capping
        self._pacing = pacing

    def get_ad_unit(self) -> AdUnits:  # pylint: disable=missing-function-docstring
        return self._ad_unit.value

    def get_name(self) -> str:  # pylint: disable=missing-function-docstring
        return self._name

    def get_placement_id(self) -> int:  # pylint: disable=missing-function-docstring
        return self._placement_id

    def get_ad_delivery(self) -> bool:  # pylint: disable=missing-function-docstring
        return self._ad_delivery

    def get_item_name(self) -> str:  # pylint: disable=missing-function-docstring
        return self._item_name

    def get_reward_amount(self) -> int:  # pylint: disable=missing-function-docstring
        return self._reward_amount

    def get_capping(self) -> dict:  # pylint: disable=missing-function-docstring
        return self._capping

    def get_pacing(self) -> dict:  # pylint: disable=missing-function-docstring
        return self._pacing

    def get_object(self) -> dict:  # pylint: disable=missing-class-docstring
        """
        returns formatted dictionary for api request
        :return: formatted dictionary for the placement
        :example:
        ```js
        {
            "appKey": "28cd2e39",
            "placements": [
                {
                "adUnit": "rewardedVideo", // rewardedVideo / interstitial / banner
                "name": "Main_Menu", // unique placement name
                "itemName": "coin", // the rewarded item name
                "rewardAmount": 25, // amount of rewards to give per ad view
                "capping": {
                        "enabled": 1, // 1 - enable capping, otherwise 0 (default: 1)
                    "cappingLimit": 3, // limit of ads per cappingInterval
                    "cappingInterval": "h" // interval type. "h"-hours, "d"-days (default: âdâ)
                }
                },
                {
                "adUnit": "banner",
                "name": "Custom_Pause",
                "pacing": {
                    "enabled": 0, // 1 - enable pacing, otherwise 0 (default: 1)
                    "pacingMinutes": 3, // pacing gap in minutes
                }
                }
            ]
        }
        ```
        """

        obj = {'adUnit': self.get_ad_unit(),
               'adDelivery': 1 if self.get_ad_delivery() else 0}

        if self._placement_id:
            obj['id'] = self.get_placement_id()

        if self._name:
            obj['name'] = self.get_name()

        if self._ad_unit == AdUnits.RewardedVideo:
            if self._item_name:
                obj['itemName'] = self.get_item_name()

            if self._reward_amount:
                obj['rewardAmount'] = self.get_reward_amount()

        if self._capping:
            obj['capping'] = self._capping.get_object()

        if self._pacing:
            obj['pacing'] = self._pacing.get_object()

        return obj
