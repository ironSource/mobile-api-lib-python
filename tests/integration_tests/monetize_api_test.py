# pylint: disable=missing-module-docstring
import unittest
from typing import Dict, List
import time
import os
import asyncio

import pydash

import pytest

from ironsource_api.ironsource_api import IronSourceAPI
from ironsource_api.monetize_api import AdUnitStatus, AdUnitStatusMap, AdUnits, Platform, Networks, Breakdowns, Metrics
from ironsource_api.monetize_api.instance_config import IronSourceInstance, VungleInstance
from ironsource_api.monetize_api.mediation_group_priority import MediationGroupPriority, MediationGroupTier, TierType
from ironsource_api.monetize_api.placement_config import Placement, Pacing, Capping

TEST_APP_NAME = 'Test_{}'.format(int(time.time()))
API_CI_SECRET = os.environ.get('API_CI_SECRET', '')
API_CI_TOKEN = os.environ.get('API_CI_TOKEN', '')
API_CI_USER = os.environ.get('API_CI_USER', '')
DEMO_ACCOUNT_SECRET = os.environ.get('DEMO_ACCOUNT_SECRET', '')
DEMO_ACCOUNT_TOKEN = os.environ.get('DEMO_ACCOUNT_TOKEN', '')
DEMO_ACCOUNT_USER = os.environ.get('DEMO_ACCOUNT_USER', '')

iron_src_api = IronSourceAPI()

# pylint: disable=too-many-public-methods, missing-function-docstring,missing-class-docstring


