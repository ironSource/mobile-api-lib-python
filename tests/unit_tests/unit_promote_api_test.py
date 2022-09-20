# pylint: disable=missing-module-docstring
from io import BytesIO, FileIO
from itertools import count
import json
import unittest
import time

from pytest_mock import MockerFixture

import pytest

from ironsource_api.ironsource_api import IronSourceAPI
from ironsource_api.promote_api.promote_api import AdUnits, Breakdowns, Metrics, Platform, CreativeType
from ironsource_api.promote_api.audience_list import AudienceListMeta, AudienceListType, AudienceListData
from ironsource_api.promote_api.campaign_bids import CampaignBidsList, CampaignBid
from ironsource_api.promote_api.creatives import Creative, CreativeAsset, UsageType
from ironsource_api.utils import ResponseInterface


ironsrc_api = IronSourceAPI()
ironsrc_api.set_credentials('TEST_USER', 'TEST_TOKEN',
                            'TEST_SECRET')


# pylint: disable=too-many-public-methods, missing-function-docstring,missing-class-docstring
@pytest.mark.asyncio
class UnitPromoteAPITest(unittest.IsolatedAsyncioTestCase):

    audience_list_trgt_name = 'AudienceListTest_Trgt_Test'
    audience_list_trgt_id = '1234abcd'
    audience_list_sprsn_name = 'AudienceListTest_Sprsn_Test'
    audience_list_sprsn_id = '1234abcd'

    bids_array_test = [
        {'country': 'AR', 'bid': 1},
        {'country': 'AU', 'bid': 7},
        {'country': 'BR', 'bid': 2},
        {'country': 'CA', 'bid': 5},
        {'country': 'DE', 'bid': 3},
        {'country': 'IL', 'bid': 4},
        {'country': 'IR', 'bid': 5},
        {'country': 'US', 'bid': 10}
    ]

    test_campaign_id = 1234
    test_app_id = '1234abcd'

    request_id = '1234'
    results_count = 0
    results_bulk_size = 50
    page_num = 2

    @pytest.fixture(autouse=True)
    def before_after_tests(self, mocker: MockerFixture):
        self.mocker = mocker
        mocker.patch(
            'ironsource_api.promote_api.promote_api.BaseAPI.get_bearer_auth', return_value='TOKEN')
        yield

    def get_mock_exec_req(self, msg):
        mocked_res = ResponseInterface()
        mocked_res.msg = msg
        mocked_res.error_code = -1
        mocked_req = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.execute_request',
            return_value=mocked_res)

        return mocked_req

    def get_mock_exec_req_with_pagination(self, msg):
        mocked_req = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.execute_request_with_pagination',
            return_value=None)

        return mocked_req

    @pytest.mark.asyncio
    async def test_unit_create_targeting_audience_list(self):
        self.mocker.patch(
            'ironsource_api.promote_api.promote_api.BaseAPI.get_basic_auth', return_value='TOKEN')
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        options = {
            'headers': {
                'Authorization': 'Basic TOKEN'
            },
            'json': {
                'name': self.audience_list_trgt_name,
                'type': 'targeting',
                'description': 'desc_' + self.audience_list_trgt_name
            }
        }

        promote_api = ironsrc_api.promote_api()
        audience_meta_data = AudienceListMeta(name=self.audience_list_trgt_name, list_type=AudienceListType.Targeting,
                                              description=f'desc_{self.audience_list_trgt_name}')

        res = await promote_api.create_audience_list(audience_meta_data)

        mocked_req.assert_called_once_with(
            'post', "https://platform-api.supersonic.com/audience/api/create", False, **options)

    @pytest.mark.asyncio
    async def test_unit_create_suppression_audience_list(self):
        self.mocker.patch(
            'ironsource_api.promote_api.promote_api.BaseAPI.get_basic_auth', return_value='TOKEN')
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        options = {
            'headers': {
                'Authorization': 'Basic TOKEN'
            },
            'json': {
                'name': self.audience_list_sprsn_name,
                'type': 'suppression_static',
                'platform': 'android',
                'bundleId': 'iron.web.jalepano.browser',
                'description': 'desc_' + self.audience_list_sprsn_name
            }
        }

        promote_api = ironsrc_api.promote_api()
        audience_meta_data = AudienceListMeta(name=self.audience_list_sprsn_name, list_type=AudienceListType.Suppression,
                                              description='desc_' + self.audience_list_sprsn_name,
                                              platform=Platform.Android, bundle_id='iron.web.jalepano.browser')
        res = await promote_api.create_audience_list(audience_meta_data)
        mocked_req.assert_called_once_with(
            'post', "https://platform-api.supersonic.com/audience/api/create", False, **options)

    @pytest.mark.asyncio
    def test_unit_meta_data_exception(self):

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

    @pytest.mark.asyncio
    async def test_unit_add_devices_to_targeting_list(self):
        self.mocker.patch(
            'ironsource_api.promote_api.promote_api.BaseAPI.get_basic_auth', return_value='TOKEN')
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        options = {
            'headers': {
                'Authorization': 'Basic TOKEN'
            },
            'json': {
                'deviceIds': ['bb602f59-0cf6-4d25-8ba5-19eb6e1c68f0', '3075ac27-1718-44f2-a0a7-072bc565777e'],
                'addAudience': [str(self.__class__.audience_list_trgt_id)]
            }
        }
        audience_list_data = AudienceListData()
        audience_list_data.add_devices(
            ['bb602f59-0cf6-4d25-8ba5-19eb6e1c68f0', '3075ac27-1718-44f2-a0a7-072bc565777e'])
        audience_list_data.add_list_for_update(
            str(self.__class__.audience_list_trgt_id))
        res = await ironsrc_api.promote_api().update_audience_list(audience_list_data)
        mocked_req.assert_called_once_with(
            'post', 'https://platform-api.supersonic.com/audience/api', False, **options)

    @pytest.mark.asyncio
    async def test_unit_remove_devices_from_lists(self):

        self.mocker.patch(
            'ironsource_api.promote_api.promote_api.BaseAPI.get_basic_auth', return_value='TOKEN')
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')

        options = {
            'headers': {
                'Authorization': 'Basic TOKEN'
            },
            'json': {
                'deviceIds': ['bb602f59-0cf6-4d25-8ba5-19eb6e1c68f0', '3075ac27-1718-44f2-a0a7-072bc565777e'],
                'removeAudience': [str(self.__class__.audience_list_trgt_id)]
            }
        }

        audience_list_data = AudienceListData()
        audience_list_data.add_devices(
            ['bb602f59-0cf6-4d25-8ba5-19eb6e1c68f0', '3075ac27-1718-44f2-a0a7-072bc565777e'])
        audience_list_data.add_list_for_remove(
            str(self.__class__.audience_list_sprsn_id))
        res = await ironsrc_api.promote_api().update_audience_list(audience_list_data)

        mocked_req.assert_called_once_with(
            'post', 'https://platform-api.supersonic.com/audience/api', False, **options)

    @pytest.mark.asyncio
    async def test_unit_get_audience_lists(self):
        self.mocker.patch(
            'ironsource_api.promote_api.promote_api.BaseAPI.get_basic_auth', return_value='TOKEN')
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Basic TOKEN'
            }
        }

        audience_lists = await ironsrc_api.promote_api().get_audience_lists()
        mocked_req.assert_called_once_with(
            method='get', url='https://platform-api.supersonic.com/audience/api/show', **options)

    @pytest.mark.asyncio
    async def test_unit_delete_all_audience_lists(self):
        self.mocker.patch(
            'ironsource_api.promote_api.promote_api.BaseAPI.get_basic_auth', return_value='TOKEN')
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Basic TOKEN'
            }
        }
        audience_list = '1234'

        res = await ironsrc_api.promote_api().delete_audience_list(audience_list)
        mocked_req.assert_called_once_with(
            'delete', 'https://platform-api.supersonic.com/audience/api/1234', **options)

    @pytest.mark.asyncio
    async def test_unit_add_bid_for_campaign_no_app_id(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                'bids': self.bids_array_test,
                'campaignId': self.__class__.test_campaign_id

            }
        }
        bid_list = CampaignBidsList(self.__class__.test_campaign_id)
        for bid in self.__class__.bids_array_test:
            bid_list.add_bid(CampaignBid(
                bid=bid['bid'], country=bid['country']))

        res = await ironsrc_api.promote_api().update_bids([bid_list])
        mocked_req.assert_called_once_with(
            method='put', url='https://api.ironsrc.com/advertisers/v2/multibid', **options)

    def test_unit_get_bids_for_campaign(self):
        mocked_req = self.get_mock_exec_req_with_pagination(msg='Test')
        r_steam = BytesIO()
        mocked_io_pipe = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.os.pipe',
            return_value=(123, 123))
        mocked_io_open = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.io.open',
            return_value=r_steam)
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'campaignId': self.__class__.test_campaign_id,
                'count': 5

            }
        }

        byte_arr_r = ironsrc_api.promote_api().get_bids_for_campaign(campaign_id=self.__class__.test_campaign_id,
                                                                     max_records=5)

        mocked_req.assert_called_once_with(
            'https://api.ironsrc.com/advertisers/v2/multibid', 123, "bids", "Error getting bids for campaign", options, False)

    @pytest.mark.asyncio
    async def test_unit_delete_campaign_bids(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                'campaignId': self.__class__.test_campaign_id,
                'bids':
                self.__class__.bids_array_test

            }
        }
        bid_list = CampaignBidsList(
            campaign_id=self.__class__.test_campaign_id)
        for bid in self.__class__.bids_array_test:
            bid_list.add_bid(CampaignBid(
                bid=bid['bid'], country=bid['country']))

        res = await ironsrc_api.promote_api().delete_bids([bid_list])
        mocked_req.assert_called_once_with(
            method='delete', url='https://api.ironsrc.com/advertisers/v2/multibid', **options)

    @pytest.mark.asyncio
    async def test_unit_add_bid_for_campaign_with_app_id(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                'campaignId': self.__class__.test_campaign_id,
                'bids':
                [{
                    'applicationId': self.__class__.test_app_id,
                    'bid': 10,
                    'country': 'US'

                }]

            }
        }

        bid_list = CampaignBidsList(self.__class__.test_campaign_id)
        bid_list.add_bid(CampaignBid(bid=10, country='US',
                         application_id=self.__class__.test_app_id))

        res = await ironsrc_api.promote_api().update_bids([bid_list])
        mocked_req.assert_called_once_with(
            method='put', url='https://api.ironsrc.com/advertisers/v2/multibid', **options)

    @pytest.mark.asyncio
    async def test_unit_delete_bid_for_campaign_with_app_id(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                'campaignId': self.__class__.test_campaign_id,
                'bids':
                [{
                    'applicationId': self.__class__.test_app_id,
                    'bid': 10,
                    'country': 'US'

                }]

            }
        }
        bid_list = CampaignBidsList(self.__class__.test_campaign_id)
        bid_list.add_bid(CampaignBid(bid=10, country='US',
                         application_id=self.__class__.test_app_id))

        res = await ironsrc_api.promote_api().delete_bids([bid_list])
        mocked_req.assert_called_once_with(
            method='delete', url='https://api.ironsrc.com/advertisers/v2/multibid', **options)

    @pytest.mark.asyncio
    async def test_unit_get_titles(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {}
        }
        titles = await ironsrc_api.promote_api().get_titles()
        mocked_req.assert_called_once_with(
            method='get', url='https://api.ironsrc.com/advertisers/v2/titles', **options)

    @pytest.mark.asyncio
    async def test_unit_get_titles_with_search(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'searchTerm': 'Adobe'
            }
        }
        titles = await ironsrc_api.promote_api().get_titles(search_term='Adobe')
        mocked_req.assert_called_once_with(
            method='get', url='https://api.ironsrc.com/advertisers/v2/titles', **options)

    @pytest.mark.asyncio
    async def test_unit_get_titles_with_os(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'os': 'android'
            }
        }
        titles = await ironsrc_api.promote_api().get_titles(os_sys=Platform.Android)
        mocked_req.assert_called_once_with(
            method='get', url='https://api.ironsrc.com/advertisers/v2/titles', **options)

    @pytest.mark.asyncio
    async def test_unit_get_titles_with_bulk(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'resultsBulkSize': 50,
                'pageNumber': self.__class__.page_num,
                'requestId': self.__class__.request_id
            }
        }
        results_bulk_size = 50
        titles = await ironsrc_api.promote_api().get_titles(results_bulk_size=results_bulk_size, page_number=self.__class__.page_num, request_id=self.__class__.request_id)
        mocked_req.assert_called_once_with(
            method='get', url='https://api.ironsrc.com/advertisers/v2/titles', **options)

    @pytest.mark.asyncio
    async def test_unit_get_assets(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'titleId': '1234',
                'ids': '1234'
            }
        }
        assets = await ironsrc_api.promote_api().get_assets(title_id=1234, ids=[1234])
        mocked_req.assert_called_once_with(
            method='get', url='https://api.ironsrc.com/advertisers/v2/assets', **options)

    @pytest.mark.asyncio
    async def test_unit_create_assets(self):

        self.mocker.patch(
            'ironsource_api.promote_api.promote_api.open', return_value=None)
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'files': {'file': ("test_asset.jpeg", None)},
            'data': {
                'type': 'image',
                'titleId': '1234'
            }
        }

        assets = await ironsrc_api.promote_api().create_assets(1234, 'image', './tests/test_asset_python.jpeg', "test_asset.jpeg")
        mocked_req.assert_called_once_with(
            'post', 'https://api.ironsrc.com/advertisers/v2/assets', False, **options)

    @pytest.mark.asyncio
    async def test_unit_get_creatives(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'titleId': '1234',
                'type': 'videoAndCarousel',
                'requestId': self.request_id,
                'pageNumber': self.page_num,
                'resultsBulkSize': self.results_bulk_size

            }
        }

        creatives_res = await ironsrc_api.promote_api().get_creatives(title_id=1234, creative_type=CreativeType.VIDEO_CAROUSEL,
                                                                      request_id=self.request_id, page_number=self.page_num,
                                                                      results_bulk_size=self.results_bulk_size)
        mocked_req.assert_called_once_with(
            method='get', url='https://api.ironsrc.com/advertisers/v2/creatives', is_gzip=False, **options)

    @pytest.mark.asyncio
    async def test_unit_create_creatives(self):
        creative_name = f"test_creative_Test"
        assets = [{'id': 1234, 'usageType': 'video'},
                  {'id': 1234, 'usageType': 'right'},
                  {'id': 1234, 'usageType': 'middle'},
                  {'id': 1234, 'usageType': 'left'}]
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'json': {
                'titleId': 1234,
                'creatives': [{
                    'name': creative_name,
                    'language': 'EN',
                    'type': 'videoAndCarousel',
                    'assets': assets
                }
                ]
            }
        }

        new_creative = Creative(
            name=creative_name, creative_type=CreativeType.VIDEO_CAROUSEL, language='EN')
        creative_asset: CreativeAsset
        for creative_asset in assets:
            new_creative.add_asset(CreativeAsset(
                asset_id=creative_asset['id'], usage_type=UsageType(creative_asset['usageType'])))
        creative_res = await ironsrc_api.promote_api().create_creatives(title_id=1234, creatives=[new_creative])

        mocked_req.assert_called_once_with(
            "post", "https://api.ironsrc.com/advertisers/v2/creatives", **options)

    @pytest.mark.asyncio
    async def test_unit_creative_raise_error(self):
        with pytest.raises(Exception):
            new_creative = Creative(
                name='test_creative', creative_type=CreativeType.VIDEO_CAROUSEL, language='EN')
            new_creative.add_asset(CreativeAsset(
                123, UsageType.INTERACTIVE_ENDCARD))

        with pytest.raises(Exception):
            new_creative = Creative(
                name='test_creative', creative_type=CreativeType.VIDEO_CAROUSEL, language='EN')
            new_creative.add_asset(CreativeAsset(123, UsageType.LEFT))
            new_creative.add_asset(CreativeAsset(123, UsageType.RIGHT))
            creative_res = await ironsrc_api.promote_api().create_creatives(title_id=530297, creatives=[new_creative])

    def test_unit_reporting_api(self):
        mocked_req = self.get_mock_exec_req_with_pagination(msg='Test')
        r_steam = BytesIO()
        mocked_io_pipe = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.os.pipe',
            return_value=(123, 123))
        mocked_io_open = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.io.open',
            return_value=r_steam)
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'startDate': '2020-01-01',
                'endDate': '2020-01-01',
                'format': 'json',
                'direction': 'asc',
                'metrics': 'clicks,completions',
                'breakdowns': 'creatives,country',
                'campaignId': '1234',
                'bundleId': 'com.is.test',
                'count': 5,
                'country': 'US',
                'creativeId': '1234',
                'os': 'android',
                'deviceType': 'phone',
                'adUnit': 'rewardedVideo',
                'order': 'country'
            }

        }
        ironsrc_api.promote_api().get_advertiser_statistics(start_date='2020-01-01', end_date='2020-01-01', metrics=[Metrics.Clicks, Metrics.Completions],
                                                            breakdowns=[Breakdowns.Creatives, Breakdowns.Country], campaign_ids=['1234'], bundle_ids=['com.is.test'], count=5, country=['US'],
                                                            creative_ids=['1234'], os_sys=Platform.Android, device_type='phone', ad_unit=AdUnits.RewardedVideo, order=Breakdowns.Country)

        mocked_req.assert_called_once_with('https://api.ironsrc.com/advertisers/v2/reports',
                                           123, 'data', "error getting advertiser statistics", options, False)

    def test_unit_skan_reporting_api(self):
        mocked_req = self.get_mock_exec_req_with_pagination(msg='Test')
        r_steam = BytesIO()
        mocked_io_pipe = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.os.pipe',
            return_value=(123, 123))
        mocked_io_open = self.mocker.patch(
            'ironsource_api.promote_api.promote_api.io.open',
            return_value=r_steam)
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'startDate': '2020-01-01',
                'endDate': '2020-01-01',
                'format': 'json',
                'direction': 'asc',
                'metrics': 'storeOpens,installs',
                'breakdowns': 'day,title',
                'campaignId': '1234',
                'bundleId': 'com.is.test',
                'count': 5,
                'country': 'US',
                'creativeId': '1234',
                'os': 'android',
                'deviceType': 'phone',
                'adUnit': 'rewardedVideo',
                'order': 'country'
            }

        }
        ironsrc_api.promote_api().get_skan_reporting(start_date='2020-01-01', end_date='2020-01-01', metrics=[Metrics.StoreOpens, Metrics.Installs],
                                                            breakdowns=[Breakdowns.Day, Breakdowns.Title], campaign_ids=['1234'], bundle_ids=['com.is.test'], count=5, country=['US'],
                                                            creative_ids=['1234'], os_sys=Platform.Android, device_type='phone', ad_unit=AdUnits.RewardedVideo, order=Breakdowns.Country,as_bytes=True)

        mocked_req.assert_called_once_with('https://api.ironsrc.com/advertisers/v4/reports/skan',
                                           123, 'data',  "error getting skan report", options, True)

    @pytest.mark.asyncio
    async def test_unit_universal_skan_reporting_api(self):
        mocked_req = self.get_mock_exec_req('{\"TEST\":\"TEST\"}')
        options = {
            'headers': {
                'Authorization': 'Bearer TOKEN'
            },
            'params': {
                'date': '2020-01-01'
            }

        }
        await ironsrc_api.promote_api().get_universal_skan_report(date='2020-01-01')

        mocked_req.assert_called_once_with(method='get',url='https://platform.ironsrc.com/partners/postback/v1', **options)

if __name__ == '__main__':
    unittest.main()
