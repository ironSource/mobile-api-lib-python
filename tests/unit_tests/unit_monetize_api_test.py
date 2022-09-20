# pylint: disable=missing-module-docstring
from io import BytesIO
import unittest
from typing import Dict, List
from unittest.mock import call


from pytest_mock import MockerFixture
import pytest

from ironsource_api.ironsource_api import IronSourceAPI

from ironsource_api.monetize_api import AdUnitStatus, AdUnitStatusMap, AdUnits, Platform, Networks, Breakdowns, Metrics
from ironsource_api.monetize_api.instance_config import IronSourceInstance, VungleInstance
from ironsource_api.monetize_api.mediation_group_priority import MediationGroupPriority, MediationGroupTier, TierType
from ironsource_api.monetize_api.placement_config import Placement, Pacing, Capping
from ironsource_api.utils import ResponseInterface



ironsrc_api = IronSourceAPI()

ironsrc_api.set_credentials('TEST_USER',
                             'TEST_TOKEN',
                             'TEST_SECRET')

# pylint: disable=too-many-public-methods, missing-function-docstring,missing-class-docstring


@pytest.mark.asyncio
class Test_UnitTestsMonetizeAPI(unittest.IsolatedAsyncioTestCase):
    TEST_APP_NAME = 'Test_App_Name'
    TEST_APP_KEY = '1234abc'
    ironsource_instance_id = 1234
    mediation_group_id = 1234
    placement_id = 1234

    @pytest.fixture(autouse=True)
    def before_after_tests(self, mocker: MockerFixture):
        self.mocker = mocker
        mocker.patch(
            'ironsource_api.monetize_api.monetize_api.BaseAPI.get_bearer_auth', return_value='TOKEN')
        yield

    def get_mock_exec_req(self, msg):
        mocked_res = ResponseInterface()
        mocked_res.msg = msg
        mocked_res.error_code = -1
        mocked_req = self.mocker.patch(
            'ironsource_api.monetize_api.monetize_api.execute_request',
            return_value=mocked_res)

        return mocked_req

    @pytest.mark.asyncio
    async def test_unit_get_apps(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            }
        }
        res = await ironsrc_api.monetize_api().get_apps()
        mocked_req.assert_awaited_once_with(
            'get', url="https://platform.ironsrc.com/partners/publisher/applications/v6", **options)

    @pytest.mark.asyncio
    async def test_unit_add_app(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        ad_unit_status = AdUnitStatusMap()
        ad_unit_status[AdUnits.RewardedVideo] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Interstitial] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Offerwall] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Banner] = AdUnitStatus.Test

        res = await ironsrc_api.monetize_api().add_temporary_app(app_name=self.TEST_APP_NAME, platform=Platform.Android,
                                                                  coppa=False, ad_unit_status=ad_unit_status, ccpa=False)

        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                'appName': self.TEST_APP_NAME,
                'platform': 'Android',
                'coppa': 0,
                'adUnits': {
                    'rewardedVideo': 'Test',
                    'interstitial': 'Test',
                    'OfferWall': 'Test',
                    'banner': 'Test'
                }
            }
        }
        mocked_req.assert_called_once_with(
            method='post', url='https://platform.ironsrc.com/partners/publisher/applications/v6', **options)

    @pytest.mark.asyncio
    async def test_unit_add_live_app(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        ad_unit_status = AdUnitStatusMap()
        ad_unit_status[AdUnits.RewardedVideo] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Interstitial] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Offerwall] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Banner] = AdUnitStatus.Test
        taxonomy = 'Other Non-Gaming'

        res = await ironsrc_api.monetize_api().add_app(
            'https://play.google.com/store/apps/details?id=iron.web.jalepano.browser', taxonomy, False, ad_unit_status, False)

        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                'storeUrl': 'https://play.google.com/store/apps/details?id=iron.web.jalepano.browser',
                'taxonomy': 'Other Non-Gaming',
                'coppa': 0,
                'adUnits': {
                    'rewardedVideo': 'Test',
                    'interstitial': 'Test',
                    'OfferWall': 'Test',
                    'banner': 'Test'
                }
            }
        }
        mocked_req.assert_called_once_with(
            method='post', url='https://platform.ironsrc.com/partners/publisher/applications/v6', **options)

    @pytest.mark.asyncio
    async def test_unit_create_new_instances(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        ironsource_price_map: Dict[int, List[str]] = {10: ['US'], 5: ['IL']}

        ironsource_instance = IronSourceInstance(instance_name='TEST', ad_unit=AdUnits.RewardedVideo,
                                                 application_key=self.__class__.TEST_APP_KEY, status=False,
                                                 pricing=ironsource_price_map)
        vungle_instance = VungleInstance(instance_name='TEST', ad_unit=AdUnits.RewardedVideo, app_id='TEST',
                                         reporting_api_id='TEST', placement_id='TEST', status=True)

        res = await ironsrc_api.monetize_api().add_instances(self.__class__.TEST_APP_KEY,
                                                              [ironsource_instance, vungle_instance])

        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                "appKey": "1234abc",
                "configurations":
                {
                    "ironSource": {
                        "rewardedVideo": [
                            {"instanceName": "TEST",
                             "status": "inactive",
                             "pricing": [
                                 {"eCPM": 10, "country": ["US"]},
                                 {"eCPM": 5, "country": ["IL"]}
                             ]
                             }
                        ]
                    },
                    "Vungle": {
                        "appConfig": {
                            "AppID": "TEST", "reportingAPIId": "TEST"
                        },
                        "rewardedVideo": [{"instanceName": "TEST", "status": "active", "PlacementId": "TEST"}]}}}
        }
        mocked_req.assert_called_once_with(
            method='post', url="https://platform.ironsrc.com/partners/publisher/instances/v1", **options)

    @pytest.mark.asyncio
    async def test_unit_update_instances(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        ironsource_price_map: Dict[int, List[str]] = {7: ['US'], 5: ['IL']}

        ironsource_instance_update = IronSourceInstance(instance_name='TEST', ad_unit=AdUnits.RewardedVideo,
                                                        application_key=self.__class__.TEST_APP_KEY, status=False,
                                                        pricing=ironsource_price_map,
                                                        instance_id=self.__class__.ironsource_instance_id)
        ironsource_def_instance = IronSourceInstance(instance_name='Default', ad_unit=AdUnits.RewardedVideo,
                                                     application_key=self.__class__.TEST_APP_KEY, status=True,
                                                     instance_id=0)

        res = await ironsrc_api.monetize_api().update_instances(self.__class__.TEST_APP_KEY,
                                                                 [ironsource_instance_update, ironsource_def_instance])

        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                "appKey": "1234abc",
                "configurations": {
                    "ironSource": {
                        "rewardedVideo": [

                            {
                                "instanceId": 1234,
                                "instanceName": "TEST",
                                "status": "inactive",
                                "pricing": [
                                    {
                                        "eCPM": 7,
                                        "country": [
                                            "US"
                                        ]
                                    },
                                    {
                                        "eCPM": 5,
                                        "country": [
                                            "IL"
                                        ]
                                    }
                                ]
                            },
                            {
                                "instanceId": 0,
                                "status": "active",
                                "instanceName": "Default"
                            }
                        ]
                    }
                }
            }
        }
        mocked_req.assert_called_once_with(
            method='put', url='https://platform.ironsrc.com/partners/publisher/instances/v1', **options)

    @pytest.mark.asyncio
    async def test_unit_delete_instances(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        res = await ironsrc_api.monetize_api().delete_instance(self.__class__.TEST_APP_KEY,
                                                                self.__class__.ironsource_instance_id)
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'appKey': self.__class__.TEST_APP_KEY,
                'instanceId': self.__class__.ironsource_instance_id
            }
        }
        mocked_req.assert_called_once_with(
            method='delete', url='https://platform.ironsrc.com/partners/publisher/instances/v1', **options)

    @pytest.mark.asyncio
    async def test_unit_get_mediation_group(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'appKey': 'c90cab7d'
            }
        }
        res = await ironsrc_api.monetize_api().get_mediation_groups(application_key='c90cab7d')
        mocked_req.assert_called_once_with(
            method='get', url='https://platform.ironsrc.com/partners/publisher/mediation/management/v2', **options)

    @pytest.mark.asyncio
    async def test_unit_create_mediation_group(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                "appKey": "1234abc",
                "adUnit": "rewardedVideo",
                "groupName": "Test_Group_Automation",
                "groupCountries": [
                    "US",
                    "IL"
                ],
                "groupPosition": 1,
                "adSourcePriority": {
                    "tier1": {
                        "tierType": "manual",
                        "instances": [{
                            "providerName": "ironSource",
                            "instanceId": 0,
                            "rate": 10,
                            "capping": 2
                        }]
                    },
                    "tier2": {
                        "tierType": "sortByCpm",
                        "instances": [{
                            "providerName": "Vungle",
                            "instanceId": 0,
                            "rate": 4
                        }]
                    }
                }
            }
        }
        mediation_group_priority = MediationGroupPriority()
        tier1 = MediationGroupTier(tier_type=TierType.MANUAL)
        tier1.add_instances(network=Networks.IronSource,
                            instance_id=0, rate=10, position=1, capping=2)
        tier2 = MediationGroupTier(tier_type=TierType.SORT_BY_CPM)
        tier2.add_instances(network=Networks.Vungle,
                            instance_id=0, rate=4, position=1)

        mediation_group_priority.set_mediation_group_tier(
            group_tier=tier1, position=0)
        mediation_group_priority.set_mediation_group_tier(
            group_tier=tier2, position=1)

        res = await ironsrc_api.monetize_api().create_mediation_group(application_key=self.__class__.TEST_APP_KEY,
                                                                       ad_unit=AdUnits.RewardedVideo,
                                                                       group_name='Test_Group_Automation',
                                                                       group_countries=[
                                                                           'US', 'IL'],
                                                                       ad_source_priority=mediation_group_priority,
                                                                       group_position=1)

        mocked_req.assert_called_once_with(
            method='post', url='https://platform.ironsrc.com/partners/publisher/mediation/management/v2', **options)

    @pytest.mark.asyncio
    async def test_unit_update_mediation_group(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                "appKey": "1234abc",
                "groupName": "Test_Group_Automation_updated",
                "groupId": 1234,
                "groupCountries": [
                    "US"
                ],
                "adSourcePriority": {
                    "tier1": {
                        "tierType": "manual",
                        "instances": [{
                            "providerName": "ironSource",
                            "instanceId": 0,
                            "rate": 10,
                            "capping": 2
                        }]
                    },
                    "tier2": {
                        "tierType": "sortByCpm",
                        "instances": [{
                            "providerName": "Vungle",
                            "instanceId": 0,
                            "rate": 4
                        }]
                    },
                    "tier3": {
                        "tierType": "sortByCpm",
                        "instances": [{
                            "providerName": "ironSource",
                            "instanceId": 1234
                        }]
                    }
                }
            }}

        new_instance_id = 1234

        mediation_group_priority = MediationGroupPriority()
        tier1 = MediationGroupTier(TierType.MANUAL)
        tier1.add_instances(network=Networks.IronSource,
                            instance_id=0, rate=10, position=1, capping=2)
        tier2 = MediationGroupTier(tier_type=TierType.SORT_BY_CPM)
        tier2.add_instances(network=Networks.Vungle,
                            instance_id=0, rate=4, position=1)
        tier3 = MediationGroupTier(tier_type=TierType.SORT_BY_CPM)
        tier3.add_instances(network=Networks.IronSource,
                            instance_id=new_instance_id)

        mediation_group_priority.set_mediation_group_tier(
            group_tier=tier1, position=0)
        mediation_group_priority.set_mediation_group_tier(
            group_tier=tier2, position=1)
        mediation_group_priority.set_mediation_group_tier(
            group_tier=tier3, position=2)

        update_res = await ironsrc_api.monetize_api().update_mediation_group(
            application_key=self.__class__.TEST_APP_KEY, group_id=self.__class__.mediation_group_id,
            group_name='Test_Group_Automation_updated', group_countries=['US'], ad_source_priority=mediation_group_priority)

        mocked_req.assert_called_once_with(
            method='put', url='https://platform.ironsrc.com/partners/publisher/mediation/management/v2', **options)

    @pytest.mark.asyncio
    async def test_unit_delete_mediation_group(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'appKey': self.__class__.TEST_APP_KEY,
                'groupId': self.__class__.mediation_group_id
            }
        }

        res = await ironsrc_api.monetize_api().delete_mediation_group(application_key=self.__class__.TEST_APP_KEY,
                                                                       group_id=self.__class__.mediation_group_id)

        mocked_req.assert_called_once_with(
            method='delete', url='https://platform.ironsrc.com/partners/publisher/mediation/management/v2', **options)

    @pytest.mark.asyncio
    async def test_unit_report_with_demo_data(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'startDate': '2020-01-01',
                'endDate': '2020-01-01'
            }
        }

        res = await ironsrc_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01')
        mocked_req.assert_called_once_with(
            method='get', url='https://platform.ironsrc.com/partners/publisher/mediation/applications/v6/stats', **options)

    @pytest.mark.asyncio
    async def test_unit_report_demo_data_app_breakdown(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'startDate': '2020-01-01',
                'endDate': '2020-01-01',
                'breakdowns': [
                    'app',
                    'country'
                ],
                'adUnits': 'interstitial',
                'adSource': 'ironSource',
                'metrics': ['impressions', 'clicks'],
                'appKey': 'abcd1234',
                'country': 'US'
            }
        }
        res = await ironsrc_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='abcd1234',
                                                                      ad_units=AdUnits.Interstitial,
                                                                      ad_source=Networks.IronSource,
                                                                      country='US',
                                                                      metrics=[
                                                                          Metrics.impressions, Metrics.clicks],
                                                                      breakdowns=[Breakdowns.Application, Breakdowns.Country])

        mocked_req.assert_called_once_with(
            method='get', url='https://platform.ironsrc.com/partners/publisher/mediation/applications/v6/stats', **options)

    @pytest.mark.asyncio
    async def test_unit_create_new_placements(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                "appKey": "1234abc",
                "placements": [{
                    "adUnit": "rewardedVideo",
                    "adDelivery": 1,
                    "name": "RV_TEST_PLACEMENT",
                    "itemName": "Test",
                    "rewardAmount": 1000,
                    "capping": {
                        "enabled": 1,
                        "cappingLimit": 100,
                        "cappingInterval": "h"
                    },
                    "pacing": {
                        "enabled": 1,
                        "pacingMinutes": 100
                    }
                },
                    {
                    "adUnit": "banner",
                    "adDelivery": 0,
                    "name": "Banner_TEST_PLACEMENT"
                }
                ]
            }
        }

        rv_placement = Placement(ad_unit=AdUnits.RewardedVideo, ad_delivery=True, name='RV_TEST_PLACEMENT',
                                 item_name='Test', reward_amount=1000, capping=Capping(limit=100, interval='h', enabled=True), pacing=Pacing(100, True))
        banner_placement = Placement(
            ad_unit=AdUnits.Banner, ad_delivery=False, name='Banner_TEST_PLACEMENT')

        res = await ironsrc_api.monetize_api().add_placements(self.__class__.TEST_APP_KEY,
                                                               [rv_placement, banner_placement])

        mocked_req.assert_called_once_with(
            method='post', url="https://platform.ironsrc.com/partners/publisher/placements/v1", **options)

    @pytest.mark.asyncio
    async def test_unit_get_placements(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                "appKey": "1234abc",
            }
        }

        res = await ironsrc_api.monetize_api().get_placements(self.__class__.TEST_APP_KEY)
        mocked_req.assert_called_once_with(
            'get', url="https://platform.ironsrc.com/partners/publisher/placements/v1", **options)

    @pytest.mark.asyncio
    async def test_unit_update_placements(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json':
            {
                "appKey": "1234abc",
                "placements": [{
                    "adUnit": "rewardedVideo",
                    'itemName': 'gems',
                    "id": self.__class__.placement_id,
                    "adDelivery": 1,
                    "rewardAmount": 2,
                    "capping": {
                        "enabled": 1,
                        "cappingLimit": 4,
                        "cappingInterval": "d"
                    },
                    "pacing": {
                        "enabled": 1,
                        "pacingMinutes": 10
                    }
                }]
            }
        }
        placement_update = Placement(ad_unit=AdUnits.RewardedVideo, ad_delivery=True, placement_id=self.__class__.placement_id,
                                     item_name='gems', reward_amount=2, capping=Capping(4, 'd', True),
                                     pacing=Pacing(10, True))

        res = await ironsrc_api.monetize_api().update_placements(self.__class__.TEST_APP_KEY,
                                                                  [placement_update])
        mocked_req.assert_called_once_with(
            method='put', url="https://platform.ironsrc.com/partners/publisher/placements/v1", **options)

    @pytest.mark.asyncio
    async def test_unit_delete_placements(self):

        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                "appKey": "1234abc",
                "adUnit":"rewardedVideo",
                "id":self.__class__.placement_id
            }
        }

        res = await ironsrc_api.monetize_api().delete_placements(self.__class__.TEST_APP_KEY,
                                                                  AdUnits.RewardedVideo,
                                                                  self.__class__.placement_id)
        mocked_req.assert_called_once_with(method='delete',url="https://platform.ironsrc.com/partners/publisher/placements/v1", **options)

    @pytest.mark.asyncio
    async def test_unit_imp_ad_revenue(self):

        mocked_req = self.get_mock_exec_req('{\"urls\":[\"TEST\"]}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                "appKey": self.TEST_APP_KEY,
                "date":'2020-01-01',
                'reportType': 1
            }
        }
       

        res = await ironsrc_api.monetize_api().get_impression_ad_revenue('2020-01-01',self.TEST_APP_KEY)
        mocked_req.assert_has_calls([
            call('get',url="https://platform.ironsrc.com/partners/adRevenueMeasurements/v3", **options),
            call(method='get',url="TEST",is_gzip=True)
            ])

    @pytest.mark.asyncio
    async def test_unit_imp_ad_revenue_as_stream(self):
        mocked_req_stream = self.mocker.patch('ironsource_api.monetize_api.monetize_api.execute_request_as_stream',return_value=BytesIO())
        mocked_req = self.get_mock_exec_req('{\"urls\":[\"TEST\"]}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                "appKey": self.TEST_APP_KEY,
                "date":'2020-01-01',
                'reportType': 1
            }
        }
       

        res = await ironsrc_api.monetize_api().get_impression_ad_revenue('2020-01-01',self.TEST_APP_KEY,True)
        mocked_req.assert_called_once_with('get',url="https://platform.ironsrc.com/partners/adRevenueMeasurements/v3", **options)
        mocked_req_stream.assert_called_once_with(url="TEST",is_gzip=True)
    
    @pytest.mark.asyncio
    async def test_unit_user_ad_revenue_as_stream(self):
        mocked_req_stream = self.mocker.patch('ironsource_api.monetize_api.monetize_api.execute_request_as_stream',return_value=BytesIO())
        mocked_req = self.get_mock_exec_req('{\"urls\":[\"TEST\"]}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                "appKey": self.TEST_APP_KEY,
                "date":'2020-01-01',
                'reportType': 1
            }
        }
       

        res = await ironsrc_api.monetize_api().get_user_ad_revenue('2020-01-01',self.TEST_APP_KEY,True)
        mocked_req.assert_called_once_with('get',url="https://platform.ironsrc.com/partners/userAdRevenue/v3", **options)
        mocked_req_stream.assert_called_once_with(url="TEST",is_gzip=True)

    
    @pytest.mark.asyncio
    async def test_unit_user_ad_revenue(self):

        mocked_req = self.get_mock_exec_req('{\"urls\":[\"TEST\"]}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                "appKey": self.TEST_APP_KEY,
                "date":'2020-01-01',
                'reportType': 1
            }
        }
       

        res = await ironsrc_api.monetize_api().get_user_ad_revenue('2020-01-01',self.TEST_APP_KEY)
        mocked_req.assert_has_calls([
            call('get',url="https://platform.ironsrc.com/partners/userAdRevenue/v3", **options),
            call(method='get',url="TEST",is_gzip=True)
            ])
        


if __name__ == '__main__':
    unittest.main()
