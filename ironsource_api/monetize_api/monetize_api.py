"""IronSource Monetize API"""
import io
from typing import Iterable, Union
import json

from ironsource_api.base_api import BaseAPI

from . import AdUnits, Networks, Metrics, Breakdowns, Platform, AdUnitStatusMap
from .instance_config import InstanceConfig
from .mediation_group_priority import MediationGroupPriority, TierType
from .placement_config import Placement
from ..utils import execute_request_as_stream, execute_request

APP_API_URL = "https://platform.ironsrc.com/partners/publisher/applications/v6"

REPORT_URL = 'https://platform.ironsrc.com/partners/publisher/mediation/applications/v6/stats'

UAR_URL = 'https://platform.ironsrc.com/partners/userAdRevenue/v3'

ARM_URL = 'https://platform.ironsrc.com/partners/adRevenueMeasurements/v3'

MEDIATION_GROUP_MGMT_URL = 'https://platform.ironsrc.com/partners/publisher/mediation/management/v2'

INSTANCES_API_URL = 'https://platform.ironsrc.com/partners/publisher/instances/v1'

PLACEMENTS_URL = "https://platform.ironsrc.com/partners/publisher/placements/v1"


class MonetizeAPI(BaseAPI):
    """IronSource Monetize API"""




    ###########
    # Reporting
    ###########

    async def get_user_ad_revenue(self, date: str, application_key: str, stream: bool = False) -> Union[str, io.BytesIO]:
        """Get User Ad Revenue per application key
        :param date: - date in 'YYYY-MM-DD' format
        :type date: str
        :param application_key: - the application key for which user ad revenue is being requested
        :type application_key: str
        :param stream: - (Defaults - False) if true stream will be returned
        :type stream: bool
        :return: user ad revenue as string or byte stream
        """
        bearer_token = await self.get_bearer_auth()
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'date': date,
                'appKey': application_key,
                'reportType': 1
            }
        }
        response = await execute_request('get', url=UAR_URL, **options)
        if response.error_code != -1:
            raise Exception(
                "Error getting User Ad Revenue: {}".format(response.msg))

        try:
            json_res = json.loads(response.msg)
            if not stream:
                response = await execute_request(method='get', url=json_res['urls'][0], is_gzip=True)
                return response.msg

            response = execute_request_as_stream(
                url=json_res['urls'][0], is_gzip=True)
            return response

        except Exception as exception:
            raise Exception("Error getting User Ad Revenue: ") from exception

    async def get_impression_ad_revenue(self, date: str, application_key: str, stream: bool = False) -> Union[str, io.BytesIO]:
        """ Impressions level Ad Revenue per application
        :param date: - date in 'YYYY-MM-DD' format
        :type date: str
        :param application_key: - the application key for which user ad revenue is being requested
        :param application_key: str
        :param stream: - (Defaults - False) if true stream will be returned
        :type stream: bool
        :return: Impression level ad revenue as string or byte stream
        """
        bearer_token = await self.get_bearer_auth()
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'date': date,
                'appKey': application_key,
                'reportType': 1
            }
        }
        response = await execute_request('get', url=ARM_URL, **options)
        if response.error_code != -1:
            raise Exception(
                "Error getting Impression Ad Revenue: {}".format(response.msg))

        try:
            json_res = json.loads(response.msg)
            if not stream:
                response = await execute_request(method='get', url=json_res['urls'][0], is_gzip=True)
                return response.msg

            response = execute_request_as_stream(
                url=json_res['urls'][0], is_gzip=True)
            return response

        except Exception as exception:
            raise Exception(
                "Error getting Impression Ad Revenue: ") from exception

    # pylint: disable=unused-argument

    async def get_monetization_data(self, start_date: str, end_date: str, application_key: str = None,
                                    country: str = None, ad_units: AdUnits = None, ad_source: Networks = None,
                                    metrics: Iterable[Metrics] = None,
                                    breakdowns: Iterable[Breakdowns] = None) -> dict:
        """Get monetization reporting

        :param start_date: Report start date in the following format YYYY-MM-DD
        :type start_date: str
        :param end_date: Report end date in the following format YYYY-MM-DD
        :type end_date: str
        :param application_key: The application key for the report
        :type application_key: str, optional
        :param country: Country code in 2 letter country code,
                        as per `[ISO 3166-1 Alpha-2] <https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>`_.
        :type country: str, optional
        :param ad_units: Filter for specific AdUnit (RewardedVideo, Interstitial, Banner, Offerwall)
        :type ad_units: AdUnits, optional
        :param ad_source: Filter for specific Ad Source - network.
        :type ad_source: Networks, optional
        :param metrics: List of metrics see {@link https://developers.ironsrc.com/ironsource-mobile/air/supported-breakdown-metric/ | Metrics} see supported metrics and breakdowns
        :type metrics: Iterable[Metrics], optional
        :param breakdowns: List of breakdowns see {@link https://developers.ironsrc.com/ironsource-mobile/air/supported-breakdown-metric/ | Breakdowns} see supported breakdown and metrics
        :type breakdowns: Iterable[Breakdowns], optional
        :return: None if there was an error fetching monetization data or dictionary with the data
        """
        params = list(locals().items())
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'startDate': start_date,
                'endDate': end_date,
            }
        }
        for key, value in params:
            if key not in ['self', 'start_date', 'end_date'] and value:
                if key in ('breakdowns', 'metrics'):
                    options['params'][key] = []
                    for arr_val in value:
                        options['params'][key].append(arr_val.value)
                else:
                    if key == 'application_key':
                        new_key = 'appKey'
                    elif key == 'ad_units':
                        new_key = 'adUnits'
                        value = value.value
                    elif key == 'ad_source':
                        new_key = 'adSource'
                        value = value.value
                    else:
                        new_key = key

                    options['params'][new_key] = value

        res = await execute_request(method='get', url=REPORT_URL, **options)
        if res.error_code != -1:
            raise Exception('Error getting monetization data {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    #############
    # Application
    #############

    async def get_apps(self) -> dict:
        """Get list of apps

        :return: dictionary of list of apps from the account
        :rtype: dict
        """
        bearer_token = await self.get_bearer_auth()
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            }
        }
        response = await execute_request('get', url=APP_API_URL, **options)
        if response.error_code != -1:
            raise Exception('Error getting apps Error: {}, Error code:{}'.format(
                response.msg, response.error_code))
        return json.loads(response.msg)

    async def add_temporary_app(self, app_name: str, platform: Platform, coppa: bool, ad_unit_status: AdUnitStatusMap = None, ccpa: bool = None):
        """
        Adds a temporary app
        :param app_name: Application's name
        :type app_name: str
        :param platform: Application's platform from Platform
        :type platform: Platform
        :param coppa: The COPPA settings of the application (True/False)
        :type coppa: bool
        :param ad_unit_status:  Ad Unit status map see AdUnitStatusMap
        :type ad_unit_status: AdUnitStatusMap
        :param ccpa: The CCPA settings of the application (True/False)
        :type ccpa: bool
        :return: dict with new application key
        """
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            }
        }

        body = {
            'appName': app_name,
            'platform': platform.value,
            'coppa': 1 if coppa else 0
        }
        if ad_unit_status:
            body['adUnits'] = ad_unit_status.get_formatted_map()
        if ccpa:
            body['ccpa'] = 1 if ccpa else 0

        options['json'] = body

        res = await execute_request(method='post', url=APP_API_URL, **options)

        if res.error_code != -1:
            raise Exception('Error creating temporary app {} Error Code: {}'.format(
                res.msg, res.error_code))
        return json.loads(res.msg)

    async def add_app(self, app_store_url: str, taxonomy: str, coppa: bool, ad_unit_status: AdUnitStatusMap = None, ccpa: bool = None):
        """
        Adds application which is already live in the store
        :param app_store_url: iOS / Android app store url for the application
        :type app_store_url: str
        :param taxonomy: the application sub-genre - directory of valid labels: <https://developers.is.com/ironsource-mobile/air/taxonomy-2> \n
        :type taxonomy: str
        :param coppa: The COPPA settings of the application (True/False)
        :type coppa: bool
        :param ad_unit_status:  Ad Unit status map see AdUnitStatusMap
        :type ad_unit_status: AdUnitStatusMap
        :param ccpa: The CCPA settings of the application (True/False)
        :type ccpa: bool
        :return: dict with new application key
        """
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            }
        }

        body = {
            'storeUrl': app_store_url,
            'taxonomy': taxonomy,
            'coppa': 1 if coppa else 0
        }
        if ad_unit_status:
            body['adUnits'] = ad_unit_status.get_formatted_map()
        if ccpa:
            body['ccpa'] = 1 if ccpa else 0

        options['json'] = body

        res = await execute_request(method='post', url=APP_API_URL, **options)

        if res.error_code != -1:
            raise Exception('Error creating app {} Error Code: {}'.format(
                res.msg, res.error_code))
        return json.loads(res.msg)

    ###########
    # Instances
    ###########

    async def get_instances(self, application_key: str) -> dict:
        """Get Instances list for a given application key

        :param application_key: application key to get instances for
        :type application_key: str
        :return: return JSON format list of the instances
        :rtype: dict
        """
        bearer_token = await self.get_bearer_auth()
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'appKey': application_key
            }
        }
        response = await execute_request('get', url=INSTANCES_API_URL, **options)
        return json.loads(response.msg)

    async def add_instances(self, application_key: str, instances: Iterable[InstanceConfig]):
        """
        Adds new instances to an app
        :param application_key: Application Key to add instance to.
        :type application_key: str
        :param instances:  List of InstanceConfigs to be add.
        :type instances: Iterable[InstanceConfig]
        :return: dict with all the instances of the app
        """
        bearer_token = await self.get_bearer_auth()
        body = {
            'appKey': application_key,
            'configurations': {

            }
        }

        instance: InstanceConfig
        for instance in instances:
            if not instance.get_ad_source() in body['configurations']:
                body['configurations'][instance.get_ad_source()] = {
                    'appConfig': instance.get_app_data_obj()
                } if instance.get_app_data_obj() else {}

            if not instance.get_instance_ad_unit() in body['configurations'][instance.get_ad_source()]:
                body['configurations'][instance.get_ad_source(
                )][instance.get_instance_ad_unit()] = []

            body['configurations'][instance.get_ad_source()][instance.get_instance_ad_unit()].append(
                instance.get_object())

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'json': body
        }

        res = await execute_request(method='post', url=INSTANCES_API_URL, **options)

        if res.error_code != -1:
            raise Exception('Error creating adding instances {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def delete_instance(self, application_key: str, instance_id: int):
        """
        Deletes instance from application
        :param application_key: Application key to delete instance from
        :type application_key: str
        :param instance_id: instance id to delete
        :type instance_id: int
        :return: return list of all instances belongs to the ap
        """
        bearer_token = await self.get_bearer_auth()
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'appKey': application_key,
                'instanceId': instance_id
            }
        }

        res = await execute_request(method='delete', url=INSTANCES_API_URL, **options)

        if res.error_code != -1:
            raise Exception('Error creating deleting instance {} error:{} Error Code: {}'.format(instance_id, res.msg,
                                                                                                 res.error_code))

        return json.loads(res.msg)

    # pylint: disable=duplicate-code
    async def update_instances(self, application_key: str, instances: Iterable[InstanceConfig]):
        """
        Updates instances for an application
        :param application_key: Application key to update instances for
        :type application_key: str
        :param instances: list of instances to update (instance must contain instance id)
        :type instances: Iterable[InstanceConfig]
        :return: list of all instances
        """
        bearer_token = await self.get_bearer_auth()
        body = {
            'appKey': application_key,
            'configurations': {

            }
        }
        instance: InstanceConfig
        for instance in instances:
            if not instance.get_ad_source() in body['configurations']:
                body['configurations'][instance.get_ad_source()] = {
                    'appConfig': instance.get_app_data_obj()
                } if instance.get_app_data_obj() else {}

            if not instance.get_instance_ad_unit() in body['configurations'][instance.get_ad_source()]:
                body['configurations'][instance.get_ad_source(
                )][instance.get_instance_ad_unit()] = []

            instance_config = instance.get_object()
            if instance.get_instance_id() != -1:
                instance_config.update(
                    {'instanceId': instance.get_instance_id()})

            body['configurations'][instance.get_ad_source(
            )][instance.get_instance_ad_unit()].append(instance_config)

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'json': body
        }

        res = await execute_request(method='put', url=INSTANCES_API_URL, **options)

        if res.error_code != -1:
            raise Exception('Error creating updating instances {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    ##################
    # Mediation Groups
    ##################

    async def get_mediation_groups(self, application_key: str):
        """
        returns mediation groups for an application
        :param application_key: application key to fetch mediation groups
        :type application_key: str
        :return: list of mediation groups
        """
        bearer_token = await self.get_bearer_auth()
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'appKey': application_key
            }
        }

        res = await execute_request(method='get', url=MEDIATION_GROUP_MGMT_URL, **options)
        if res.error_code != -1:
            raise Exception('Error getting mediation groups {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def create_mediation_group(
        self, application_key: str, ad_unit: AdUnits, group_name: str,
        group_countries: Iterable[str],
        group_position: int = None,
        group_segment: int = None,
        ad_source_priority: MediationGroupPriority = None
    ):
        """Creates new mediation group for an application

        :param application_key: Application key to create new mediation group for
        :type application_key: str
        :param ad_unit: Ad unit to create mediation group for (see AdUnits)
        :type ad_unit: AdUnits
        :param group_name: Group's name
        :type group_name: str
        :param group_countries: List of group countries in [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
        :type group_countries: Iterable[str]
        :param group_position: Position of the group in the groups list, defaults to None
        :type group_position: int, optional
        :param group_segment:  Segment ID attached to the group, defaults to None
        :type group_segment: int, optional
        :param ad_source_priority: AdSource and their priority in the group (see MediationGroupPriority), defaults to None
        :type ad_source_priority: MediationGroupPriority, optional
        :raises Exception: When API error occurs
        :return: list of groups belongs to the app in json format
        :rtype: dict
        """

        body = {
            'appKey': application_key,
            'adUnit': ad_unit.value,
            'groupCountries': group_countries,
            'groupName': group_name
        }
        if group_position:
            body['groupPosition'] = group_position
        if group_segment:
            body['groupSegments'] = group_segment
        if ad_source_priority and ad_source_priority.get_bidders():
            group_tiers = ad_source_priority.get_tiers()
            for group_tier in group_tiers:
                if group_tier.get_tier_type() == TierType.OPTIMIZED:
                    raise Exception(
                        'Optimized Tier Type is not allowed with bidding.')
        body['adSourcePriority'] = ad_source_priority.get_object()

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'json': body
        }

        res = await execute_request(method='post', url=MEDIATION_GROUP_MGMT_URL, **options)
        if res.error_code != -1:
            raise Exception('Error creating Mediation Group {} Error Code: {}'.format(
                res.msg, res.error_code))
        return json.loads(res.msg)

    async def update_mediation_group(self, application_key: str, group_id: int, group_name: str = None,
                                     group_countries: Iterable[str] = None, group_segments: int = None,
                                     ad_source_priority: MediationGroupPriority = None):
        """
        Updates mediation group for an app
        :param application_key: Application key to update group for
        :type application_key: str
        :param group_id: Id of the group to update
        :type group_id: int
        :param group_name: (optional) - Group name
        :type group_name: str
        :param group_countries: (optional) -  List of group countries in
        [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
        :type group_countries: Iterable[str]
        :param group_segments: (optional) Group segment to update
        :param group_segments: int
        :param ad_source_priority: (optional) Ad Sources and their priority in the group (see MediationGroupPriority)
        :param ad_source_priority: MediationGroupPriority
        :return: List of group for the application after the changes
        """

        body = {
            'appKey': application_key,
            'groupId': group_id
        }
        if group_name:
            body['groupName'] = group_name
        if group_countries:
            body['groupCountries'] = group_countries
        if group_segments:
            body['groupSegments'] = group_segments

        if ad_source_priority and ad_source_priority.get_bidders():
            group_tiers = ad_source_priority.get_tiers()
            for group_tier in group_tiers:
                if group_tier.get_tier_type() == TierType.OPTIMIZED:
                    raise Exception(
                        'Optimized Tier Type is not allowed with bidding.')
        body['adSourcePriority'] = ad_source_priority.get_object()

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'json': body
        }

        res = await execute_request(method='put', url=MEDIATION_GROUP_MGMT_URL, **options)
        if res.error_code != -1:
            raise Exception(
                'Error updating Mediation Group id: {}, error: {} Error Code: {}'.format(group_id, res.msg,
                                                                                         res.error_code))
        return json.loads(res.msg)

    async def delete_mediation_group(self, application_key: str, group_id: int):
        """Deletes group for an application

        :param application_key: Application key to delete the group for
        :type application_key: str
        :param group_id: The group ID to delete
        :type group_id: int

        :return:  List of group for the application after the changes

        """
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'appKey': application_key,
                'groupId': group_id
            }
        }

        res = await execute_request(method='delete', url=MEDIATION_GROUP_MGMT_URL, **options)
        if res.error_code != -1:
            raise Exception('Error deleting Mediation Group id: {}, error: {} Error code: {}'.format(group_id, res.msg,
                                                                                                     res.error_code))
        return json.loads(res.msg)

    ############
    # Placements
    ############

    async def get_placements(self, application_key: str) -> dict:
        """Get list of placements

        :param application_key: Application key for placements
        :type application_key: str
        :return: json list of placements from the application
        :rtype: dict
        """
        bearer_token = await self.get_bearer_auth()
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'appKey': application_key
            }
        }
        response = await execute_request('get', url=PLACEMENTS_URL, **options)
        if response.error_code != -1:
            raise Exception('Error getting placements Error: {}, Error code:{}'.format(
                response.msg, response.error_code))
        return json.loads(response.msg)

    async def add_placements(self, application_key: str, placements: Iterable[Placement]) -> dict:
        """
        Create new placements, include capping and pacing setup, in your application account
        :param application_key: Application key of the app
        :type application_key: str
        :param placements: Array (list) of placements to be added/created
        :type placements: Iterable[Placement]
        :return json: placement identifier - This parameter is not shown in the ironSource platform and you can retrieve it using the get_placements method. You will need to use the id when editing/deleting placements.
        """
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            }
        }

        body = {
            'appKey': application_key,
            'placements': []
        }

        placement: Placement
        if len(placements) > 0:
            for placement in placements:
                if placement.get_name():
                    body['placements'].append(placement.get_object())
                else:
                    raise ValueError('New placements must have a name.')
        else:
            # itay, check this
            raise Exception('Length of placements list must be > 0.')

        options['json'] = body

        res = await execute_request(method='post', url=PLACEMENTS_URL, **options)

        if res.error_code != -1:
            raise Exception('Error creating placement {} Error Code: {}'.format(
                res.msg, res.error_code))
        return json.loads(res.msg)

    async def delete_placements(self, application_key: str, ad_unit: AdUnits, placement_id: int) -> str:
        """
        Archive existing placements in your applications
        :param application_key: Application key to delete placement from
        :type application_key: str
        :param ad_unit: ad unit name
        :type ad_unit: AdUnits
        :param placement_id: placement id to delete
        :type placement_id: int
        :return: return True if successful
        """
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'json': {
                'appKey': application_key,
                'adUnit': ad_unit.value,
                'id': placement_id
            }
        }

        res = await execute_request(method='delete', url=PLACEMENTS_URL, **options)

        if res.error_code != -1:
            raise Exception('Error deleting placement {} error:{} Error Code: {}'.format(placement_id, res.msg,
                                                                                         res.error_code))

        return res.msg

    # pylint: disable=duplicate-code

    async def update_placements(self, application_key: str, placements: Iterable[Placement]):
        """
        Updates placements for an application
        :param application_key: Application key to update placements for
        :type application_key: str
        :param placements: list of placements to update (placement must contain placement id)
        :type placements: Iterable[Placement]
        :return: True if successful
        """
        bearer_token = await self.get_bearer_auth()
        body = {
            'appKey': application_key,
            'placements': []
        }

        placement: Placement
        if len(placements) > 0:
            for placement in placements:
                if placement.get_placement_id():
                    body['placements'].append(placement.get_object())
                else:
                    raise ValueError(
                        'Updated placements must have a placement_id.')
        else:
            raise Exception('Length of placements list must be > 0.')

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'json': body
        }

        res = await execute_request(method='put', url=PLACEMENTS_URL, **options)

        if res.error_code != -1:
            raise Exception('Error creating updating placements {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)
