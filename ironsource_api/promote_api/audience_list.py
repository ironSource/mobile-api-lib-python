"""Module for Audience List"""
import enum
from typing import Iterable, Union

from ironsource_api.promote_api import Platform

# pylint: disable=invalid-name
class AudienceListType(enum.Enum):
    """Enum for Audience List Types"""
    Suppression = 'suppression_static'
    Targeting = 'targeting'


class AudienceListMeta:
    """Create AudienceList Object

        :param name: Audience List name.
        :type name: str
        :param list_type: Audience List type. see AudienceListType.
        :type list_type: AudienceListType
        :param description: Audience List description.
        :type description: str
        :param bundle_id: Bundle id for the list, defaults to None
        :type bundle_id: str, optional
        :param platform: platform for the audience list. See Platform., defaults to None
        :type platform: Platform, optional
        """
    _name: str
    _type: AudienceListType
    _description: str
    _bundle_id: str
    _platform: Platform

    def __init__(self, name: str, list_type: AudienceListType, description: str, bundle_id: str = None,
                 platform: Platform = None):
        self._name = name
        self._type = list_type
        self._description = description
        self._bundle_id = bundle_id
        self._platform = platform

        if list_type == AudienceListType.Suppression:
            if not bundle_id:
                raise Exception('Bundle Id is required when using Suppression type list')
            if not platform:
                raise Exception('Platform is required when using Suppression type list')

    def to_object(self):
        """
        Returns dict for REST API
        :return:
        """
        obj = {
            'name': self._name,
            'type': self._type.value,
            'description': self._description
        }
        if self._type == AudienceListType.Suppression:
            obj['bundleId'] = self._bundle_id
            obj['platform'] = self._platform.value

        return obj


class AudienceListData:
    """
    Class representing Audience list data
    """
    _ids_to_add: Iterable[str] = []
    _ids_to_remove: Iterable[str] = []
    _device_list: Iterable[str] = []

    def __init__(self):
        self._ids_to_add = []
        self._ids_to_remove = []
        self._device_list = []

    def add_list_for_update(self, audience_list_id: str):
        """Add audience list id to the update list

        ::param audience_list_id: audience list id to update in string.
        :type audience_list_id: str
        """
        self._ids_to_add.append(audience_list_id)

    def add_list_for_remove(self, audience_list_id: str):
        """
        Add audience list id to the remove list
        :param audience_list_id: audience list id to remove in string.
        :type audience_list_id: str
        :return:
        """
        self._ids_to_remove.append(audience_list_id)

    def add_devices(self, devices: Union[str, list]):
        """
        Adds devices to the list
        :param devices: either a device in string or list of devices
        :type devices: Union[str, list]
        :return:
        """
        if isinstance(devices, str):
            self._device_list.append(devices)
        else:
            self._device_list = self._device_list + devices

    def to_object(self):
        """
        Returns dict for REST API
        :return:
        """
        obj = {'deviceIds': self._device_list}
        if self._ids_to_add:
            obj['addAudience'] = self._ids_to_add
        if self._ids_to_remove:
            obj['removeAudience'] = self._ids_to_remove
        return obj
