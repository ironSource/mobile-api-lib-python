# Table of Contents

* [monetize\_api](#monetize_api)
  * [AdUnitStatusMap](#adunitstatusmap-objects)
  * [AdUnitStatus](#adunitstatus-objects)
  * [AdUnits](#adunits-objects)
  * [Platform](#platform-objects)
  * [Metrics](#metrics-objects)
  * [Networks](#networks-objects)
  * [Breakdowns](#breakdowns-objects)
  * [MonetizeAPI](#monetize_api.MonetizeAPI)
    * [set\_credentials](#monetize_api.MonetizeAPI.set_credentials)
    * [get\_user\_ad\_revenue](#monetize_api.MonetizeAPI.get_user_ad_revenue)
    * [get\_impression\_ad\_revenue](#monetize_api.MonetizeAPI.get_impression_ad_revenue)
    * [get\_monetization\_data](#monetize_api.MonetizeAPI.get_monetization_data)
    * [get\_apps](#monetize_api.MonetizeAPI.get_apps)
    * [add\_temporary\_app](#monetize_api.MonetizeAPI.add_temporary_app)
    * [add\_app](#monetize_api.MonetizeAPI.add_app)
    * [get\_instances](#monetize_api.MonetizeAPI.get_instances)
    * [add\_instances](#monetize_api.MonetizeAPI.add_instances)
    * [delete\_instance](#monetize_api.MonetizeAPI.delete_instance)
    * [update\_instances](#monetize_api.MonetizeAPI.update_instances)
    * [get\_mediation\_groups](#monetize_api.MonetizeAPI.get_mediation_groups)
    * [create\_mediation\_group](#monetize_api.MonetizeAPI.create_mediation_group)
    * [update\_mediation\_group](#monetize_api.MonetizeAPI.update_mediation_group)
    * [delete\_mediation\_group](#monetize_api.MonetizeAPI.delete_mediation_group)
    * [get\_placements](#monetize_api.MonetizeAPI.get_placements)
    * [add\_placements](#monetize_api.MonetizeAPI.add_placements)
    * [delete\_placements](#monetize_api.MonetizeAPI.delete_placements)
    * [update\_placements](#monetize_api.MonetizeAPI.update_placements)
* [placement\_config](#placement_config)
  * [Capping](#placement_config.Capping)
  * [Pacing](#placement_config.Pacing)
  * [Placement](#placement_config.Placement)
* [mediation\_group\_priority](#mediation_group_priority)
  * [TierType](#mediation_group_priority.TierType)
    * [MANUAL](#mediation_group_priority.TierType.MANUAL)
    * [SORT\_BY\_CPM](#mediation_group_priority.TierType.SORT_BY_CPM)
    * [OPTIMIZED](#mediation_group_priority.TierType.OPTIMIZED)
    * [BIDDERS](#mediation_group_priority.TierType.BIDDERS)
  * [MediationGroupTier](#mediation_group_priority.MediationGroupTier)
    * [add\_instances](#mediation_group_priority.MediationGroupTier.add_instances)
    * [get\_instance\_list](#mediation_group_priority.MediationGroupTier.get_instance_list)
    * [remove\_instance](#mediation_group_priority.MediationGroupTier.remove_instance)
    * [get\_tier\_type](#mediation_group_priority.MediationGroupTier.get_tier_type)
  * [MediationGroupPriority](#mediation_group_priority.MediationGroupPriority)
    * [set\_mediation\_group\_tier](#mediation_group_priority.MediationGroupPriority.set_mediation_group_tier)
    * [remove\_tier](#mediation_group_priority.MediationGroupPriority.remove_tier)
    * [remove\_bidders](#mediation_group_priority.MediationGroupPriority.remove_bidders)
    * [get\_bidders](#mediation_group_priority.MediationGroupPriority.get_bidders)
    * [get\_tiers](#mediation_group_priority.MediationGroupPriority.get_tiers)
* [instance\_config](#instance_config)
  * [InstanceConfig](#instance_config.InstanceConfig)
  * [IronSourceInstance](#instance_config.IronSourceInstance)
  * [IronSourceBidding](#instance_config.IronSourceBidding)
  * [AdColonyInstance](#instance_config.AdColonyInstance)
  * [AdColonyBidding](#instance_config.AdColonyBidding)
  * [AdMobInstance](#instance_config.AdMobInstance)
  * [AdManager](#instance_config.AdManager)
  * [AmazonInstance](#instance_config.AmazonInstance)
  * [ApplovinInstance](#instance_config.ApplovinInstance)
  * [ChartboostInstance](#instance_config.ChartboostInstance)
  * [CrossPromotionBidding](#instance_config.CrossPromotionBidding)
  * [CSJInstance](#instance_config.CSJInstance)
  * [DirectDeals](#instance_config.DirectDeals)
  * [FacebookInstance](#instance_config.FacebookInstance)
  * [FacebookBidding](#instance_config.FacebookBidding)
  * [FyberInstance](#instance_config.FyberInstance)
  * [HyperMXInstance](#instance_config.HyperMXInstance)
  * [InMobiInstance](#instance_config.InMobiInstance)
  * [InMobiBidding](#instance_config.InMobiBidding)
  * [LiftoffInstance](#instance_config.LiftoffInstance)
  * [MaioInstance](#instance_config.MaioInstance)
  * [MediaBrixInstance](#instance_config.MediaBrixInstance)
  * [MyTarget](#instance_config.MyTarget)
  * [TapJoyInstance](#instance_config.TapJoyInstance)
  * [TapJoyBidding](#instance_config.TapJoyBidding)
  * [PangleInstance](#instance_config.PangleInstance)
  * [PangleBidding](#instance_config.PangleBidding)
  * [UnityAdsInstance](#instance_config.UnityAdsInstance)
  * [SmaatoInstance](#instance_config.SmaatoInstance)
  * [SnapInstance](#instance_config.SnapInstance)
  * [SuperAwesomeInstance](#instance_config.SuperAwesomeInstance)
  * [TencentInstance](#instance_config.TencentInstance)
  * [YahooBidding](#instance_config.YahooBidding)
  * [VungleInstance](#instance_config.VungleInstance)
  * [VungleBidding](#instance_config.VungleBidding)

<a id="monetize_api"></a>

# monetize\_api

IronSource Monetize API

<a id="monetize_api.MonetizeAPI"></a>

## MonetizeAPI Objects

```python
class MonetizeAPI()
```

IronSource Monetize API

<a id="monetize_api.MonetizeAPI.set_credentials"></a>

#### set\_credentials

```python
def set_credentials(user: str, token: str, secret: str)
```

sets the API credentials

**Arguments**:

- `user` (`str`): - user name from the platform
- `token` (`str`): - token from the platform
- `secret` (`str`): - secret from the platform

<a id="monetize_api.MonetizeAPI.get_user_ad_revenue"></a>

#### get\_user\_ad\_revenue

```python
async def get_user_ad_revenue(date: str,
                              application_key: str,
                              stream: bool = False) -> Union[str, io.BytesIO]
```

Get User Ad Revenue per application key

**Arguments**:

- `date` (`str`): - date in 'YYYY-MM-DD' format
- `application_key` (`str`): - the application key for which user ad revenue is being requested
- `stream` (`bool`): - (Defaults - False) if true stream will be returned

**Returns**:

user ad revenue as string or byte stream

<a id="monetize_api.MonetizeAPI.get_impression_ad_revenue"></a>

#### get\_impression\_ad\_revenue

```python
async def get_impression_ad_revenue(
        date: str,
        application_key: str,
        stream: bool = False) -> Union[str, io.BytesIO]
```

Impressions level Ad Revenue per application

**Arguments**:

- `date` (`str`): - date in 'YYYY-MM-DD' format
- `application_key`: - the application key for which user ad revenue is being requested
- `application_key`: str
- `stream` (`bool`): - (Defaults - False) if true stream will be returned

**Returns**:

Impression level ad revenue as string or byte stream

<a id="monetize_api.MonetizeAPI.get_monetization_data"></a>

#### get\_monetization\_data

```python
async def get_monetization_data(
        start_date: str,
        end_date: str,
        application_key: str = None,
        country: str = None,
        ad_units: AdUnits = None,
        ad_source: Networks = None,
        metrics: Iterable[Metrics] = None,
        breakdowns: Iterable[Breakdowns] = None) -> dict
```

Get monetization reporting

**Arguments**:

- `start_date` (`str`): Report start date in the following format YYYY-MM-DD
- `end_date` (`str`): Report end date in the following format YYYY-MM-DD
- `application_key` (`str, optional`): The application key for the report
- `country` (`str, optional`): Country code in 2 letter country code,
as per `[ISO 3166-1 Alpha-2] <https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>`_.
- `ad_units` (`AdUnits, optional`): Filter for specific [AdUnit](#adunits-objects) (RewardedVideo, Interstitial, Banner, Offerwall)
- `ad_source` (`Networks, optional`): Filter for specific Ad Source - [network](#networks-objects).
- `metrics` (`Iterable[Metrics], optional`): List of [metrics](#metrics-objects) see [supported breakdown and metrics](https://developers.ironsrc.com/ironsource-mobile/air/supported-breakdown-metric/)
- `breakdowns` (`Iterable[Breakdowns], optional`): List of [breakdowns](#breakdowns-objects) see [supported breakdown and metrics](https://developers.ironsrc.com/ironsource-mobile/air/supported-breakdown-metric/)

**Returns**:

None if there was an error fetching monetization data or dictionary with the data

<a id="monetize_api.MonetizeAPI.get_apps"></a>

#### get\_apps

```python
async def get_apps() -> dict
```

Get list of apps

**Returns**:

`dict`: dictionary of list of apps from the account

<a id="monetize_api.MonetizeAPI.add_temporary_app"></a>

#### add\_temporary\_app

```python
async def add_temporary_app(app_name: str,
                            platform: Platform,
                            coppa: bool,
                            ad_unit_status: AdUnitStatusMap = None,
                            ccpa: bool = None)
```

Adds a temporary app

**Arguments**:

- `app_name` (`str`): Application's name
- `platform` (`Platform`): Application's platform from Platform
- `coppa` (`bool`): The COPPA settings of the application (True/False)
- `ad_unit_status` (`AdUnitStatusMap`): Ad Unit status map see [AdUnitStatusMap](#adunitstatusmap-objects)
- `ccpa` (`bool`): The CCPA settings of the application (True/False)

**Returns**:

dict with new application key

<a id="monetize_api.MonetizeAPI.add_app"></a>

#### add\_app

```python
async def add_app(app_store_url: str,
                  taxonomy: str,
                  coppa: bool,
                  ad_unit_status: AdUnitStatusMap = None,
                  ccpa: bool = None)
```

Adds application which is already live in the store

**Arguments**:

- `app_store_url` (`str`): iOS / Android app store url for the application
- `taxonomy` (`str`): the application sub-genre - directory of valid labels: <https://developers.is.com/ironsource-mobile/air/taxonomy-2> \n
- `coppa` (`bool`): The COPPA settings of the application (True/False)
- `ad_unit_status` (`AdUnitStatusMap`): Ad Unit status map see [AdUnitStatusMap](#adunitstatusmap-objects)
- `ccpa` (`bool`): The CCPA settings of the application (True/False)

**Returns**:

dict with new application key

<a id="monetize_api.MonetizeAPI.get_instances"></a>

#### get\_instances

```python
async def get_instances(application_key: str) -> dict
```

Get Instances list for a given application key

**Arguments**:

- `application_key` (`str`): application key to get instances for

**Returns**:

`dict`: return JSON format list of the instances

<a id="monetize_api.MonetizeAPI.add_instances"></a>

#### add\_instances

```python
async def add_instances(application_key: str,
                        instances: Iterable[InstanceConfig])
```

Adds new instances to an app

**Arguments**:

- `application_key` (`str`): Application Key to add instance to.
- `instances` (`Iterable[InstanceConfig]`): List of [InstanceConfigs](#ironsourceinstance-objects) to be add.

**Returns**:

dict with all the instances of the app

<a id="monetize_api.MonetizeAPI.delete_instance"></a>

#### delete\_instance

```python
async def delete_instance(application_key: str, instance_id: int)
```

Deletes instance from application

**Arguments**:

- `application_key` (`str`): Application key to delete instance from
- `instance_id` (`int`): instance id to delete

**Returns**:

return list of all instances belongs to the ap

<a id="monetize_api.MonetizeAPI.update_instances"></a>

#### update\_instances

```python
async def update_instances(application_key: str,
                           instances: Iterable[InstanceConfig])
```

Updates instances for an application

**Arguments**:

- `application_key` (`str`): Application key to update instances for
- `instances` (`Iterable[InstanceConfig]`): list of [instances](#ironsourceinstance-objects) to update (instance must contain instance id)

**Returns**:

list of all instances

<a id="monetize_api.MonetizeAPI.get_mediation_groups"></a>

#### get\_mediation\_groups

```python
async def get_mediation_groups(application_key: str)
```

returns mediation groups for an application

**Arguments**:

- `application_key` (`str`): application key to fetch mediation groups

**Returns**:

list of mediation groups

<a id="monetize_api.MonetizeAPI.create_mediation_group"></a>

#### create\_mediation\_group

```python
async def create_mediation_group(
        application_key: str,
        ad_unit: AdUnits,
        group_name: str,
        group_countries: Iterable[str],
        group_position: int = None,
        group_segment: int = None,
        ad_source_priority: MediationGroupPriority = None)
```

Creates new mediation group for an application

**Arguments**:

- `application_key` (`str`): Application key to create new mediation group for
- `ad_unit` (`AdUnits`): Ad unit to create mediation group for (see [AdUnits](#adunits-objects))
- `group_name` (`str`): Group's name
- `group_countries` (`Iterable[str]`): List of group countries in [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
- `group_position` (`int, optional`): Position of the group in the groups list, defaults to None
- `group_segment` (`int, optional`): Segment ID attached to the group, defaults to None
- `ad_source_priority` (`MediationGroupPriority, optional`): AdSource and their priority in the group (see [MediationGroupPriority](#mediationgrouppriority-objects)), defaults to None

**Raises**:

- `Exception`: When API error occurs

**Returns**:

`dict`: list of groups belongs to the app in json format

<a id="monetize_api.MonetizeAPI.update_mediation_group"></a>

#### update\_mediation\_group

```python
async def update_mediation_group(
        application_key: str,
        group_id: int,
        group_name: str = None,
        group_countries: Iterable[str] = None,
        group_segments: int = None,
        ad_source_priority: MediationGroupPriority = None)
```

Updates mediation group for an app

**Arguments**:

- `application_key` (`str`): Application key to update group for
- `group_id` (`int`): Id of the group to update
- `group_name` (`str`): (optional) - Group name
- `group_countries` (`Iterable[str]`): (optional) -  List of group countries in
[ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
- `group_segments`: (`int, optional`) Group segment to update
- `ad_source_priority`: (`MediationGroupPriority, optional`) Ad Sources and their priority in the group (see [MediationGroupPriority](#mediationgrouppriority-objects))

**Returns**:

List of group for the application after the changes

<a id="monetize_api.MonetizeAPI.delete_mediation_group"></a>

#### delete\_mediation\_group

```python
async def delete_mediation_group(application_key: str, group_id: int)
```

Deletes group for an application

**Arguments**:

- `application_key` (`str`): Application key to delete the group for
- `group_id` (`int`): The group ID to delete

**Returns**:

List of group for the application after the changes

<a id="monetize_api.MonetizeAPI.get_placements"></a>

#### get\_placements

```python
async def get_placements(application_key: str) -> dict
```

Get list of placements

**Arguments**:

- `application_key` (`str`): Application key for placements

**Returns**:

`dict`: json list of placements from the application

<a id="monetize_api.MonetizeAPI.add_placements"></a>

#### add\_placements

```python
async def add_placements(application_key: str,
                         placements: Iterable[Placement]) -> dict
```

Create new placements, include capping and pacing setup, in your application account

**Arguments**:

- `application_key` (`str`): Application key of the app
- `placements` (`Iterable[Placement]`): Array (list) of [placements](#placement-objects) to be added/created

**Returns**:

`json`: placement identifier - This parameter is not shown in the ironSource platform and you can retrieve it using the get_placements method. You will need to use the id when editing/deleting placements.

<a id="monetize_api.MonetizeAPI.delete_placements"></a>

#### delete\_placements

```python
async def delete_placements(application_key: str, ad_unit: AdUnits,
                            placement_id: int) -> str
```

Archive existing placements in your applications

**Arguments**:

- `application_key` (`str`): Application key to delete placement from
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) type
- `placement_id` (`int`): placement id to delete

**Returns**:

return `True` if successful

<a id="monetize_api.MonetizeAPI.update_placements"></a>

#### update\_placements

```python
async def update_placements(application_key: str,
                            placements: Iterable[Placement])
```

Updates placements for an application

**Arguments**:

- `application_key` (`str`): Application key to update placements for
- `placements` (`Iterable[Placement]`): list of [placements](#placement-objects) to update (placement must contain placement id)

**Returns**:

`True` if successful

<a id="placement_config"></a>

# placement\_config

Module for creating placements object

<a id="placement_config.Capping"></a>

## Capping Objects

```python
class Capping()
```

Capping Class

**Arguments**:

- `limit` (`int`): Capping limit (max 1000).
- `interval` (`str`): Capping interval: 'd' - days or 'h' - hours
- `enabled` (`bool`): True is enabled, False is disabled.

**Raises**:

- `TypeError`: When wrong type was set
- `ValueError`: when limit or interval values are wrong

<a id="placement_config.Pacing"></a>

## Pacing Objects

```python
class Pacing()
```

Pacing Class

**Arguments**:

- `minutes` (`float`): Minimum gap in minutes between ad delivery (max 1000).
- `enabled` (`bool`): True is enabled, False is disabled.

**Raises**:

- `TypeError`: when enabled type is wrong.

<a id="placement_config.Placement"></a>

## Placement Objects

```python
class Placement()
```

Placement Object


**Arguments**:

- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) for placement
- `ad_delivery` (`bool`): Ad delivery is turned on or off
- `name` (`str, optional`): placement unique name - only required for add_placements method
- `placement_id` (`int, optional`): Placement unique identifier - not used for add_placements method
- `item_name` (`str, optional`): Reward name (max 30 chars) - rewardedVideo only
- `reward_amount` (`int, optional`): Amount of items to gift for a single ad view (max 2000000000) - rewardedVideo only
- `capping` (`Capping, optional`): [Capping](#capping-objects) for placement, defaults to None
- `pacing` (`Pacing, optional`): [pacing](#pacing-objects) for placement, defaults to None

**Raises**:

- `ValueError`: 
- `TypeError`: 

<a id="mediation_group_priority"></a>

# mediation\_group\_priority

Module for Mediation Group Tier Priority

<a id="mediation_group_priority.TierType"></a>

## TierType Objects

```python
class TierType(enum.Enum)
```

Enum representing different tier types for mediation group

<a id="mediation_group_priority.TierType.MANUAL"></a>

* #### MANUAL

<a id="mediation_group_priority.TierType.SORT_BY_CPM"></a>

* #### SORT\_BY\_CPM

<a id="mediation_group_priority.TierType.OPTIMIZED"></a>

* #### OPTIMIZED

<a id="mediation_group_priority.TierType.BIDDERS"></a>

* #### BIDDERS

<a id="mediation_group_priority.MediationGroupTier"></a>

## MediationGroupTier Objects

```python
class MediationGroupTier()
```

Mediation Group Tier

<a id="mediation_group_priority.MediationGroupTier.add_instances"></a>

#### add\_instances

```python
def add_instances(network: Networks,
                  instance_id: int,
                  rate: int = None,
                  position: int = None,
                  capping: int = None)
```

Adds instance to group Tier

**Arguments**:

- `network`: a network from [Networks](#__init__.Networks)
- `instance_id`: ID of the instance for the network (see MonetizeAPI().get_instances())
- `rate`: Optional: overrides the cpm of the instance with rate
- `position`: Optional: The position of the instance in the waterfall, only for Manual tier type
- `capping`: Optional: Set capping for the instance per session

<a id="mediation_group_priority.MediationGroupTier.get_instance_list"></a>

#### get\_instance\_list

```python
def get_instance_list() -> list
```

Returns list of instances in the tier

<a id="mediation_group_priority.MediationGroupTier.remove_instance"></a>

#### remove\_instance

```python
def remove_instance(network: Networks, instance_id: int)
```

Removes instance from the tier.

**Arguments**:

- `network`: The [Network](#__init__.Networks) of the instance to remove.
- `instance_id`: Instance ID to remove.

<a id="mediation_group_priority.MediationGroupTier.get_tier_type"></a>

#### get\_tier\_type

```python
def get_tier_type() -> TierType
```

**Returns**:

the tier type of the group

<a id="mediation_group_priority.MediationGroupPriority"></a>

## MediationGroupPriority Objects

```python
class MediationGroupPriority()
```

Class representing a groups priority of tiers


<a id="mediation_group_priority.MediationGroupPriority.set_mediation_group_tier"></a>

#### set\_mediation\_group\_tier

```python
def set_mediation_group_tier(group_tier: MediationGroupTier,
                             position: int) -> bool
```

sets group tier in specific place in the group (tier1, tier2, tier3)

**Arguments**:

- `group_tier`: [MediationGroupTier](#mediationgrouptier-objects) to be added to the group tier list
- `position`: The Position of the tier (0-2), Ignored in case of bidding tier.

**Returns**:

true upon successful addition of the tier to the group list.

<a id="mediation_group_priority.MediationGroupPriority.remove_tier"></a>

#### remove\_tier

```python
def remove_tier(position: int)
```

Removes tier from the group

**Arguments**:

- `position`: position of the tier to be removed (0-2)

<a id="mediation_group_priority.MediationGroupPriority.remove_bidders"></a>

#### remove\_bidders

```python
def remove_bidders()
```

Removes bidders from the group

<a id="mediation_group_priority.MediationGroupPriority.get_bidders"></a>

#### get\_bidders

```python
def get_bidders()
```

Returns groups bidders list

<a id="mediation_group_priority.MediationGroupPriority.get_tiers"></a>

#### get\_tiers

```python
def get_tiers() -> Iterable[any]
```

Returns groups tiers list

<a id="instance_config"></a>

# instance\_config

<a id="instance_config.IronSourceInstance"></a>

## IronSourceInstance Objects

```python
class IronSourceInstance(IronSourceBase)
```

Create IronSource Instance

**Arguments**:

- `instance_name` (`str`): name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `application_key` (`str`): Application key for the instance
- `pricing` (`Dict[int, List[str]], optional`): dictionary of price and list of countries, defaults to None
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1

<a id="instance_config.IronSourceBidding"></a>

## IronSourceBidding Objects

```python
class IronSourceBidding(IronSourceBase)
```

Create IronSource bidding instance

**Arguments**:

- `instance_name` (`str`): name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `application_key` (`str`): Application key for the instance
- `pricing` (`Dict[int, List[str]], optional`): dictionary of price and list of countries, defaults to None
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1

<a id="instance_config.AdColonyInstance"></a>

## AdColonyInstance Objects

```python
class AdColonyInstance(AdColonyBase)
```

AdColony instance

**Arguments**:

- `instance_name` (`str`): name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): AdColony App ID
- `zone_id` (`str`): AdColony Zone ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.AdColonyBidding"></a>

## AdColonyBidding Objects

```python
class AdColonyBidding(AdColonyBase)
```

AdColony Bidding instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): AdColony App ID
- `zone_id` (`str`): AdColony Zone ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.AdMobInstance"></a>

## AdMobInstance Objects

```python
class AdMobInstance(InstanceConfig)
```

AdMob instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): AdMob App ID
- `ad_unit_id` (`str`): AdMob AdUnit ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.AdManager"></a>

## AdManager Objects

```python
class AdManager(InstanceConfig)
```

Ad Manager instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): AdManager App ID
- `ad_unit_id` (`str`): AdManager Ad Unit ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.AmazonInstance"></a>

## AmazonInstance Objects

```python
class AmazonInstance(InstanceConfig)
```

Amazon Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_key` (`str`): Amazon Application Key
- `ec` (`str`): Amazon EC
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.ApplovinInstance"></a>

## ApplovinInstance Objects

```python
class ApplovinInstance(InstanceConfig)
```

Applovin Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `sdk_key` (`str`): Applovin SDK Key
- `zone_id` (`str`): Applovin Zone ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.ChartboostInstance"></a>

## ChartboostInstance Objects

```python
class ChartboostInstance(InstanceConfig)
```

Chartboost Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Charboost App ID
- `app_signature` (`str`): Chartboost App Signature
- `ad_location` (`str`): Charboost Ad Location
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.CrossPromotionBidding"></a>

## CrossPromotionBidding Objects

```python
class CrossPromotionBidding(InstanceConfig)
```

Cross Promotion Bidding Instance"

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `traffic_id` (`str`): Cross Promotion traffic ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.CSJInstance"></a>

## CSJInstance Objects

```python
class CSJInstance(InstanceConfig)
```

CSJ Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): CSJ Application ID
- `slot_id` (`str`): CSJ Slot ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.DirectDeals"></a>

## DirectDeals Objects

```python
class DirectDeals(InstanceConfig)
```

Direct Deals Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `traffic_id` (`str`): Direct Deal Traffic ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.FacebookInstance"></a>

## FacebookInstance Objects

```python
class FacebookInstance(FacebookBase)
```

Facebook Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Facebook App ID
- `user_access_token` (`str`): Facebook User Access Token
- `placement_id` (`str`): Facebook Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.FacebookBidding"></a>

## FacebookBidding Objects

```python
class FacebookBidding(FacebookBase)
```

Facebook Bidding Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Facebook Application ID
- `user_access_token` (`str`): Facebook User Access Token
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.FyberInstance"></a>

## FyberInstance Objects

```python
class FyberInstance(InstanceConfig)
```

Fyber Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Fyber Application ID
- `ad_spot_id` (`str`): Fyber Ad Spot ID
- `content_id` (`str`): Fyber Content ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.HyperMXInstance"></a>

## HyperMXInstance Objects

```python
class HyperMXInstance(InstanceConfig)
```

HyperMXInstance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `placement_id` (`str`): HyperMX Placement ID
- `distributor_id`: HyperMX Distributor Id
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.InMobiInstance"></a>

## InMobiInstance Objects

```python
class InMobiInstance(InMobiBase)
```

InMobi Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `placement_id` (`str`): InMobi Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.InMobiBidding"></a>

## InMobiBidding Objects

```python
class InMobiBidding(InMobiBase)
```

InMobi Bidding Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `placement_id` (`str`): InMobi Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.LiftoffInstance"></a>

## LiftoffInstance Objects

```python
class LiftoffInstance(InstanceConfig)
```

Liftoff Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): LiftOff Application ID
- `ad_unit_id` (`str`): LiftOff Ad Unit ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.MaioInstance"></a>

## MaioInstance Objects

```python
class MaioInstance(InstanceConfig)
```

Maio Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Maio App ID
- `media_id` (`str`): Maio Media ID
- `zone_id` (`str`): Maio ZoneID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.MediaBrixInstance"></a>

## MediaBrixInstance Objects

```python
class MediaBrixInstance(InstanceConfig)
```

MediaBrix Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): MediaBrix App ID
- `reporting_property` (`str`): MediaBrix Reporting property
- `zone` (`str`): MediaBrix Zone
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.MyTarget"></a>

## MyTarget Objects

```python
class MyTarget(InstanceConfig)
```

MyTarget Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `slot_id` (`str`): MyTarget Slot ID
- `placement_id` (`str`): MyTarget Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.TapJoyInstance"></a>

## TapJoyInstance Objects

```python
class TapJoyInstance(TapJoyBase)
```

TapJoy Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `sdk_key` (`str`): TapJoy SDK Key
- `api_key` (`str`): TapJoy API Key
- `placement_name` (`str`): TapJoy Placement Name
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.TapJoyBidding"></a>

## TapJoyBidding Objects

```python
class TapJoyBidding(TapJoyBase)
```

TapJoy Bidding Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `sdk_key` (`str`): TapJoy SDK Key
- `api_key` (`str`): TapJoy API Key
- `placement_name` (`str`): TapJoy Placement Name
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.PangleInstance"></a>

## PangleInstance Objects

```python
class PangleInstance(PangleBase)
```

Pangle Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Pangle App ID
- `slot_id` (`str`): Pangle Slot ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.PangleBidding"></a>

## PangleBidding Objects

```python
class PangleBidding(PangleBase)
```

Pangle Bidding Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Pangle App ID
- `slot_id` (`str`): Pangle Slot ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.UnityAdsInstance"></a>

## UnityAdsInstance Objects

```python
class UnityAdsInstance(InstanceConfig)
```

Unity Ads Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `source_id` (`str`): Unity Source ID
- `zone_id` (`str`): Unity Zone ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.SmaatoInstance"></a>

## SmaatoInstance Objects

```python
class SmaatoInstance(InstanceConfig)
```

Smaato Bidding Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `application_name` (`str`): Smaato Application Name
- `ad_space_id` (`str`): Smaato Ad Space ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.SnapInstance"></a>

## SnapInstance Objects

```python
class SnapInstance(InstanceConfig)
```

Snap Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Snap Application ID
- `slot_id` (`str`): Snap Slot ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.SuperAwesomeInstance"></a>

## SuperAwesomeInstance Objects

```python
class SuperAwesomeInstance(InstanceConfig)
```

SuperAwesome Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): SuperAwesome Application ID
- `placement_id` (`str`): SuperAwesome Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.TencentInstance"></a>

## TencentInstance Objects

```python
class TencentInstance(InstanceConfig)
```

Tencent Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Tencent Application ID
- `placement_id` (`str`): Tencent Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.YahooBidding"></a>

## YahooBidding Objects

```python
class YahooBidding(InstanceConfig)
```

Yahoo Bidding Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Yahoo Application ID
- `site_id` (`str`): Yahoo Site ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.VungleInstance"></a>

## VungleInstance Objects

```python
class VungleInstance(VungleBase)
```

Vungle Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Vungle Application ID
- `reporting_api_id` (`str`): Vungle Reporting API ID
- `placement_id` (`str`): Vungle Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="instance_config.VungleBidding"></a>

## VungleBidding Objects

```python
class VungleBidding(VungleBase)
```

Vungle Bidding Instance

**Arguments**:

- `instance_name` (`str`): Name for the instance
- `ad_unit` (`AdUnits`): [Ad Unit](#adunits-objects) that the instance will be used with
- `app_id` (`str`): Vungle Application ID
- `reporting_api_id` (`str`): Vungle Reporting API ID
- `placement_id` (`str`): Vungle Placement ID
- `status` (`bool, optional`): Instance is turned on or off, defaults to True
- `instance_id` (`int, optional`): instance id of the instance for update request, defaults to -1
- `rate` (`float, optional`): instance rate, defaults to None

<a id="__init__.AdUnitStatusMap"></a>

## AdUnitStatusMap Objects

```python
class AdUnitStatusMap(dict)
```

This class represents mapping of Ad Units to their active status
example:
```js
adunit_map = AdUnitStatusMap()
adunit_map[AdUnits.RewardedVideo] = AdUnitStatus.Live
```

<a id="__init__.AdUnitStatus"></a>

## AdUnitStatus Objects

```python
class AdUnitStatus(enum.Enum)
```

Enum class represents Ad Unit Status


* #### Live


* #### Off


* #### Test

<a id="__init__.AdUnits"></a>

## AdUnits Objects

```python
class AdUnits(enum.Enum)
```

Enum class represents Ad Unit


* #### RewardedVideo


* #### Interstitial


* #### Banner


* #### Offerwall

<a id="__init__.Platform"></a>

## Platform Objects

```python
class Platform(enum.Enum)
```

Enum class represents platfroms


* #### iOS


* #### Android

<a id="__init__.Metrics"></a>

## Metrics Objects

```python
class Metrics(enum.Enum)
```

Enum class represents reporting metrics


* #### impressions


* #### revenue


* #### eCPM


* #### appFillRate


* #### appRequests


* #### completions


* #### revenuePerCompletion


* #### appFills


* #### useRate


* #### activeUsers


* #### engagedUsers


* #### engagedUsersRate


* #### impressionsPerEngagedUser


* #### revenuePerActiveUser


* #### revenuePerEngagedUser


* #### clicks


* #### clickThroughRate


* #### completionRate


* #### adSourceChecks


* #### adSourceResponses


* #### adSourceAvailabilityRate


* #### sessions


* #### engagedSessions


* #### impressionsPerSession


* #### impressionPerEngagedSessions


* #### sessionsPerActiveUser

<a id="__init__.Networks"></a>

## Networks Objects

```python
class Networks(enum.Enum)
```

Enum class represents networks


* #### IronSource


* #### IronSourceBidding


* #### AppLovin


* #### AdColony


* #### AdColonyBidding


* #### AdMob


* #### AdManager


* #### Amazon


* #### Chartboost


* #### CrossPromotionBidding


* #### CSJ


* #### DirectDeals


* #### Facebook


* #### FacebookBidding


* #### Fyber


* #### HyperMX


* #### InMobi


* #### InMobiBidding


* #### LiftOff


* #### Maio


* #### MediaBrix


* #### MyTarget


* #### Pangle


* #### PangleBidding


* #### Smaato


* #### Snap


* #### SuperAwesome


* #### TapJoy


* #### TapJoyBidding


* #### Tencent


* #### UnityAds


* #### Vungle


* #### VungleBidding


* #### YahooBidding

<a id="__init__.Breakdowns"></a>

## Breakdowns Objects

```python
class Breakdowns(enum.Enum)
```

Enum class represents reporting breakdowns


* #### Date


* #### Application


* #### Platform


* #### Network


* #### AdUnits


* #### Instance


* #### Country


* #### Segment


* #### Placement


* #### IOSVersion


* #### ConnectionType


* #### SDKVersion


* #### AppVersion


* #### ATT


* #### IDFA


* #### ABTest
