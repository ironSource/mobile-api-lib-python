# Table of Contents

* [promote\_api](#promote_api)
  * [AdUnits](#__init__.AdUnits)
  * [Breakdowns](#__init__.Breakdowns)
  * [Platform](#__init__.Platform)
  * [UsageType](#__init__.UsageType)
  * [CreativeType](#__init__.CreativeType)
  
  * [PromoteAPI](#promote_api.PromoteAPI)
    * [set\_credentials](#promote_api.PromoteAPI.set_credentials)
    * [get\_skan\_reporting](#promote_api.PromoteAPI.get_skan_reporting)
    * [get\_advertiser\_statistics](#promote_api.PromoteAPI.get_advertiser_statistics)
    * [get\_universal\_skan\_report](#promote_api.PromoteAPI.get_universal_skan_report)
    * [get\_bids\_for\_campaign](#promote_api.PromoteAPI.get_bids_for_campaign)
    * [update\_bids](#promote_api.PromoteAPI.update_bids)
    * [delete\_bids](#promote_api.PromoteAPI.delete_bids)
    * [get\_audience\_lists](#promote_api.PromoteAPI.get_audience_lists)
    * [create\_audience\_list](#promote_api.PromoteAPI.create_audience_list)
    * [delete\_audience\_list](#promote_api.PromoteAPI.delete_audience_list)
    * [update\_audience\_list](#promote_api.PromoteAPI.update_audience_list)
    * [get\_titles](#promote_api.PromoteAPI.get_titles)
    * [get\_assets](#promote_api.PromoteAPI.get_assets)
    * [create\_assets](#promote_api.PromoteAPI.create_assets)
    * [get\_creatives](#promote_api.PromoteAPI.get_creatives)
    * [create\_creatives](#promote_api.PromoteAPI.create_creatives)
* [audience\_list](#audience_list)
  * [AudienceListType](#audience_list.AudienceListType)
    * [Suppression](#audience_list.AudienceListType.Suppression)
    * [Targeting](#audience_list.AudienceListType.Targeting)
  * [AudienceListMeta](#audience_list.AudienceListMeta)
  * [AudienceListData](#audience_list.AudienceListData)
    * [add\_list\_for\_update](#audience_list.AudienceListData.add_list_for_update)
    * [add\_list\_for\_remove](#audience_list.AudienceListData.add_list_for_remove)
    * [add\_devices](#audience_list.AudienceListData.add_devices)
* [campaign\_bids](#campaign_bids)
  * [CampaignBid](#campaign_bids.CampaignBid)
  * [CampaignBidsList](#campaign_bids.CampaignBidsList)
    * [add\_bid](#campaign_bids.CampaignBidsList.add_bid)
    * [get\_campaign\_id](#campaign_bids.CampaignBidsList.get_campaign_id)
* [creatives](#creatives)
  * [CreativeAsset](#creatives.CreativeAsset)
    * [get\_asset\_id](#creatives.CreativeAsset.get_asset_id)
    * [get\_usage\_type](#creatives.CreativeAsset.get_usage_type)
  * [Creative](#creatives.Creative)
    * [check\_asset\_compatible](#creatives.Creative.check_asset_compatible)
    * [is\_validate](#creatives.Creative.is_validate)
    * [get\_name](#creatives.Creative.get_name)
    * [get\_creative\_type](#creatives.Creative.get_creative_type)
    * [get\_language](#creatives.Creative.get_language)
    * [get\_assets](#creatives.Creative.get_assets)
    * [add\_asset](#creatives.Creative.add_asset)

<a id="promote_api"></a>

# promote\_api

IronSource Promotion API

<a id="promote_api.PromoteAPI"></a>

## PromoteAPI

```python
class PromoteAPI()
```

IronSource Promote API

<a id="promote_api.PromoteAPI.set_credentials"></a>

#### set\_credentials

```python
def set_credentials(user: str, token: str, secret: str)
```

sets the API credentials

**Arguments**:

- `user`: - user name from the platform
- `token`: - token from the platform
- `secret`: - secret from the platform

<a id="promote_api.PromoteAPI.get_skan_reporting"></a>

#### get\_skan\_reporting

```python
def get_skan_reporting(start_date: str,
                       end_date: str,
                       metrics: Iterable[Metrics],
                       breakdowns: Iterable[Breakdowns] = None,
                       response_format: str = 'json',
                       count: int = None,
                       campaign_ids: Iterable[int] = None,
                       bundle_ids: Iterable[str] = None,
                       creative_ids: Iterable[int] = None,
                       country: Iterable[str] = None,
                       os_sys: Platform = None,
                       device_type: str = None,
                       ad_unit: AdUnits = None,
                       order: Union[Metrics, Breakdowns] = None,
                       direction: str = 'asc',
                       as_bytes=False) -> io.BytesIO
```

SKAN Reporting API

This method returns a BytesIO stream which will contain all responses from the api including pagination
The stream will contain new data all the time until there is no more.
in case of json, each response will be it's own json array

**Arguments**:

- `start_date`: report start date in the following format YYYY-MM-DD
- `end_date`: report end date in the following format YYYY-MM-DD
- `metrics`: list of report [metrics](#metrics).
- `breakdowns`: list of report [breakdowns](#breakdowns).
- `response_format`: report format type 'csv' or 'json' only - default 'json'
- `count`: maximum number of records in the report
- `campaign_ids`: list of campaign ids
- `bundle_ids`: list of bundle ids
- `creative_ids`: list of creative ids.
- `country`: list of country code in 2 letter country code,
as per [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
- `os_sys`: either 'ios' or 'android'. See [Platform](#platform)
- `device_type`: either 'phone' or 'tablet'
- `ad_unit`: Ad Unit. see [AdUnits](#adunits)
- `order`: a [breakdown](#breakdowns) or [metric](#metrics) to order by
- `direction`: direction of order 'asc' or 'desc' - default 'asc'
- `as_bytes`: in case the return io.BytesIO value should be in bytes

**Returns**:

io.BytesIO stream that will contain the response
example:
```python
bytes_io = iron_src_api.promote_api().get_advertiser_statistics('2020-10-03','2020-10-04',
[Metrics.Impressions,Metrics.Clicks,Metrics.Installs],
[Breakdowns.Application,Breakdowns.Day],response_format='csv')

line = bytes_io_r.readline()

while len(line) > 0:
    print(line)
    line = bytes_io_r.readline()

bytes_io_r.close()
```
<a id="promote_api.PromoteAPI.get_advertiser_statistics"></a>

#### get\_advertiser\_statistics

```python
def get_advertiser_statistics(start_date: str,
                              end_date: str,
                              metrics: Iterable[Metrics],
                              breakdowns: Iterable[Breakdowns] = None,
                              response_format: str = 'json',
                              count: int = None,
                              campaign_ids: Iterable[int] = None,
                              bundle_ids: Iterable[str] = None,
                              creative_ids: Iterable[int] = None,
                              country: Iterable[str] = None,
                              os_sys: Platform = None,
                              device_type: str = None,
                              ad_unit: AdUnits = None,
                              order: Union[Metrics, Breakdowns] = None,
                              direction: str = 'asc',
                              as_bytes=False) -> io.BytesIO
```

User Acquisition Reporting API

This method returns a BytesIO stream which will contain all responses from the api including pagination
The stream will contain new data all the time until there is no more.
in case of json, each response will be it's own json array

**Arguments**:

- `start_date`: report start date in the following format YYYY-MM-DD
- `end_date`: report end date in the following format YYYY-MM-DD
- `metrics`: list of report metrics. see [Metrics](#metrics)
- `breakdowns`: list of report breakdowns. see [Breakdowns](#breakdowns)
- `response_format`: report format type 'csv' or 'json' only - default 'json'
- `count`: maximum number of records in the report
- `campaign_ids`: list of campaign ids
- `bundle_ids`: list of bundle ids
- `creative_ids`: list of creative ids.
- `country`: list of country code in 2 letter country code,
as per [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
- `os_sys`: either 'ios' or 'android' see [Platform](#platform)
- `device_type`: either 'phone' or 'tablet'
- `ad_unit`: Ad Unit. see [AdUnits](#adunits)
- `order`: a breakdown or metric to order by
- `direction`: direction of order 'asc' or 'desc' - default 'asc'
- `as_bytes`: in case the return io.BytesIO value should be in bytes

**Returns**:

io.BytesIO stream that will contain the response
example:
```python
bytes_io = iron_src_api.promote_api().get_advertiser_statistics('2020-10-03','2020-10-04',
[Metrics.Impressions,Metrics.Clicks,Metrics.Installs],
[Breakdowns.Application,Breakdowns.Day],response_format='csv')

line = bytes_io_r.readline()

while len(line) > 0:
    print(line)
    line = bytes_io_r.readline()

bytes_io_r.close()
```
<a id="promote_api.PromoteAPI.get_universal_skan_report"></a>

#### get\_universal\_skan\_report

```python
async def get_universal_skan_report(date: str) -> str
```

returns a copy of the raw winning postbacks data from every network, directly from Apple.

**Arguments**:

- `date`: date of the report

**Returns**:

json with list of urls of the report

<a id="promote_api.PromoteAPI.get_bids_for_campaign"></a>

#### get\_bids\_for\_campaign

```python
def get_bids_for_campaign(campaign_id: int,
                          max_records: int = 1000,
                          as_bytes: bool = False) -> io.BytesIO
```

returns the current bids for a campaign

**Arguments**:

- `campaign_id`: the campaign id to fetch bids for.
- `max_records`: maximum number of records per response

**Returns**:

io.BytesIO stream that will contain the response

<a id="promote_api.PromoteAPI.update_bids"></a>

#### update\_bids

```python
async def update_bids(campaign_bids: Iterable[CampaignBidsList])
```

Update bids for campaigns

**Arguments**:

- `campaign_bids`: Array of [CampaignBidsList](#campaignbidslist). Each CampaignBidList contain bids for a campaign.

**Returns**:

array of all update requests and result message from the API.
response object example
```js 
{'campaignId':1234,'bidsUpdates':999,'msg':'Accepted'}
```

<a id="promote_api.PromoteAPI.delete_bids"></a>

#### delete\_bids

```python
async def delete_bids(campaign_bids: Iterable[CampaignBidsList])
```

Delete bids for campaigns

**Arguments**:

- `campaign_bids`: Array of [CampaignBidsList](#campaignbidslist). Each CampaignBidList contain bids for deletion.

**Returns**:

array of all delete requests and result message from the API.
response object example 
```js
{'campaignId':1234,'bidsUpdates':999,'msg':'Accepted'}
```

<a id="promote_api.PromoteAPI.get_audience_lists"></a>

#### get\_audience\_lists

```python
async def get_audience_lists()
```

return all audience lists for the account

**Returns**:

json array with all audience list
For example:
```js
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
```

<a id="promote_api.PromoteAPI.create_audience_list"></a>

#### create\_audience\_list

```python
async def create_audience_list(audience_meta_data: AudienceListMeta)
```

Creates new Audience List

**Arguments**:

- `audience_meta_data`: Meta data of the new audience list. See AudienceListMeta

**Returns**:

The API response

<a id="promote_api.PromoteAPI.delete_audience_list"></a>

#### delete\_audience\_list

```python
async def delete_audience_list(audience_list_id: str)
```

Delete an audience list

**Arguments**:

- `audience_list_id`: The audience list to delete in string

**Returns**:

The API response for deletion

<a id="promote_api.PromoteAPI.update_audience_list"></a>

#### update\_audience\_list

```python
async def update_audience_list(audience_list_data: AudienceListData)
```

Update Audience lists with device ids

**Arguments**:

- `audience_list_data`: Object containing audience lists ids and device ids. See AudienceListData

**Returns**:

The API response for update of the list

<a id="promote_api.PromoteAPI.get_titles"></a>

#### get\_titles

```python
async def get_titles(os_sys: Platform = None,
                     search_term: str = None,
                     request_id: str = None,
                     results_bulk_size: int = None,
                     page_number: int = None) -> dict
```

Get list of title

**Arguments**:

- `os_sys` (`Platform, optional`): Filter titles of a specified os, defaults to None.
- `search_term` (`str, optional`): Filter by the name or partial name of the title, defaults to None
- `request_id` (`str, optional`): Used for paginated request, defaults to None
- `results_bulk_size` (`int, optional`): Used for paginated request, defaults to None
- `page_number` (`int, optional`): Used for paginated request, defaults to None

**Raises**:

- `ValueError`: _description_

**Returns**:

`dict
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
}``: dictionary with array of the titles

<a id="promote_api.PromoteAPI.get_assets"></a>

#### get\_assets

```python
async def get_assets(asset_type: str = None,
                     title_id: int = None,
                     ids: Union[int, list] = None,
                     request_id: str = None,
                     page_number: int = None,
                     results_bulk_size: int = None) -> dict
```

Get List of assets

**Arguments**:

- `asset_type` (`str, optional`): Filter assets of a specified type. (Options: image, video, html, html_iec), defaults to None
- `title_id` (`int, optional`): Title Id to filter by, defaults to None
- `ids` (`Union[int, list], optional`): Asset id to filter by, defaults to None
- `request_id` (`str, optional`): Used for paginated requests, defaults to None
- `page_number` (`int, optional`): Used for paginated requests, defaults to None
- `results_bulk_size` (`int, optional`): Used for paginated requests, defaults to None

**Raises**:

- `ValueError`: 
- `Exception`: 

**Returns**:

`dict
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
       }`: JSON formatted array of the assets

<a id="promote_api.PromoteAPI.create_assets"></a>

#### create\_assets

```python
async def create_assets(title_id: int,
                        asset_type: str,
                        file_path: str,
                        file_name: str = None) -> dict
```

Create Asset to be used with Creative

**Arguments**:

- `title_id` (`int`): Title id that the asset belongs to.
- `asset_type` (`str`): The type of the asset. One of the following: image, video.
- `file_path` (`str`): Path to asset file. See details below.
- `file_name` (`str, optional`): Name to overwrite file's name, defaults to None

**Raises**:

- `ValueError`: _description_
- `Exception`: _description_

**Returns**:

`dict
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
Note: Videos longer than 30sec will have limited traffic`: json format with information on the uploaded asset

<a id="promote_api.PromoteAPI.get_creatives"></a>

#### get\_creatives

```python
async def get_creatives(creative_type: CreativeType = None,
                        title_id: int = None,
                        request_id: str = None,
                        page_number: int = None,
                        results_bulk_size: int = None)
```

Name - Mandatory - Data type - Description

**Arguments**:

- `creative_type`: - No - String - Filter creatives of a specified type. Use CreativeType class
- `title_id`: - No - Number - Filter creatives of a specific title.
- `request_id`: - No - String - Used for paginated requests.
- `page_number`: - No - Number - Used for paginated requests.
- `results_bulk_size`: - No - Number - Used for paginated requests.

<a id="promote_api.PromoteAPI.create_creatives"></a>

#### create\_creatives

```python
async def create_creatives(title_id: int,
                           creatives: Iterable[Creative]) -> dict
```

Name - Mandatory - Data type - Description

**Arguments**:

- `title_id`: - Yes - Int - The title ID.
- `creatives`: - Yes - List - List of creative objects. Use class Creative.

**Returns**:

`dict`: {"success": true,
"ids": [1,2,3]}

<a id="audience_list"></a>

# audience\_list

Module for Audience List

<a id="audience_list.AudienceListType"></a>

## AudienceListType

```python
class AudienceListType(enum.Enum)
```

Enum for Audience List Types

<a id="audience_list.AudienceListType.Suppression"></a>

#### Suppression

<a id="audience_list.AudienceListType.Targeting"></a>

#### Targeting

<a id="audience_list.AudienceListMeta"></a>

## AudienceListMeta

```python
class AudienceListMeta()
```

Create AudienceList Object

**Arguments**:

- `name` (`str`): Audience List name.
- `list_type` (`AudienceListType`): Audience List type. see AudienceListType.
- `description` (`str`): Audience List description.
- `bundle_id` (`str, optional`): Bundle id for the list, defaults to None
- `platform` (`Platform, optional`): platform for the audience list. See Platform., defaults to None

<a id="audience_list.AudienceListData"></a>

## AudienceListData

```python
class AudienceListData()
```

Class representing Audience list data

<a id="audience_list.AudienceListData.add_list_for_update"></a>

#### add\_list\_for\_update

```python
def add_list_for_update(audience_list_id: str)
```

Add audience list id to the update list

**Arguments**:

- `audience_list_id` (`str`): audience list id to update in string.

<a id="audience_list.AudienceListData.add_list_for_remove"></a>

#### add\_list\_for\_remove

```python
def add_list_for_remove(audience_list_id: str)
```

Add audience list id to the remove list

**Arguments**:

- `audience_list_id` (`str`): audience list id to remove in string.

<a id="audience_list.AudienceListData.add_devices"></a>

#### add\_devices

```python
def add_devices(devices: Union[str, list])
```

Adds devices to the list

**Arguments**:

- `devices` (`Union[str, list]`): either a device in string or list of devices


<a id="campaign_bids"></a>

# campaign\_bids

Module for Campaign Bids

<a id="campaign_bids.CampaignBid"></a>

## CampaignBid

```python
class CampaignBid()
```

Class representing a bid
Campaign Bid Object that represents a campaign bid

**Arguments**:

- `bid` (`float`): bid for campaign in float
- `country` (`str`): country for bid as per [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
- `application_id` (`int, optional`): application id for bid, defaults to -1


<a id="campaign_bids.CampaignBidsList"></a>

## CampaignBidsList

```python
class CampaignBidsList()
```
Create campaign bid object

**Arguments**:

- `campaign_id` (`int`): campaign id of the bid


<a id="campaign_bids.CampaignBidsList.add_bid"></a>

#### add\_bid

```python
def add_bid(bid: CampaignBid)
```

Adds a bid to the list

**Arguments**:

- `bid` (`CampaignBid`): [CampgianBid](#campaignbid) for the campaign bid object

<a id="campaign_bids.CampaignBidsList.get_campaign_id"></a>

#### get\_campaign\_id

```python
def get_campaign_id()
```

returns the campaign id

**Returns**:

campaign id.

<a id="creatives"></a>

# creatives

Module for Creatives

<a id="creatives.Creative"></a>

## Creative

```python
class Creative()
```

Class that represents Creative

**Arguments**:

- `name` (`str`): Name of the creative
- `creative_type` (`CreativeType`): [Type](#creativetype) of the creative.
- `language` (`str`): 2 letter e.g english=”EN”.
- `assets` (`Iterable[CreativeAsset], optional`): List of [CreativeAsset](#creativeasset), defaults to []

<a id="creatives.Creative.check_asset_compatible"></a>

#### check\_asset\_compatible

```python
def check_asset_compatible(asset: CreativeAsset) -> bool
```

Checks is CreativeAsset is compatible with the Creative

**Arguments**:

- `asset` (`CreativeAsset`): [Assets](#creativeasset) to check compatibility

**Returns**:

`bool`: True is compatible else False

<a id="creatives.Creative.is_validate"></a>

#### is\_validate

```python
def is_validate() -> bool
```

Check if creative is valid

**Returns**:

`bool`: True if the creative is valid with all it's assets

<a id="creatives.Creative.add_asset"></a>

#### add\_asset

```python
def add_asset(asset: CreativeAsset)
```

Adds asset to creative

**Arguments**:

- `asset` (`CreativeAsset`): [CreativeAsset](#createassets) to be added

**Raises**:

- `ValueError`: If Asset usage is wrong


<a id="creatives.CreativeAsset"></a>

## CreativeAsset

```python
class CreativeAsset()
```

Creative Asset for Creative usage

**Arguments**:

- `asset_id` (`int`): Asset ID for the creative asset see [get_assets](#getassets)
- `usage_type` (`UsageType`): [Usage type](#__init__.UsageType) of the creative




<br>
<a id="__init__.Metrics"></a>

## Metrics

```python
class Metrics(enum.Enum)
```

Metrics for promote reporting api


* ####  Impressions


* ####  Clicks


* ####  Completions


* ####  Installs


* ####  Spend


* ####  StoreOpens
<br>
<a id="__init__.AdUnits"></a>

## AdUnits

```python
class AdUnits(enum.Enum)
```

Ad Units for promote API


* ####  RewardedVideo


* ####  Interstitial


* ####  Banner


* ####  Offerwall
<br>
<a id="__init__.Breakdowns"></a>

## Breakdowns

```python
class Breakdowns(enum.Enum)
```

Breakdowns for promote reporting API


* ####  Day


* ####  Campaign


* ####  Title


* ####  Application


* ####  Country


* ####  OS


* ####  DeviceType


* ####  Creative


* ####  AdUnit


* ####  Creatives
<br>
<a id="__init__.Platform"></a>

## Platform

```python
class Platform(enum.Enum)
```

Platforms for promote API


* ####  iOS


* ####  Android

<a id="__init__.UsageType"></a>

<br>
## UsageType

```python
class UsageType(enum.Enum)
```

Usage Types for creative API


* ####  VIDEO


* ####  LEFT


* ####  MIDDLE


* ####  RIGHT


* ####  INTERACTIVE\_ENDCARD


* ####  PHONE\_PORTRAIT


* ####  PHONE\_LANDSCAPE


* ####  TABLET\_PORTRAIT


* ####  TABLET\_LANDSCAPE


<br>
<a id="__init__.CreativeType"></a>

## CreativeType

```python
class CreativeType(enum.Enum)
```

Creative types for creative API


* ####  VIDEO\_CAROUSEL


* ####  VIDEO\_INTERACTIVE\_ENDCARD


* ####  VIDEO\_FULLSCREEN