class IronSourceAPITest(unittest.IsolatedAsyncioTestCase):
    TEST_APP_KEY = 'd8ceefb9'
    ironsource_instance_id = -1
    mediation_group_id = -1
    placement_id = -1

    @pytest.mark.run(order=1)
    async def test_get_apps(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        res = await iron_src_api.monetize_api().get_apps()
        assert isinstance(res, list)
        self.assertEqual(set(res[0].keys()),
                         {'appKey', 'appName', 'adUnits', 'appStatus', 'bundleId', 'creationDate', 'icon',
                          'networkReportingApi', 'platform', 'coppa', 'taxonomy', 'bundleRefId', 'ccpa'})

    @pytest.mark.run(order=2)
    async def test_add_app(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)
        ad_unit_status = AdUnitStatusMap()
        ad_unit_status[AdUnits.RewardedVideo] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Interstitial] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Offerwall] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Banner] = AdUnitStatus.Test

        res = await iron_src_api.monetize_api().add_temporary_app(app_name=TEST_APP_NAME, platform=Platform.Android,
                                                                  coppa=False, ad_unit_status=ad_unit_status, ccpa=False)
        assert isinstance(res, dict)

        app_list = await iron_src_api.monetize_api().get_apps()
        app_object: dict

        for app_obj in app_list:
            if app_obj["appKey"] == res["appKey"]:
                app_object = app_obj
                break

        self.__class__.TEST_APP_KEY = res["appKey"]

        assert app_object["appName"] == TEST_APP_NAME
        assert app_object["platform"] == Platform.Android.value
        assert (type(app_object["adUnits"]["rewardedVideo"]["activeNetworks"]),
                len(app_object["adUnits"]["rewardedVideo"]["activeNetworks"])) == (list, 1)
        assert (type(app_object["adUnits"]["offerWall"]["activeNetworks"]),
                len(app_object["adUnits"]["offerWall"]["activeNetworks"])) == (list, 1)
        assert (type(app_object["adUnits"]["interstitial"]["activeNetworks"]),
                len(app_object["adUnits"]["interstitial"]["activeNetworks"])) == (list, 1)
        assert (type(app_object["adUnits"]["banner"]["activeNetworks"]),
                len(app_object["adUnits"]["banner"]["activeNetworks"])) == (list, 1)

    @pytest.mark.run(order=3)
    async def test_add_live_app(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)
        ad_unit_status = AdUnitStatusMap()
        ad_unit_status[AdUnits.RewardedVideo] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Interstitial] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Offerwall] = AdUnitStatus.Test
        ad_unit_status[AdUnits.Banner] = AdUnitStatus.Test
        taxonomy = 'Other Non-Gaming'

        res = await iron_src_api.monetize_api().add_app(
            'https://play.google.com/store/apps/details?id=iron.web.jalepano.browser', taxonomy, False, ad_unit_status, False)

        assert isinstance(res, dict)

        app_list = await iron_src_api.monetize_api().get_apps()
        app_object: dict

        for app_obj in app_list:
            if app_obj["appKey"] == res["appKey"]:
                app_object = app_obj
                break

        self.__class__.TEST_APP_KEY = res["appKey"]
        assert app_object["appName"] == 'Super Fast Browser'
        assert app_object["platform"] == Platform.Android.value
        assert (type(app_object["adUnits"]["rewardedVideo"]["activeNetworks"]),
                len(app_object["adUnits"]["rewardedVideo"]["activeNetworks"])) == (list, 1)
        assert (type(app_object["adUnits"]["offerWall"]["activeNetworks"]),
                len(app_object["adUnits"]["offerWall"]["activeNetworks"])) == (list, 1)
        assert (type(app_object["adUnits"]["interstitial"]["activeNetworks"]),
                len(app_object["adUnits"]["interstitial"]["activeNetworks"])) == (list, 1)
        assert (type(app_object["adUnits"]["banner"]["activeNetworks"]),
                len(app_object["adUnits"]["banner"]["activeNetworks"])) == (list, 1)

    @pytest.mark.run(order=4)
    async def test_create_new_instances(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        assert self.__class__.TEST_APP_KEY != ''
        ironsource_price_map: Dict[int, List[str]] = {10: ['US'], 5: ['IL']}

        ironsource_instance = IronSourceInstance(instance_name='TEST', ad_unit=AdUnits.RewardedVideo,
                                                 application_key=self.__class__.TEST_APP_KEY, status=False,
                                                 pricing=ironsource_price_map)
        vungle_instance = VungleInstance(instance_name='TEST', ad_unit=AdUnits.RewardedVideo, app_id='TEST',
                                         reporting_api_id='TEST', placement_id='TEST', status=True)

        res = await iron_src_api.monetize_api().add_instances(self.__class__.TEST_APP_KEY,
                                                              [ironsource_instance, vungle_instance])

        assert isinstance(res, dict)

        assert res['rewardedVideo']
        assert (type(res['rewardedVideo']['ironSource']), len(
            res['rewardedVideo']['ironSource'])) == (list, 2)

        ironsource_instance = pydash.find(
            res['rewardedVideo']['ironSource'], lambda inst: inst['name'] == 'TEST')
        self.__class__.ironsource_instance_id = ironsource_instance['id']

        assert ironsource_instance['name'] == 'TEST'
        assert ironsource_instance['status'] == 'inactive'
        assert (type(ironsource_instance['pricing']), len(
            ironsource_instance['pricing'])) == (list, 2)
        self.assertCountEqual(ironsource_instance['pricing'],
                              [{"eCPM": 10, "Countries": ["US"]}, {"eCPM": 5, "Countries": ["IL"]}])
        assert (type(res['rewardedVideo']['Vungle']), len(
            res['rewardedVideo']['Vungle'])) == (list, 1)

    @pytest.mark.run(order=5)
    async def test_add_instances_without_appconfig(self):
        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        assert self.__class__.TEST_APP_KEY != ''
     
        vungle_instance = VungleInstance(instance_name='TEST2', ad_unit=AdUnits.RewardedVideo, app_id='',
                                         reporting_api_id='', placement_id='TEST2', status=True)

        res = await iron_src_api.monetize_api().add_instances(self.__class__.TEST_APP_KEY,
                                                              [ vungle_instance])

        assert isinstance(res, dict)

        assert res['rewardedVideo']
        assert (type(res['rewardedVideo']['Vungle']), len(
            res['rewardedVideo']['Vungle'])) == (list, 2)

       

    @pytest.mark.run(order=5)
    async def test_update_instances(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)
        assert self.__class__.ironsource_instance_id != -1
        ironsource_price_map: Dict[int, List[str]] = {7: ['US'], 5: ['IL']}
        
        ironsource_instance_update = IronSourceInstance(instance_name='TEST', ad_unit=AdUnits.RewardedVideo,
                                                        application_key=self.__class__.TEST_APP_KEY, status=False,
                                                        pricing=ironsource_price_map,
                                                        instance_id=self.__class__.ironsource_instance_id)
        ironsource_def_instance = IronSourceInstance(instance_name='Default', ad_unit=AdUnits.RewardedVideo,
                                                     application_key=self.__class__.TEST_APP_KEY, status=True,
                                                     instance_id=0)

        res = await iron_src_api.monetize_api().update_instances(self.__class__.TEST_APP_KEY,
                                                                 [ironsource_instance_update, ironsource_def_instance])

        assert isinstance(res, dict)

        ironsource_instance = pydash.find(res['rewardedVideo']['ironSource'],
                                          lambda inst: inst['id'] == self.__class__.ironsource_instance_id)

        self.assertCountEqual(ironsource_instance['pricing'],
                              [{"eCPM": 7, "Countries": ["US"]}, {"eCPM": 5, "Countries": ["IL"]}])

    @pytest.mark.run(order=6)
    async def test_delete_instances(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)
        assert self.__class__.ironsource_instance_id != -1

        res = await iron_src_api.monetize_api().delete_instance(self.__class__.TEST_APP_KEY,
                                                                self.__class__.ironsource_instance_id)
        assert isinstance(res, dict)
        assert (type(res['rewardedVideo']['ironSource']), len(
            res['rewardedVideo']['ironSource'])) == (list, 1)

    @pytest.mark.run(order=8)
    async def test_get_mediation_group(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        res = await iron_src_api.monetize_api().get_mediation_groups(application_key='c90cab7d')

        assert isinstance(res, dict)
        assert 'adUnits' in res
        assert (type(res['adUnits']['rewardedVideo']), len(
            res['adUnits']['rewardedVideo'])) == (list, 1)
        assert res['adUnits']['rewardedVideo'][0]['groupName'] == 'All Countries'
        assert res['adUnits']['rewardedVideo'][0]['adSourcePriority']['tier1']['tierType'] == 'sortByCpm'
        assert (type(res['adUnits']['rewardedVideo'][0]['adSourcePriority']['tier1']['instances']),
                len(res['adUnits']['rewardedVideo'][0]['adSourcePriority']['tier1']['instances'])) == (list, 1)
        assert (type(res['adUnits']['rewardedVideo'][0]['adSourcePriority']['tier2']['instances']),
                len(res['adUnits']['rewardedVideo'][0]['adSourcePriority']['tier2']['instances'])) == (list, 3)
        assert (type(res['adUnits']['rewardedVideo'][0]['adSourcePriority']['tier3']['instances']),
                len(res['adUnits']['rewardedVideo'][0]['adSourcePriority']['tier3']['instances'])) == (list, 1)

    @pytest.mark.run(order=8)
    async def test_create_mediation_group(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        assert self.__class__.TEST_APP_KEY != ''

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
        
        res = await iron_src_api.monetize_api().create_mediation_group(application_key=self.__class__.TEST_APP_KEY,
                                                                       ad_unit=AdUnits.RewardedVideo,
                                                                       group_name='Test_Group_Automation',
                                                                       group_countries=[
                                                                           'US', 'IL'],
                                                                       ad_source_priority=mediation_group_priority,
                                                                       group_position=1)

        assert isinstance(res, dict)
        assert (type(res['adUnits']['rewardedVideo']), len(
            res['adUnits']['rewardedVideo'])) == (list, 2)

        group_object = pydash.find(res['adUnits']['rewardedVideo'],
                                   lambda group: group['groupName'] == 'Test_Group_Automation')

        self.assertCountEqual(group_object['groupCountries'], ['US', 'IL'])

        assert group_object['adSourcePriority']['tier1']['tierType'] == TierType.MANUAL.value
        assert (type(group_object['adSourcePriority']['tier1']['instances']),
                len(group_object['adSourcePriority']['tier1']['instances'])) == (list, 1)
        tier1_instance = group_object['adSourcePriority']['tier1']['instances'][0]

        assert (tier1_instance['instanceId'], tier1_instance['providerName'],
                tier1_instance['rate']) == (0, Networks.IronSource.value, 10)

        assert (tier1_instance['capping']['value'],
                tier1_instance['capping']['interval']) == (2, 'session')

        assert group_object['adSourcePriority']['tier2']['tierType'] == TierType.SORT_BY_CPM.value
        assert (type(group_object['adSourcePriority']['tier2']['instances']),
                len(group_object['adSourcePriority']['tier2']['instances'])) == (list, 1)

        tier2_instance = group_object['adSourcePriority']['tier2']['instances'][0]
        assert (tier2_instance['instanceId'], tier2_instance['providerName']) == (
            0, Networks.Vungle.value)

        self.__class__.mediation_group_id = group_object['groupId']

    @pytest.mark.run(order=9)
    async def test_update_mediation_group(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        assert self.__class__.mediation_group_id != -1

        ironsource_price_map: Dict[int, List[str]] = {10: ['US'], 5: ['IL']}

        ironsource_instance_update = IronSourceInstance(instance_name='TEST_FOR_GROUP', ad_unit=AdUnits.RewardedVideo,
                                                        application_key=self.__class__.TEST_APP_KEY, status=True,
                                                        pricing=ironsource_price_map)

        res_add_instance = await iron_src_api.monetize_api().add_instances(application_key=self.__class__.TEST_APP_KEY,
                                                                           instances=[ironsource_instance_update])

        new_instance = pydash.find(res_add_instance['rewardedVideo']['ironSource'],
                                   lambda instance: instance['name'] == 'TEST_FOR_GROUP')
        new_instance_id = new_instance['id']

        mediation_group_prio = MediationGroupPriority()
        tier1 = MediationGroupTier(TierType.MANUAL)
        tier1.add_instances(network=Networks.IronSource,
                            instance_id=0, rate=10, position=1, capping=2)
        tier2 = MediationGroupTier(tier_type=TierType.SORT_BY_CPM)
        tier2.add_instances(network=Networks.Vungle,
                            instance_id=0, rate=4, position=1)
        tier3 = MediationGroupTier(tier_type=TierType.SORT_BY_CPM)
        tier3.add_instances(network=Networks.IronSource,
                            instance_id=new_instance_id)

        mediation_group_prio.set_mediation_group_tier(
            group_tier=tier1, position=0)
        mediation_group_prio.set_mediation_group_tier(
            group_tier=tier2, position=1)
        mediation_group_prio.set_mediation_group_tier(
            group_tier=tier3, position=2)

        update_res = await iron_src_api.monetize_api().update_mediation_group(
            application_key=self.__class__.TEST_APP_KEY, group_id=self.__class__.mediation_group_id,
            group_name='Test_Group_Automation_updated', group_countries=['US'], ad_source_priority=mediation_group_prio)

        group_object = pydash.find(update_res['adUnits']['rewardedVideo'],
                                   lambda group: group['groupName'] == 'Test_Group_Automation_updated')

        assert group_object['adSourcePriority']['tier3']['tierType'] == TierType.SORT_BY_CPM.value
        assert (type(group_object['adSourcePriority']['tier3']['instances']),
                len(group_object['adSourcePriority']['tier3']['instances'])) == (list, 1)

        updated_instance = group_object['adSourcePriority']['tier3']['instances'][0]

        assert updated_instance['instanceId'] == new_instance_id
        assert updated_instance['providerName'] == Networks.IronSource.value

    @pytest.mark.run(order=10)
    async def test_delete_mediation_group(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        assert self.__class__.mediation_group_id != -1

        res = await iron_src_api.monetize_api().delete_mediation_group(application_key=self.__class__.TEST_APP_KEY,
                                                                       group_id=self.__class__.mediation_group_id)

        assert isinstance(res, dict)
        assert (type(res['adUnits']['rewardedVideo']), len(
            res['adUnits']['rewardedVideo'])) == (list, 1)

    @pytest.mark.run(order=11)
    async def test_report_with_demo_data(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)

        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01')
        assert (type(res), len(res)) == (list, 4)
        assert isinstance(res[0]["data"], list)
        assert len(res[0]["data"]) > 0

    @pytest.mark.run(order=12)
    async def test_report_demo_data_app_breakdown(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      breakdowns=[Breakdowns.Application])

        assert type(res) == list
        assert len(res) >= 16

    @pytest.mark.run(order=13)
    async def test_report_demo_data_only_one_app(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      breakdowns=[Breakdowns.Application])

        assert (type(res), len(res)) == (list, 3)
        assert 'Golden Cave Treasure' in (res[0]['appName'])

    @pytest.mark.run(order=14)
    # pylint: disable=invalid-name
    async def test_report_demo_data_one_app_US_only(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      country='US',
                                                                      breakdowns=[Breakdowns.Country])

        assert (type(res), len(res)) == (list, 3)
        assert (type(res[0]['data']), res[0]['data']
                [0]['countryCode']) == (list, 'US')

    @pytest.mark.run(order=15)
    async def test_report_demo_data_one_app_rv_only(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      breakdowns=[Breakdowns.Application])
        assert (type(res), len(res)) == (list, 1)
        assert (res[0]['adUnits']) == 'Rewarded Video'

    @pytest.mark.run(order=16)
    async def test_report_demo_data_one_app_rv_breakdown_by_network(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      breakdowns=[Breakdowns.Network])
        assert (type(res), len(res)) == (list, 10)
        assert (res[0]['adUnits']) == 'Rewarded Video'
        assert 'providerName' in res[0]
        assert len(res[0]['data'][0]) > 0

    @pytest.mark.run(order=17)
    async def test_report_demo_data_one_app_rv_breakdown_by_instance_ironsource_network(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      ad_source=Networks.IronSource,
                                                                      breakdowns=[Breakdowns.Instance])
        assert (type(res), len(res)) == (list, 4)
        assert (res[0]['adUnits']) == 'Rewarded Video'
        assert (res[0]['providerName']) == 'ironSource'
        assert 'instanceId' in res[0]
        assert 'instanceName' in res[0]
        assert len(res[0]['data'][0]) > 0

    @pytest.mark.run(order=18)
    async def test_report_demo_data_one_app_rv_breakdown_by_adunit(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_source=Networks.IronSource,
                                                                      breakdowns=[Breakdowns.AdUnits])

        assert (type(res), len(res)) == (list, 3)
        assert len(res[0]['data'][0]) > 0

    @pytest.mark.run(order=19)
    async def test_report_demo_data_one_app_rv_breakdown_by_country(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_source=Networks.IronSource,
                                                                      breakdowns=[Breakdowns.Country])

        assert (type(res), len(res)) == (list, 3)
        assert len(res[0]['data']) == 209

    @pytest.mark.run(order=20)
    async def test_report_demo_data_one_app_rv_breakdown_by_placement(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      breakdowns=[Breakdowns.Placement])

        assert (type(res), len(res)) == (list, 11)
        assert 'adUnits' in res[0]
        assert len(res[0]['data'][0]) > 0

    @pytest.mark.run(order=21)
    async def test_report_demo_data_one_app_rv_breakdown_by_platform(self):

        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      breakdowns=[Breakdowns.Platform])
        assert len(res) > 0
        assert 'platform' in res[0]
        assert len(res[0]['data']) > 0

    @pytest.mark.run(order=22)
    async def test_report_demo_data_one_app_rv_breakdown_by_segment(self):
        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      breakdowns=[Breakdowns.Segment])
        assert len(res) > 0
        assert 'segment' in res[0]
        assert len(res[0]['data']) > 0

    @pytest.mark.run(order=23)
    async def test_report_demo_data_one_app_only_impressions(self):
        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      metrics=[Metrics.impressions])
        assert len(res) == 1
        assert len(res[0]['data']) == 1
        assert len(res[0]['data'][0].keys()) == 1
        self.assertCountEqual(res[0]['data'][0].keys(), ['impressions'])

    @pytest.mark.run(order=24)
    async def test_report_demo_data_one_app_only_revenue(self):
        iron_src_api.set_credentials(DEMO_ACCOUNT_USER,
                                     DEMO_ACCOUNT_TOKEN,
                                     DEMO_ACCOUNT_SECRET)
        res = await iron_src_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01',
                                                                      application_key='c581a75d',
                                                                      ad_units=AdUnits.RewardedVideo,
                                                                      metrics=[Metrics.revenue])
        assert len(res) == 1
        assert len(res[0]['data']) == 1
        assert len(res[0]['data'][0].keys()) == 1
        self.assertCountEqual(res[0]['data'][0].keys(), ['revenue'])

    @pytest.mark.run(order=25)
    async def test_create_new_placements(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        assert self.__class__.TEST_APP_KEY != ''
        
        rv_placement = Placement(ad_unit=AdUnits.RewardedVideo, ad_delivery=False, name='TEST_RV_PLACEMENT',
                                 item_name='diamonds', reward_amount=1)

        res = await iron_src_api.monetize_api().add_placements(self.__class__.TEST_APP_KEY,
                                                               [rv_placement])

        assert isinstance(res, dict)

        assert res['placements']
        assert (type(res['placements']), len(res['placements'])) == (list, 1)

        placement = pydash.find(
            res['placements'], lambda inst: inst['name'] == 'TEST_RV_PLACEMENT')
        print(res['placements'])
        self.__class__.placement_id = placement['id']

        assert placement['name'] == 'TEST_RV_PLACEMENT'
        assert placement['adUnit'] == AdUnits.RewardedVideo.value

    @pytest.mark.run(order=26)
    async def test_get_placements(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)

        res = await iron_src_api.monetize_api().get_placements(self.__class__.TEST_APP_KEY)
        assert isinstance(res, list)
        self.assertEqual(set(res[0].keys()),
                         {'name', 'id', 'adUnit', 'itemName', 'rewardAmount', 'adDelivery', 'capping',
                          'pacing', 'abVersion'})

    @pytest.mark.run(order=27)
    async def test_update_placements(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)
        assert self.__class__.placement_id != -1

        placement_update = Placement(ad_unit=AdUnits.RewardedVideo, ad_delivery=True, placement_id=self.__class__.placement_id,
                                     item_name='gems', reward_amount=2, capping=Capping(4, 'd', True),
                                     pacing=Pacing(10, True))

        res = await iron_src_api.monetize_api().update_placements(self.__class__.TEST_APP_KEY,
                                                                  [placement_update])

        assert res==True
        placements = await iron_src_api.monetize_api().get_placements(self.__class__.TEST_APP_KEY)

        placement = pydash.find(placements,
                                lambda p: p['id'] == self.__class__.placement_id)

        assert placement['id'] == self.__class__.placement_id
        assert placement['adUnit'] == AdUnits.RewardedVideo.value
        assert placement['adDelivery'] == 1
        assert placement['itemName'] == 'gems'
        assert placement['rewardAmount'] == 2
        assert isinstance(placement['capping'], dict)
        assert placement['capping']['enabled'] == 1
        assert placement['capping']['cappingLimit'] == 4
        assert placement['capping']['cappingInterval'] == 'd'
        assert isinstance(placement['pacing'], dict)
        assert placement['pacing']['enabled'] == 1
        assert placement['pacing']['pacingMinutes'] == 10

    @pytest.mark.run(order=28)
    async def test_delete_placements(self):

        iron_src_api.set_credentials(API_CI_USER,
                                     API_CI_TOKEN,
                                     API_CI_SECRET)
        assert self.__class__.placement_id != -1

        res = await iron_src_api.monetize_api().delete_placements(self.__class__.TEST_APP_KEY,
                                                                  AdUnits.RewardedVideo,
                                                                  self.__class__.placement_id)
        assert res == 'true'


if __name__ == '__main__':
    unittest.main()
