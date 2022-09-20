"""This module is for IronSource Monetize API"""

import enum

# pylint: disable=invalid-name
class AdUnitStatusMap(dict):
    """This class represents mapping of Ad Units to their active status
        example:
        adunit_map = AdUnitStatusMap()
        adunit_map[AdUnits.RewardedVideo] = AdUnitStatus.Live
    """

    def __setitem__(self, key, value):
        """set AdUnit and it's status"""
        if not isinstance(key, AdUnits) or not isinstance(value, AdUnitStatus):
            raise TypeError('Key must be of type AdUnits and value must be of type AdUnitStatus')
        super().__setitem__(key, value)

    def get_formatted_map(self):
        """returns formatted dict of AdUnits and their status"""
        res_map = {}
        for key, value in self.items():
            res_map[key.value] = value.value
        return res_map


class AdUnitStatus(enum.Enum):
    """Enum class represents Ad Unit Status"""
    Live = 'Live'
    Off = 'Off'
    Test = 'Test'


class AdUnits(enum.Enum):
    """Enum class represents Ad Unit"""
    RewardedVideo = 'rewardedVideo'
    Interstitial = 'interstitial'
    Banner = 'banner'
    Offerwall = 'OfferWall'


class Platform(enum.Enum):
    """Enum class represents platfroms"""
    iOS = 'iOS'
    Android = 'Android'


class Metrics(enum.Enum):
    """Enum class represents reporting metrics"""
    impressions = 'impressions'
    revenue = 'revenue'
    eCPM = 'ecpm'
    appFillRate = 'appfillrate'
    appRequests = 'appRequests'
    completions = 'completions'
    revenuePerCompletion = 'revenuePerCompletion'
    appFills = 'appFills'
    useRate = 'useRate'
    activeUsers = 'activeUsers'
    engagedUsers = 'engagedUsers'
    engagedUsersRate = 'engagedUsersRate'
    impressionsPerEngagedUser = 'impressionsPerEngagedUser'
    revenuePerActiveUser = 'revenuePerActiveUser'
    revenuePerEngagedUser = 'revenuePerEngagedUser'
    clicks = 'clicks'
    clickThroughRate = 'clickThroughRate'
    completionRate = 'completionRate'
    adSourceChecks = 'adSourceChecks'
    adSourceResponses = 'adSourceResponses'
    adSourceAvailabilityRate = 'adSourceAvailabilityRate'
    sessions = 'sessions'
    engagedSessions = 'engagedSessions'
    impressionsPerSession = 'impressionsPerSession'
    impressionPerEngagedSessions = 'impressionPerEngagedSessions'
    sessionsPerActiveUser = 'sessionsPerActiveUser'


class Networks(enum.Enum):
    """Enum class represents networks"""
    IronSource = 'ironSource'
    IronSourceBidding = 'ironSourceBidding'
    AppLovin = 'AppLovin'
    AdColony = 'AdColony'
    AdColonyBidding = 'adColonyBidding'
    AdMob = 'AdMob'
    AdManager = 'AdManager'
    Amazon = 'Amazon'
    Chartboost = 'Chartboost'
    CrossPromotionBidding = 'crossPromotionBidding'
    CSJ = 'CSJ'
    DirectDeals = 'DirectDeals'
    Facebook = 'Facebook'
    FacebookBidding = 'facebookBidding'
    Fyber = 'Fyber'
    HyperMX = 'HyprMX'
    InMobi = 'InMobi'
    InMobiBidding = 'inMobiBidding'
    LiftOff = 'Liftoff Bidding'
    Maio = 'Maio'
    MediaBrix = 'mediaBrix'
    MyTarget = 'myTargetBidding'
    Pangle = 'Pangle'
    PangleBidding = 'pangleBidding'
    Smaato = 'smaatoBidding'
    Snap = 'Snap'
    SuperAwesome = 'SuperAwesomeBidding'
    TapJoy = 'TapJoy'
    TapJoyBidding = 'TapJoyBidding'
    Tencent = 'Tencent'
    UnityAds = 'UnityAds'
    Vungle = 'Vungle'
    VungleBidding = 'vungleBidding'
    YahooBidding = 'yahooBidding'


class Breakdowns(enum.Enum):
    """Enum class represents reporting breakdowns"""
    Date = 'date'
    Application = 'app'
    Platform = 'platform'
    Network = 'adSource'
    AdUnits = 'adUnits'
    Instance = 'instance'
    Country = 'country'
    Segment = 'segment'
    Placement = 'placement'
    IOSVersion = 'iosVersion'
    ConnectionType = 'connectionType'
    SDKVersion = 'sdkVersion'
    AppVersion = 'appVersion'
    ATT = 'att'
    IDFA = 'idfa'
    ABTest = 'abTest'
    