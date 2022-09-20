"""Module for Creatives"""

from typing import Iterable
from . import CreativeType, UsageType
from ..utils import check_instance


class CreativeAsset():
    """Creative Asset for Creative usage

    :param asset_id: Asset ID for the creative Asset
    :type asset_id: int
    :param usage_type: Usage type of the creative
    :type usage_type: UsageType
    """
    _asset_id: int
    _usage_type: UsageType

    def __init__(self, asset_id: int, usage_type: UsageType):
        if check_instance(asset_id, int, 'asset_id'):
            self._asset_id = asset_id

        if check_instance(usage_type, UsageType, 'usage_type'):
            self._usage_type = usage_type
    # pylint: disable=missing-function-docstring
    def get_asset_id(self):
        return self._asset_id
    # pylint: disable=missing-function-docstring
    def get_usage_type(self):
        return self._usage_type
    # pylint: disable=missing-function-docstring
    def get_object(self):
        """
        :return: dict that represent the object
        """
        return {'usageType': self.get_usage_type(),
                'id': self.get_asset_id()}


class Creative():
    """Class that represents Creative

        :param name: Name of the creative
        :type name: str
        :param creative_type: Type of the creative.
        :type creative_type: CreativeType
        :param language: 2 letter e.g english=”EN”.
        :type language: str
        :param assets: List of CreativeAsset, defaults to []
        :type assets: Iterable[CreativeAsset], optional
        """
    _name: str
    _creative_type: CreativeType
    _language: str
    _assets: Iterable[CreativeAsset] = []
     # pylint: disable=dangerous-default-value
    def __init__(self, name: str, creative_type: CreativeType, language: str, assets: Iterable[CreativeAsset] = []):
        if check_instance(name, str, 'name'):
            self._name = name

        if check_instance(creative_type, CreativeType, 'creative_type'):
            self._creative_type = creative_type

        if check_instance(language, str, 'language') and len(language) == 2:
            self._language = language
        elif len(language) != 2:
            raise ValueError(
                "language must be length 2, not {}.".format(len(language)))

        if check_instance(assets, list, 'assets'):
            for creative_asset in assets:
                if not self.check_asset_compatible(creative_asset):
                    raise ValueError(
                        f"Asset usage type {creative_asset.get_usage_type()} is not compatible with creative type {self.get_creative_type}")
            self._assets = assets

    def check_asset_compatible(self,asset:CreativeAsset)->bool:
        """_summary_

        :param asset: Assets to check compatibility
        :type asset: CreativeAsset
        :return: True is compatible else False
        :rtype: bool
        """
        mandatory = self._creative_type.value['usage_types']['mandatory']
        optionals = self._creative_type.value['usage_types']['optional'] if 'optional' in self._creative_type.value['usage_types'] else []

        if asset.get_usage_type() in mandatory + optionals:
            return True
        return False

    def is_validate(self) -> bool:
        """Check if creative is valid
        :return: True if the creative is valid with all it's assets
        :rtype: bool
        """
        asset: CreativeAsset
        usage_types_used = []
        mandatory = self._creative_type.value['usage_types']['mandatory']
        for asset in self._assets:
            # test if each asset is class CreativeAsset
            if asset.get_usage_type() in mandatory:
                usage_types_used.append(asset.get_usage_type())
                mandatory.pop(mandatory.index(asset.get_usage_type()))
            elif asset.get_usage_type() in usage_types_used:
                raise ValueError("usage_type {} for creative_type {} has already been used.".format(
                    asset.get_usage_type(), self._creative_type))

        if len(mandatory) == 0:
            return True
        raise ValueError("Creative type {} is missing mandatory assets with usage_types: {}".format(
            self._creative_type.name, mandatory))
    # pylint: disable=missing-function-docstring
    def get_name(self):
        return self._name
    # pylint: disable=missing-function-docstring
    def get_creative_type(self):
        return self._creative_type
    # pylint: disable=missing-function-docstring
    def get_language(self):
        return self._language
    # pylint: disable=missing-function-docstring
    def get_assets(self):
        return self._assets

    def add_asset(self, asset: CreativeAsset):
        """Adds asset to creative
        :param asset: CreativeAsset to be added
        :type asset: CreativeAsset
        :raises ValueError: If Asset usage is wrong
        """
        if not self.check_asset_compatible(asset):
            raise ValueError(
                f"Asset usage type {asset.get_usage_type()} is not compatible with creative type {self.get_creative_type}")
        self._assets.append(asset)


    def get_object(self):
        """
        :return: return dict that represents the object
        """
        obj = {
            'name': self.get_name(),
            'type': self.get_creative_type().value['name'],
            'language': self.get_language()
        }

        assets = []
        asset: CreativeAsset
        for asset in self.get_assets():
            asset_obj = asset.get_object()
            asset_obj['usageType'] = asset_obj['usageType'].value
            assets.append(asset_obj)

        obj['assets'] = assets

        return obj
