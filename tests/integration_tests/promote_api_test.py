# pylint: disable=missing-module-docstring
import json
import unittest
import os
import time

import pytest

from ironsource_api.ironsource_api import IronSourceAPI
from ironsource_api.promote_api import Platform, CreativeType, UsageType
from ironsource_api.promote_api.audience_list import AudienceListMeta, AudienceListType, AudienceListData
from ironsource_api.promote_api.campaign_bids import CampaignBidsList, CampaignBid
from ironsource_api.promote_api.creatives import Creative, CreativeAsset
from ironsource_api import utils

API_CI_SECRET = os.environ.get('API_CI_SECRET', '')
API_CI_TOKEN = os.environ.get('API_CI_TOKEN', '')
API_CI_USER = os.environ.get('API_CI_USER', '')

DEMO_ACCOUNT_SECRET = os.environ.get('DEMO_ACCOUNT_SECRET', '')
DEMO_ACCOUNT_TOKEN = os.environ.get('DEMO_ACCOUNT_TOKEN', '')
DEMO_ACCOUNT_USER = os.environ.get('DEMO_ACCOUNT_USER', '')

ironsrc_api = IronSourceAPI()
ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                            API_CI_SECRET)


# pylint: disable=too-many-public-methods, missing-function-docstring,missing-class-docstring
class PromoteAPITest(unittest.IsolatedAsyncioTestCase):
    audience_list_trgt_name = 'AudienceListTest_Trgt_{}'.format(int(time.time()))
    audience_list_trgt_id = -1
    audience_list_sprsn_name = 'AudienceListTest_Sprsn_{}'.format(
        int(time.time()))
    audience_list_sprsn_id = -1

    bidsArrayTest = [
        {'country': 'AR', 'bid': 1},
        {'country': 'AU', 'bid': 7},
        {'country': 'BR', 'bid': 2},
        {'country': 'CA', 'bid': 5},
        {'country': 'DE', 'bid': 3},
        {'country': 'IL', 'bid': 4},
        {'country': 'GB', 'bid': 5},
        {'country': 'US', 'bid': 10}
    ]

    test_campaign_id = 8377514
    test_app_id = 366221

    request_id = ''
    results_count = 0
    results_bulk_size = 0
    page_num = 0

    @pytest.mark.run(order=1)
    async def test_create_targeting_audience_list(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        promote_api = ironsrc_api.promote_api()
        audience_meta_data = AudienceListMeta(name=self.audience_list_trgt_name, list_type=AudienceListType.Targeting,
                                              description='desc_' + self.audience_list_trgt_name)
        assert audience_meta_data
        res = await promote_api.create_audience_list(audience_meta_data)
        assert isinstance(res, dict)
        assert 'id' in res
        self.__class__.audience_list_trgt_id = res['id']

    @pytest.mark.run(order=2)
    async def test_create_suppression_audience_list(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        promote_api = ironsrc_api.promote_api()
        audience_meta_data = AudienceListMeta(name=self.audience_list_sprsn_name, list_type=AudienceListType.Suppression,
                                              description='desc_' + self.audience_list_sprsn_name,
                                              platform=Platform.Android, bundle_id='iron.web.jalepano.browser')
        assert audience_meta_data
        res = await promote_api.create_audience_list(audience_meta_data)
        assert isinstance(res, dict)
        assert 'id' in res
        self.__class__.audience_list_sprsn_id = res['id']

    @pytest.mark.run(order=3)
    def test_meta_data_exception(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        with pytest.raises(Exception):
            AudienceListMeta(name=self.audience_list_sprsn_name,
                             list_type=AudienceListType.Suppression,
                             description='desc_' + self.audience_list_sprsn_name,
                             bundle_id='iron.web.jalepano.browser')

        with pytest.raises(Exception):
            AudienceListMeta(name=self.audience_list_sprsn_name,
                             list_type=AudienceListType.Suppression,
                             description='desc_' + self.audience_list_sprsn_name,
                             platform=Platform.Android)

    @pytest.mark.run(order=4)
    async def test_add_devices_to_targeting_list(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        audience_list_data = AudienceListData()
        audience_list_data.add_devices(
            ['bb602f59-0cf6-4d25-8ba5-19eb6e1c68f0', '3075ac27-1718-44f2-a0a7-072bc565777e'])
        audience_list_data.add_list_for_update(
            str(self.__class__.audience_list_trgt_id))
        res = await ironsrc_api.promote_api().update_audience_list(audience_list_data)
        assert res == 'Accepted'

    @pytest.mark.run(order=5)
    async def test_add_devices_to_suppression_list(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        audience_list_data = AudienceListData()
        audience_list_data.add_devices(
            ['bb602f59-0cf6-4d25-8ba5-19eb6e1c68f0', '3075ac27-1718-44f2-a0a7-072bc565777e'])
        audience_list_data.add_list_for_update(
            str(self.__class__.audience_list_sprsn_id))
        res = await ironsrc_api.promote_api().update_audience_list(audience_list_data)
        assert res == 'Accepted'

    @pytest.mark.run(order=6)
    async def test_remove_devices_from_lists(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        audience_list_data = AudienceListData()
        audience_list_data.add_devices(
            ['bb602f59-0cf6-4d25-8ba5-19eb6e1c68f0', '3075ac27-1718-44f2-a0a7-072bc565777e'])
        audience_list_data.add_list_for_remove(
            str(self.__class__.audience_list_sprsn_id))
        res = await ironsrc_api.promote_api().update_audience_list(audience_list_data)
        assert res == 'Accepted'

    @pytest.mark.run(order=7)
    async def test_get_audience_lists(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        audience_lists = await ironsrc_api.promote_api().get_audience_lists()

        assert isinstance(audience_lists, dict)
        assert isinstance(audience_lists['audiences'], list)

    @pytest.mark.run(order=8)
    async def test_delete_all_audience_lists(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        audience_lists = await ironsrc_api.promote_api().get_audience_lists()

        for audience_list in audience_lists['audiences']:
            res = await ironsrc_api.promote_api().delete_audience_list(audience_list['id'])
            assert isinstance(res, dict)

    @pytest.mark.run(order=9)
    async def test_add_bid_for_campaign_no_app_id(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        bid_list = CampaignBidsList(self.__class__.test_campaign_id)
        for bid in self.__class__.bidsArrayTest:
            bid_list.add_bid(CampaignBid(
                bid=bid['bid'], country=bid['country']))

        res = await ironsrc_api.promote_api().update_bids([bid_list])

        assert isinstance(res, list)
        assert len(res) == 1
        assert (res[0]['campaignId'], res[0]['bidUpdates'], res[0]['msg']) == (
            self.__class__.test_campaign_id, len(self.__class__.bidsArrayTest), 'Accepted')

    @pytest.mark.run(order=10)
    def test_get_bids_for_campaign(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        byte_arr_r = ironsrc_api.promote_api().get_bids_for_campaign(campaign_id=self.__class__.test_campaign_id,
                                                                     max_records=5)
        iterate_index = 1
        line = byte_arr_r.readline()
        while len(line) > 0:
            bid_arr = json.loads(line)
            if iterate_index == 1:
                assert isinstance(bid_arr, list)
                assert (len(bid_arr), bid_arr[0]['country'], bid_arr[0]['bid']) == (
                    5, 'AR', 1)
            else:
                assert isinstance(bid_arr, list)
                assert len(bid_arr) == 3

            iterate_index += 1
            line = byte_arr_r.readline()

        byte_arr_r.close()

    @pytest.mark.run(order=11)
    async def test_delete_campaign_bids(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        bid_list = CampaignBidsList(campaign_id=self.__class__.test_campaign_id)
        for bid in self.__class__.bidsArrayTest:
            bid_list.add_bid(CampaignBid(
                bid=bid['bid'], country=bid['country']))

        res = await ironsrc_api.promote_api().delete_bids([bid_list])

        assert isinstance(res, list)
        assert len(res) == 1
        assert (res[0]['campaignId'], res[0]['bidUpdates'], res[0]['msg']) == (
            self.__class__.test_campaign_id, len(self.__class__.bidsArrayTest), 'Accepted')

    @pytest.mark.run(order=12)
    async def test_add_bid_for_campaign_with_app_id(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        bid_list = CampaignBidsList(self.__class__.test_campaign_id)
        bid_list.add_bid(CampaignBid(bid=10, country='US',
                         application_id=self.__class__.test_app_id))

        res = await ironsrc_api.promote_api().update_bids([bid_list])
        assert isinstance(res, list)
        assert len(res) == 1
        assert (res[0]['campaignId'], res[0]['bidUpdates'], res[0]['msg']) == (
            self.__class__.test_campaign_id, 1, 'Accepted')

    @pytest.mark.run(order=13)
    async def test_delete_bid_for_campaign_with_app_id(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        bid_list = CampaignBidsList(self.__class__.test_campaign_id)
        bid_list.add_bid(CampaignBid(bid=10, country='US',
                         application_id=self.__class__.test_app_id))

        res = await ironsrc_api.promote_api().delete_bids([bid_list])
        assert isinstance(res, list)
        assert len(res) == 1
        assert (res[0]['campaignId'], res[0]['bidUpdates'], res[0]['msg']) == (
            self.__class__.test_campaign_id, 1, 'Accepted')

    @pytest.mark.run(order=14)
    async def test_get_titles(self):
        ironsrc_api.set_credentials(DEMO_ACCOUNT_USER, DEMO_ACCOUNT_TOKEN,
                                    DEMO_ACCOUNT_SECRET)
        titles = await ironsrc_api.promote_api().get_titles()
        assert isinstance(titles, dict)

    @pytest.mark.run(order=15)
    async def test_get_titles_with_search(self):
        ironsrc_api.set_credentials(DEMO_ACCOUNT_USER, DEMO_ACCOUNT_TOKEN,
                                    DEMO_ACCOUNT_SECRET)
        titles = await ironsrc_api.promote_api().get_titles(search_term='Adobe')
        assert isinstance(titles, dict)

    @pytest.mark.run(order=16)
    async def test_get_titles_with_os(self):
        ironsrc_api.set_credentials(DEMO_ACCOUNT_USER, DEMO_ACCOUNT_TOKEN,
                                    DEMO_ACCOUNT_SECRET)
        titles = await ironsrc_api.promote_api().get_titles(os_sys=Platform.Android)
        assert isinstance(titles, dict)

    @pytest.mark.run(order=17)
    async def test_get_titles_with_bulk(self):
        ironsrc_api.set_credentials(DEMO_ACCOUNT_USER, DEMO_ACCOUNT_TOKEN,
                                    DEMO_ACCOUNT_SECRET)
        results_bulk_size = 50
        titles = await ironsrc_api.promote_api().get_titles(results_bulk_size=results_bulk_size)
        assert isinstance(titles, dict)
        assert len(titles['titles']) == results_bulk_size
        assert isinstance(titles['requestId'], str)
        results_count = titles['totalResultsCount']

        import math
        page_num = math.ceil(results_count/results_bulk_size)

        self.__class__.results_count = results_count
        self.__class__.results_bulk_size = results_bulk_size
        self.__class__.page_num = page_num
        self.__class__.request_id = titles['requestId']

    @pytest.mark.run(order=18)
    async def test_get_titles_with_requestId(self):
        ironsrc_api.set_credentials(DEMO_ACCOUNT_USER, DEMO_ACCOUNT_TOKEN,
                                    DEMO_ACCOUNT_SECRET)
        request_id = self.__class__.request_id
        results_count = self.__class__.results_count
        results_bulk_size = self.__class__.results_bulk_size
        page_num = self.__class__.page_num

        titles = await ironsrc_api.promote_api().get_titles(request_id=request_id, results_bulk_size=results_bulk_size, page_number=2)
        assert isinstance(titles, dict)
        assert len(titles['titles']) == results_count - \
            results_bulk_size if page_num == 2 else results_bulk_size

    @pytest.mark.run(order=19)
    async def test_get_assets(self):
        ironsrc_api.set_credentials(DEMO_ACCOUNT_USER, DEMO_ACCOUNT_TOKEN,
                                    DEMO_ACCOUNT_SECRET)
        assets = await ironsrc_api.promote_api().get_assets(title_id=604146, ids=[1077455])
        assert isinstance(assets, dict)

    @pytest.mark.run(order=20)
    async def test_create_assets(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)

        ts = int(time.time())
        assets = await ironsrc_api.promote_api().create_assets(530297, 'image', './tests/test_asset_python.jpeg', f"test_asset_{ts}.jpeg")
        assert isinstance(assets, dict)
        assert assets['assets'][0]['name'] == f"test_asset_{ts}.jpeg"

    @pytest.mark.run(order=21)
    async def test_get_creatives(self):
        ironsrc_api.set_credentials(
            DEMO_ACCOUNT_USER, DEMO_ACCOUNT_TOKEN, DEMO_ACCOUNT_SECRET)
        creatives_res = await ironsrc_api.promote_api().get_creatives(title_id=770594)
        assert isinstance(creatives_res, dict)
        assert isinstance(creatives_res['creatives'], list)
        assert len(creatives_res['creatives']) == 5

    @pytest.mark.run(order=22)
    async def test_create_creatives(self):
        ironsrc_api.set_credentials(API_CI_USER, API_CI_TOKEN,
                                    API_CI_SECRET)
        creatives = await ironsrc_api.promote_api().get_creatives(title_id=530297)
        assert isinstance(creatives['creatives'], list)
        assert len(creatives['creatives'][0]['assets']) == 4
        creative_name = f"test_creative_{int(time.time())}"
        new_creative = Creative(
            name=creative_name, creative_type=CreativeType.VIDEO_CAROUSEL, language='EN')
        creative_asset: CreativeAsset
        for creative_asset in creatives['creatives'][0]['assets']:
            new_creative.add_asset(CreativeAsset(asset_id=creative_asset['id'], usage_type=UsageType(creative_asset['usageType'])))
        creative_res = await ironsrc_api.promote_api().create_creatives(title_id=530297, creatives=[new_creative])
        assert isinstance(creative_res, dict)
        assert 'success' in creative_res
        assert creative_res['success'] == True
        assert len(creative_res['ids']) == 1

    @pytest.mark.run(order=23)
    async def test_creative_raise_error(self):
        with pytest.raises(Exception):
            new_creative = Creative(
                name='test_creative', creative_type=CreativeType.VIDEO_CAROUSEL, language='EN')
            new_creative.add_asset(CreativeAsset(123,UsageType.INTERACTIVE_ENDCARD))

        with pytest.raises(Exception):
            new_creative = Creative(
                name='test_creative', creative_type=CreativeType.VIDEO_CAROUSEL, language='EN')
            new_creative.add_asset(CreativeAsset(123,UsageType.LEFT))
            new_creative.add_asset(CreativeAsset(123,UsageType.RIGHT))
            creative_res = await ironsrc_api.promote_api().create_creatives(title_id=530297, creatives=[new_creative])


if __name__ == '__main__':
    unittest.main()
