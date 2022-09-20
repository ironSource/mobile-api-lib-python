"""IronSource Promotion API"""
import io
import json
import os
import asyncio
import threading

from typing import Iterable, Union

import pydash
from ironsource_api.base_api import BaseAPI

from ironsource_api.promote_api import SKAN_REPORTING_API, UNIVERSAL_SKAN_API, CreativeType, Metrics, Breakdowns, Platform, AdUnits, REPORTING_API, MULTI_BID_API, \
    AUDIENCE_API_SHOW, AUDIENCE_API_CREATE, AUDIENCE_API_DELETE, AUDIENCE_API_UPDATE, TITLE_API, ASSETS_API, CREATIVES_API
from .audience_list import AudienceListMeta, AudienceListData
from .campaign_bids import CampaignBidsList
from .creatives import Creative
from ..utils import execute_request_with_pagination, execute_request, check_instance


class PromoteAPI(BaseAPI):
    """IronSource Promote API"""


    def get_skan_reporting(self, start_date: str, end_date: str, metrics: Iterable[Metrics],
                           breakdowns: Iterable[Breakdowns] = None, response_format: str = 'json',
                           count: int = None, campaign_ids: Iterable[int] = None, bundle_ids: Iterable[str] = None,
                           creative_ids: Iterable[int] = None, country: Iterable[str] = None, os_sys: Platform = None,
                           device_type: str = None, ad_unit: AdUnits = None,
                           order: Union[Metrics, Breakdowns] = None, direction: str = 'asc', as_bytes=False) -> io.BytesIO:
        """
        SKAN Reporting API
        This method returns a BytesIO stream which will contain all responses from the api including pagination
        The stream will contain new data all the time until there is no more.
        in case of json, each response will be it's own json array
        :param start_date: report start date in the following format YYYY-MM-DD
        :param end_date: report end date in the following format YYYY-MM-DD
        :param metrics: list of report metrics. see ironsource_api.promote_api.Metrics
        :param breakdowns: list of report breakdowns. see ironsource_api.promote_api.Breakdowns
        :param response_format: report format type 'csv' or 'json' only - default 'json'
        :param count: maximum number of records in the report
        :param campaign_ids: list of campaign ids
        :param bundle_ids: list of bundle ids
        :param creative_ids: list of creative ids.
        :param country: list of country code in 2 letter country code,
        as per [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
        :param os_sys: either 'ios' or 'android'.
        :param device_type: either 'phone' or 'tablet'
        :param ad_unit: Ad Unit. see ironsource_api.promote_api.AdUnits
        :param order: a breakdown or metric to order by
        :param direction: direction of order 'asc' or 'desc' - default 'asc'
        :param as_bytes: in case the return io.BytesIO value should be in bytes
        :return: io.BytesIO stream that will contain the response

        example:
        bytes_io = iron_src_api.promote_api().get_advertiser_statistics('2020-10-03','2020-10-04',
        [Metrics.Impressions,Metrics.Clicks,Metrics.Installs],
        [Breakdowns.Application,Breakdowns.Day],response_format='csv')

        line = bytes_io_r.readline()

        while len(line) > 0:
            print(line)
            line = bytes_io_r.readline()

        bytes_io_r.close()

        """
        allowed_metrics = [
            Metrics.Impressions,
            Metrics.Spend,
            Metrics.Installs,
            Metrics.StoreOpens]
        if len(list(set(metrics)-set(allowed_metrics))) > 0:
            raise ValueError(
                f"Only {', '.join(metric.value for metric in allowed_metrics)} Metrics are allowed in Skan Reporting")

        if breakdowns:
            allowed_breakdowns = [
                Breakdowns.Day,
                Breakdowns.Campaign,
                Breakdowns.Title,
                Breakdowns.Application,
                Breakdowns.AdUnit,
                Breakdowns.Country
            ]
            if len(list(set(breakdowns)-set(allowed_breakdowns))) > 0:
                raise ValueError(
                    f"Only {', '.join(breakdown.value for breakdown in allowed_breakdowns)} Breakdowns are allowed in Skan Reporting")

        if ad_unit:
            allowed_ad_units = [AdUnits.Interstitial, AdUnits.RewardedVideo]
            if ad_unit not in allowed_ad_units:
                raise ValueError(
                    f"Only {', '.join(ad_unit.value for ad_unit in allowed_ad_units)} Ad Units are allowed in Skan Reporting")
        if order:
            allowed_order = [
                Breakdowns.Day,
                Breakdowns.Campaign,
                Breakdowns.Title,
                Breakdowns.Application,
                Breakdowns.Country,
                Metrics.Impressions,
                Metrics.Spend,
                Metrics.Installs
            ]
            if order not in allowed_order:
                raise ValueError(
                    f"You can only order by {', '.join(order.value for order in allowed_order)} for Skan Reporting")

        return self._reporting_api_impl(
            start_date, end_date, metrics, SKAN_REPORTING_API,
            "error getting skan report", breakdowns, response_format,
            count, campaign_ids, bundle_ids, creative_ids, country, os_sys,
            device_type, ad_unit, order, direction, as_bytes
        )

    def get_advertiser_statistics(self, start_date: str, end_date: str, metrics: Iterable[Metrics],
                                  breakdowns: Iterable[Breakdowns] = None, response_format: str = 'json',
                                  count: int = None, campaign_ids: Iterable[int] = None, bundle_ids: Iterable[str] = None,
                                  creative_ids: Iterable[int] = None, country: Iterable[str] = None, os_sys: Platform = None,
                                  device_type: str = None, ad_unit: AdUnits = None,
                                  order: Union[Metrics, Breakdowns] = None, direction: str = 'asc', as_bytes=False) -> io.BytesIO:
        """
        User Acquisition Reporting API
        This method returns a BytesIO stream which will contain all responses from the api including pagination
        The stream will contain new data all the time until there is no more.
        in case of json, each response will be it's own json array
        :param start_date: report start date in the following format YYYY-MM-DD
        :param end_date: report end date in the following format YYYY-MM-DD
        :param metrics: list of report metrics. see ironsource_api.promote_api.Metrics
        :param breakdowns: list of report breakdowns. see ironsource_api.promote_api.Breakdowns
        :param response_format: report format type 'csv' or 'json' only - default 'json'
        :param count: maximum number of records in the report
        :param campaign_ids: list of campaign ids
        :param bundle_ids: list of bundle ids
        :param creative_ids: list of creative ids.
        :param country: list of country code in 2 letter country code,
        as per [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
        :param os_sys: either 'ios' or 'android'.
        :param device_type: either 'phone' or 'tablet'
        :param ad_unit: Ad Unit. see ironsource_api.promote_api.AdUnits
        :param order: a breakdown or metric to order by
        :param direction: direction of order 'asc' or 'desc' - default 'asc'
        :param as_bytes: in case the return io.BytesIO value should be in bytes
        :return: io.BytesIO stream that will contain the response

        example:
        bytes_io = iron_src_api.promote_api().get_advertiser_statistics('2020-10-03','2020-10-04',
        [Metrics.Impressions,Metrics.Clicks,Metrics.Installs],
        [Breakdowns.Application,Breakdowns.Day],response_format='csv')

        line = bytes_io_r.readline()

        while len(line) > 0:
            print(line)
            line = bytes_io_r.readline()

        bytes_io_r.close()

        """
        allowed_metrics = [
            Metrics.Impressions,
            Metrics.Spend,
            Metrics.Clicks,
            Metrics.Installs,
            Metrics.Completions]
        if len(list(set(metrics)-set(allowed_metrics))) > 0:
            raise ValueError(
                f"Only {', '.join(metric.value for metric in allowed_metrics)} Metrics are not allowed in Advertiser Reporting")

        if breakdowns:
            allowed_breakdowns = [
                Breakdowns.Day,
                Breakdowns.Campaign,
                Breakdowns.Title,
                Breakdowns.Application,
                Breakdowns.AdUnit,
                Breakdowns.Country,
                Breakdowns.OS,
                Breakdowns.DeviceType,
                Breakdowns.Creatives
            ]
            if len(list(set(breakdowns)-set(allowed_breakdowns))) > 0:
                raise ValueError(
                    f"Only {', '.join(breakdown.value for breakdown in allowed_breakdowns)} Breakdowns are not allowed in Advertiser Reporting")

        if order:
            allowed_order = [
                Breakdowns.Day,
                Breakdowns.Campaign,
                Breakdowns.Title,
                Breakdowns.Application,
                Breakdowns.Country,
                Breakdowns.Creatives,
                Breakdowns.OS,
                Metrics.Impressions,
                Metrics.Clicks,
                Metrics.Completions,
                Metrics.Spend,
                Metrics.Installs
            ]
            if order not in allowed_order:
                raise ValueError(
                    f"You can only order by {', '.join(allowed_order.value for allowed_order in allowed_order)} for Advertiser Reporting")

        return self._reporting_api_impl(
            start_date, end_date, metrics, REPORTING_API,
            "error getting advertiser statistics", breakdowns, response_format,
            count, campaign_ids, bundle_ids, creative_ids, country, os_sys,
            device_type, ad_unit, order, direction, as_bytes
        )

    def _reporting_api_impl(self, start_date: str, end_date: str, metrics: Iterable[Metrics], api_url: str, err_msg: str, breakdowns: Iterable[Breakdowns] = None, response_format: str = 'json',
                            count: int = None, campaign_ids: Iterable[int] = None, bundle_ids: Iterable[str] = None,
                            creative_ids: Iterable[int] = None, country: Iterable[str] = None, os_sys: Platform = None,
                            device_type: str = None, ad_unit: AdUnits = None,
                            order: Union[Metrics, Breakdowns] = None, direction: str = 'asc', as_bytes=False):
        event_loop = asyncio.get_event_loop()
        pipe_r, pipe_w = os.pipe()

        open_as = 'rb' if as_bytes is True else 'r'
        bytes_io_r = io.open(pipe_r, open_as)
        bearer_token = event_loop.run_until_complete(
            self.get_bearer_auth())

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'startDate': start_date,
                'endDate': end_date,
                'format': response_format,
                'direction': direction,
                'metrics': []
            }
        }
        for metric in metrics:
            options['params']['metrics'].append(metric.value)
        options['params']['metrics'] = ','.join(options['params']['metrics'])
        if breakdowns:
            options['params']['breakdowns'] = []
            for breakdown in breakdowns:
                options['params']['breakdowns'].append(breakdown.value)
            options['params']['breakdowns'] = ','.join(
                options['params']['breakdowns'])
        if count:
            options['params']['count'] = count
        if campaign_ids:
            options['params']['campaignId'] = ','.join(campaign_ids)
        if bundle_ids:
            options['params']['bundleId'] = ','.join(bundle_ids)
        if creative_ids:
            options['params']['creativeId'] = ','.join(creative_ids)
        if country:
            options['params']['country'] = ','.join(country)
        if os_sys:
            options['params']['os'] = os_sys.value
        if device_type:
            options['params']['deviceType'] = device_type
        if ad_unit:
            options['params']['adUnit'] = ad_unit.value
        if order:
            options['params']['order'] = order.value

        bg_thread = threading.Thread(target=execute_request_with_pagination, name="_get_reporting_bg",
                                     args=[api_url, pipe_w, 'data', err_msg, options, as_bytes])
        bg_thread.start()

        return bytes_io_r

    async def get_universal_skan_report(self, date: str) -> str:
        """
            returns a copy of the raw winning postbacks data from every network, directly from Apple.
            :param date: date of the report
            :return: json with list of urls of the report
            :example:
            {
                "urls": [
                    "https://postback-hub.s3.amazonaws.com/athena/raw_data_rtm_postback_hub_csv_file/outputs/..."
                ],
                "expiration": "2021-10-11 07:39:37"
            }
        """

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'date': date
            }
        }
        res = await execute_request(method='get', url=UNIVERSAL_SKAN_API, **options)
        return res.msg

    def get_bids_for_campaign(self, campaign_id: int, max_records: int = 1000, as_bytes: bool = False) -> io.BytesIO:
        """
        returns the current bids for a campaign

        :param campaign_id: the campaign id to fetch bids for.
        :param max_records: maximum number of records per response
        :return: io.BytesIO stream that will contain the response
        """
        event_loop = asyncio.get_event_loop()
        pipe_r, pipe_w = os.pipe()
        open_as = 'rb' if as_bytes is True else 'r'
        bytes_io_r = io.open(pipe_r, open_as)

        bearer_token = event_loop.run_until_complete(
            self.get_bearer_auth())
        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {
                'campaignId': campaign_id,
                'count': max_records
            }
        }

        bg_thread = threading.Thread(target=execute_request_with_pagination, name="_get_bids_for_campaign",
                                     args=[MULTI_BID_API, pipe_w, "bids", "Error getting bids for campaign", options, as_bytes])
        bg_thread.start()

        return bytes_io_r

    async def update_bids(self, campaign_bids: Iterable[CampaignBidsList]):
        """
        Update bids for campaigns
        :param campaign_bids: Array of CampaignBidsList. Each CampaignBidList contain bids for a campaign.
        :return: array of all update requests and result message from the API.
        response object example
        ```js
        {'campaignId':1234,'bidsUpdates':999,'msg':'Accepted'}
        ```
        """
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            }
        }
        update_summary = []
        bid_list: CampaignBidsList
        for bid_list in campaign_bids:
            bids_chunks = pydash.chunk(
                bid_list.get_object_for_update()['bids'], 9998)
            for chunk in bids_chunks:
                options['json'] = {
                    'campaignId': bid_list.get_campaign_id(), 'bids': chunk}
                res = await execute_request(method='put', url=MULTI_BID_API, **options)
                update_summary.append(
                    {'campaignId': bid_list.get_campaign_id(), 'bidUpdates': len(chunk), 'msg': res.msg})

        return update_summary

    async def delete_bids(self, campaign_bids: Iterable[CampaignBidsList]):
        """
        Delete bids for campaigns
        :param campaign_bids: Array of CampaignBidsList. Each CampaignBidList contain bids for deletion.
        :return: array of all delete requests and result message from the API.
        response object example {'campaignId':1234,'bidsUpdates':999,'msg':'Accepted'}
        """
        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            }
        }
        update_summary = []
        bid_list: CampaignBidsList
        for bid_list in campaign_bids:
            bids_chunks = pydash.chunk(
                bid_list.get_object_for_update()['bids'], 9998)
            for chunk in bids_chunks:
                options['json'] = {
                    'campaignId': bid_list.get_campaign_id(), 'bids': chunk}
                res = await execute_request(method='delete', url=MULTI_BID_API, **options)
                update_summary.append(
                    {'campaignId': bid_list.get_campaign_id(), 'bidUpdates': len(chunk), 'msg': res.msg})

        return update_summary

    async def get_audience_lists(self):
        """
        return all audience lists for the account
        :return: json array with all audience list
        For example:
        {
          "count": 1,
          "audiences": [
            {
              "id": 1,
              "type": "targeting",
              "name": "batz",
              "description": "batz",
              "bundleId": "com.adsd.sdf",
              "platform": "android",
              "lastModified": "2017-01-31T20:00:00.000Z",
              "hasActiveCampaigns": true
            }
          ]
        }
        """
        basic_token = self.get_basic_auth()

        options = {
            'headers': {
                'Authorization': 'Basic ' + basic_token
            }
        }

        res = await execute_request(method='get', url=AUDIENCE_API_SHOW,  **options)
        if res.error_code != -1:
            raise Exception('Error getting Audience Lists: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def create_audience_list(self, audience_meta_data: AudienceListMeta):
        """
        Creates new Audience List
        :param audience_meta_data: Meta data of the new audience list. See AudienceListMeta
        :return: The API response
        """
        basic_token = self.get_basic_auth()

        options = {
            'headers': {
                'Authorization': 'Basic ' + basic_token
            },
            'json': audience_meta_data.to_object()
        }
        res = await execute_request('post', AUDIENCE_API_CREATE, False, **options)
        if res.error_code != -1:
            raise Exception('Error creating Audience Lists: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def delete_audience_list(self, audience_list_id: str):
        """
        Delete an audience list
        :param audience_list_id: The audience list to delete in string
        :return: The API response for deletion
        """
        basic_token = self.get_basic_auth()

        options = {
            'headers': {
                'Authorization': 'Basic ' + basic_token
            }
        }
        res = await execute_request('delete', AUDIENCE_API_DELETE.format(audience_list_id), **options)
        if res.error_code != -1:
            raise Exception(
                'Error deleting Audience List {} : {} Error Code: {}'.format(audience_list_id, res.msg, res.error_code))

        return json.loads(res.msg)

    async def update_audience_list(self, audience_list_data: AudienceListData):
        """
        Update Audience lists with device ids
        :param audience_list_data: Object containing audience lists ids and device ids. See AudienceListData
        :return: The API response for update of the list
        """

        basic_token = self.get_basic_auth()

        options = {
            'headers': {
                'Authorization': 'Basic ' + basic_token
            },
            'json': audience_list_data.to_object()
        }
        res = await execute_request('post', AUDIENCE_API_UPDATE, False, **options)
        if res.error_code != -1:
            raise Exception('Error updating Audience Lists: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return res.msg

    async def get_titles(self, os_sys: Platform = None, search_term: str = None, request_id: str = None, results_bulk_size: int = None, page_number: int = None)->dict:
        """Get list of title

        :param os_sys:Filter titles of a specified os, defaults to None.
        :type os_sys: Platform, optional
        :param search_term: Filter by the name or partial name of the title, defaults to None
        :type search_term: str, optional
        :param request_id: Used for paginated request, defaults to None
        :type request_id: str, optional
        :param results_bulk_size: Used for paginated request, defaults to None
        :type results_bulk_size: int, optional
        :param page_number: Used for paginated request, defaults to None
        :type page_number: int, optional
        :raises ValueError: _description_
        :return: dictionary with array of the titles
        :rtype: dict

            Example ::
            `{
                "titles": [
                    {
                    "id": 113366,
                    "bundleId": "com.yourcompany.MiniGame",
                    "os": "android",
                    "name": "Gaming mania"
                    },
                    {
                    "id": 225566,
                    "bundleId": "com.yourcompany.BestGame",
                    "os": "ios",
                    "name": "The Best Game"
                    },
                    {
                    "id": 773366,
                    "bundleId": "com.yourcompany.MusicGame",
                    "os": "ios",
                    "name": "Guitar Music"
                    }
                ],
                "totalResultsCount": 3,
                "requestId": "MzUzMjIuODI5OTk5OS41LjI5"
            }`
        """

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {}
        }

        if os_sys and isinstance(os_sys, Platform):
            options['params']['os'] = os_sys.value
        elif os_sys and not isinstance(os_sys, Platform):
            raise ValueError(
                '{} must be type {}, not {}.'.format('os', 'str', type(os)))

        if search_term and isinstance(search_term, str):
            options['params']['searchTerm'] = search_term
        elif search_term and not isinstance(search_term, str):
            raise ValueError('{} must be type {}, not {}.'.format(
                'search_term', 'str', type(search_term)))

        if request_id and isinstance(request_id, str):
            options['params']['requestId'] = request_id
        elif request_id and not isinstance(request_id, str):
            raise ValueError('{} must be type {}, not {}.'.format(
                'request_id', 'str', type(request_id)))

        if results_bulk_size and isinstance(results_bulk_size, int):
            options['params']['resultsBulkSize'] = results_bulk_size
        elif results_bulk_size and not isinstance(results_bulk_size, int):
            raise ValueError('{} must be type {}, not {}.'.format(
                'result_bulk_size', 'int', type(results_bulk_size)))

        if page_number and isinstance(page_number, int):
            options['params']['pageNumber'] = page_number
        elif page_number and not isinstance(page_number, int):
            raise ValueError('{} must be type {}, not {}.'.format(
                'page_number', 'int', type(page_number)))

        res = await execute_request(method='get', url=TITLE_API, **options)
        if res.error_code != -1:
            raise Exception('Error getting Titles List: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def get_assets(
        self,
        asset_type: str = None,
        title_id: int = None,
        ids: Union[int, list] = None,
        request_id: str = None,
        page_number: int = None,
        results_bulk_size: int = None
    ) -> dict:
        """Get List of assets

        :param asset_type: Filter assets of a specified type. (Options: image, video, html, html_iec), defaults to None
        :type asset_type: str, optional
        :param title_id: Title Id to filter by, defaults to None
        :type title_id: int, optional
        :param ids: Asset id to filter by, defaults to None
        :type ids: Union[int, list], optional
        :param request_id: Used for paginated requests, defaults to None
        :type request_id: str, optional
        :param page_number: Used for paginated requests, defaults to None
        :type page_number: int, optional
        :param results_bulk_size: Used for paginated requests, defaults to None
        :type results_bulk_size: int, optional
        :raises ValueError:
        :raises Exception:
        :return: JSON formatted array of the assets
        :rtype: dict

         **Example**: ::
                {
                "assets": [
                    {
                    "id": 200305,
                    "type": "video",
                    "titleId": 501567,
                    "orientation": "all",
                    "source": "none",
                    "duration": 30
                    },
                    {
                    "id": 200304,
                    "type": "image",
                    "titleId": 501567,
                    "orientation": "all",
                    "source": "none",
                    "duration": null
                    },
                    {
                    "id": 200303,
                    "type": "html_iec",
                    "titleId": 501567,
                    "orientation": "all",
                    "source": "playworks",
                    "duration": null
                    }
                ],
                "totalResultsCount": 3,
                "requestId": "MjA1MzUzLjIwMDMwMy40LjM1OTY="
                }
        """

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {}
        }

        asset_types = ['image', 'video', 'html', 'html_iec']
        if check_instance(asset_type, str, 'asset_type') and asset_type in asset_types:
            options['params']['type'] = asset_type
        elif asset_type is not None:
            raise ValueError('{} must be one of {}, not {}.'.format(
                'asset_type', asset_types, asset_type))

        if check_instance(title_id, int, 'title_id'):
            options['params']['titleId'] = str(title_id)

        if check_instance(ids, Union[int, list], 'ids'):
            if isinstance(ids, list):
                ids = ','.join(str(v) for v in ids)
            else:
                ids = str(ids)
            options['params']['ids'] = ids

        if check_instance(request_id, str, 'request_id'):
            options['params']['requestId'] = request_id

        if check_instance(page_number, int, 'page_number'):
            options['params']['pageNumber'] = page_number

        if check_instance(results_bulk_size, int, 'results_bulk_size'):
            options['params']['resultsBulkSize'] = results_bulk_size

        res = await execute_request(method='get', url=ASSETS_API, **options)
        if res.error_code != -1:
            raise Exception('Error getting Assets: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def create_assets(self, title_id: int, asset_type: str, file_path: str, file_name: str = None) -> dict:
        """Create Asset to be used with Creative

        :param title_id: Title id that the asset belongs to.
        :type title_id: int
        :param asset_type: The type of the asset. One of the following: image, video.
        :type asset_type: str
        :param file_path: Path to asset file. See details below.
        :type file_path: str
        :param file_name: Name to overwrite file's name, defaults to None
        :type file_name: str, optional
        :raises ValueError: _description_
        :raises Exception: _description_
        :return: json format with information on the uploaded asset
        :rtype: dict


        Files Requirements:

        Image
        File format: png,jpg,jpeg,gif
        Max file size: 2MB
        Min dimension: 320px
        Max dimension: 3,840px
        Ratio: From 1:2 to 2:1

        Video
        Max file size: 100MB
        Max duration: 60sec
        Ratio: From 1:2 to 2:1
        Note: Videos longer than 30sec will have limited traffic
        """

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token,
            },
            'files': {},
            'data': {}
        }

        asset_types = ['image', 'video']
        if check_instance(asset_type, str, 'asset_type') and asset_type in asset_types:
            options['data']['type'] = asset_type
        elif asset_type is not None:
            raise ValueError('{} must be one of {}, not {}.'.format(
                'asset_type', asset_types, asset_type))

        if check_instance(title_id, int, 'title_id'):
            options['data']['titleId'] = str(title_id)

        if file_path and file_name:
            if check_instance(file_name, str, 'file_name') and check_instance(file_path, str, 'file_path'):
                options['files']['file'] = (file_name,
                                            open(file_path, 'rb'))
        elif check_instance(file_path, str, 'file_path'):
            options['files']['file'] = open(file_path, 'rb')

        res = await execute_request('post', ASSETS_API, False, **options)
        if res.error_code != -1:
            raise Exception('Error creating Assets: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def get_creatives(self, creative_type: CreativeType = None, title_id: int = None, request_id: str = None, page_number: int = None,  results_bulk_size: int = None):
        """
        Name - Mandatory - Data type - Description
        :param creative_type: - No - String - Filter creatives of a specified type. Use CreativeType class
        :param title_id: - No - Number - Filter creatives of a specific title.
        :param request_id: - No - String - Used for paginated requests.
        :param page_number: - No - Number - Used for paginated requests.
        :param results_bulk_size: - No - Number - Used for paginated requests.
        """

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'params': {}
        }

        if check_instance(creative_type, CreativeType, 'creative_type'):
            options['params']['type'] = creative_type.value['name']

        if check_instance(title_id, int, 'title_id'):
            options['params']['titleId'] = str(title_id)

        if check_instance(request_id, str, 'request_id'):
            options['params']['requestId'] = request_id

        if check_instance(page_number, int, 'page_number'):
            options['params']['pageNumber'] = page_number

        if check_instance(results_bulk_size, int, 'results_bulk_size'):
            options['params']['resultsBulkSize'] = results_bulk_size

        res = await execute_request(method='get', url=CREATIVES_API, is_gzip=False, **options)
        if res.error_code != -1:
            raise Exception('Error getting Creatives: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)

    async def create_creatives(self, title_id: int, creatives: Iterable[Creative]) -> dict:
        """
        Name - Mandatory - Data type - Description
        :param title_id: - Yes - Int - The title ID.
        :param creatives: - Yes - List - List of creative objects. Use class Creative.
        :returns dict:
        {"success": true,
        "ids": [1,2,3]}
        """

        bearer_token = await self.get_bearer_auth()

        options = {
            'headers': {
                'Authorization': 'Bearer ' + bearer_token
            },
            'json': {'titleId': int,
                     'creatives': []}
        }

        if check_instance(title_id, str, 'title_id'):
            options['json']['titleId'] = title_id

        if check_instance(creatives, list, 'creatives'):
            creative: Creative
            for creative in creatives:
                if not creative.is_validate():
                    raise ValueError(
                        f"Creative {creative.get_name()} is missing assets")
                options['json']['creatives'].append(creative.get_object())

        res = await execute_request('post', CREATIVES_API, **options)
        if res.error_code != -1:
            raise Exception('Error creating Assets: {} Error Code: {}'.format(
                res.msg, res.error_code))

        return json.loads(res.msg)
