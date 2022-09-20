"""Module for Mediation Group Tier Priority"""
import enum
from logging import warning, error
from typing import Iterable
from pydash import arrays

from ironsource_api.monetize_api import Networks


class TierType(enum.Enum):
    """Enum representing different tier types for mediation group"""
    MANUAL = 'manual'
    SORT_BY_CPM = 'sortByCpm'
    OPTIMIZED = 'optimized'
    BIDDERS = 'bidding'


class MediationGroupTier():
    """Mediation Group Tier Object

    :param tier_type: Tier type for mediation group
    :type tier_type: TierType
    """
    _instances = []
    _tier_type: TierType = None

    def __init__(self, tier_type: TierType):
        self._tier_type = tier_type
        self._instances = []

    def add_instances(self, network: Networks, instance_id: int, rate: int = None,
                      position: int = None, capping: int = None):
        """
        Adds instance to group Tier
        :param network: a network from Networks
        :param instance_id: ID of the instance for the network (see MonetizeAPI().get_instances())
        :param rate: Optional: overrides the cpm of the instance with rate
        :param position: Optional: The position of the instance in the waterfall, only for Manual tier type
        :param capping: Optional: Set capping for the instance per session
        """
        current_pos = self._check_if_exists(instance_id, network)
        if self._tier_type != TierType.MANUAL:
            if current_pos > -1:
                warning('Instance already exists in the group')
                return
        elif current_pos == position:
            warning('The instance already exists with the same position')
            return

        if rate:
            instance_obj = {'providerName': network.value, 'instanceId': instance_id, 'rate': rate}
        else:
            instance_obj = {'providerName': network.value, 'instanceId': instance_id}

        if capping:
            instance_obj['capping'] = capping

        if self._tier_type != TierType.MANUAL:
            self._instances.append(instance_obj)
        else:
            arrays.splice(self._instances, 0, position, instance_obj)

    def get_instance_list(self) -> list:
        """
        Returns list of instances in the tier
        """
        return self._instances

    def remove_instance(self, network: Networks, instance_id: int):
        """
        Removes instance from the tier.
        :param network: The network of the instance to remove.
        :param instance_id: Instance ID to remove.
        """
        arrays.pop(self._instances, self._check_if_exists(instance_id, network))

    def _check_if_exists(self, instance_id: int, network: Networks):
        return arrays.find_index(self._instances,
                                 lambda obj: (obj['instanceId'] == instance_id and obj['providerName'] == network))

    def get_tier_type(self) -> TierType:
        """
        :return: the tier type of the group
        """
        return self._tier_type

    def get_object(self):
        """
        building tier object for sending to the API.
        """
        group_tier = {
            'instances': self._instances,
            'tierType': self._tier_type.value
        }
        return group_tier


class MediationGroupPriority():
    """
    Class representing a groups priority of tiers
    """
    _tier_array = [None, None, None]
    _bidders: MediationGroupTier = None

    def __init__(self):
        self._tier_array = [None, None, None]
        self._bidders = None

    def set_mediation_group_tier(self, group_tier: MediationGroupTier, position: int) -> bool:
        """
        sets group tier in specific place in the group (tier1, tier2, tier3)
        :param group_tier: MediationGroupTier to be added to the group tier list
        :param position: The Position of the tier (0-2), Ignored in case of bidding tier.
        :return: true upon successful addition of the tier to the group list.
        """
        if group_tier.get_tier_type() == TierType.BIDDERS:
            if self._bidders:
                warning('Replacing bidders list')
            self._bidders = group_tier
            return True

        if position > 2:
            error('Max number of tiers are 3, position must be between 0-2')
            raise Exception('Max number of tiers are 3, position must be between 0-2')

        val_obj = self._validate_tier(group_tier, position)
        if val_obj['position'] != -1:
            error('Some instances overlap between tiers: tier {} with instances {}'
                  .format(val_obj['position'] + 1, val_obj['list']))
            raise Exception('Some instances overlap between tiers: tier {} with instances {}'
                            .format(val_obj['position'] + 1, val_obj['list']))

        self._tier_array[position] = group_tier
        return True

    def remove_tier(self, position: int):
        """
        Removes tier from the group
        :param position: position of the tier to be removed (0-2)
        """
        if not self._tier_array[position]:
            warning('Tier{} is empty'.format(position + 1))
        self._tier_array[position] = None

    def remove_bidders(self):
        """
        Removes bidders from the group
        """
        if not self._bidders:
            warning('Bidders list is empty')
            return
        self._bidders = None

    def get_bidders(self):
        """
        Returns groups bidders list
        """
        return self._bidders

    def get_tiers(self) -> Iterable[any]:
        """
        Returns groups tiers list
        """
        return self._tier_array

    def get_object(self):
        """
        Creates and returns an object to send to the API call.
        :return: dict
        """
        med_group_priority = {
        }
        if self._bidders:
            med_group_priority['bidding'] = self._bidders.get_object()
        arrays.remove(self._tier_array, lambda obj: obj is None)

        for i in range(len(self._tier_array)):
            tier_obj = self._tier_array[i].get_object()
            med_group_priority['tier{}'.format(i + 1)] = tier_obj

        return med_group_priority

    def _validate_tier(self, group_tier: MediationGroupTier, position: int) -> dict:
        """
        Validates that the instances in the given tier do not exist already on another tier in the group
        :param group_tier: The tier to be check against
        :param position: The new position of the tier - We ignore comparison in that position
        :return: In case of duplicates instances returns an object with list of duplicates and tier position,
                 otherwise returns object with position of -1 and empty list.
        """
        for i in range(len(self._tier_array)):
            if i == position or not self._tier_array[i]:
                continue
            intersection_list = arrays.intersection_with(self._tier_array[i].get_instance_list(),
                                                         group_tier.get_instance_list(),
                                                         comparator=lambda a, b: a['instanceId'] == b['instanceId']
                                                                                 and a['providerName'] == b[
                                                                                     'providerName'])
            if len(intersection_list) > 0:
                return {position: i, list: intersection_list}

        return {'position': -1, 'list': []}
