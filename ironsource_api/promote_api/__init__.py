"""
IronSource Promote API Module
"""
import enum

# pylint: disable=invalid-name
class Metrics(enum.Enum):
    """
    Metrics for promote reporting api
    """
    Impressions = 'impressions'
    Clicks = 'clicks'
    Completions = 'completions'
    Installs = 'installs'
    Spend = 'spend'
    StoreOpens = 'storeOpens'


class AdUnits(enum.Enum):
    """
    Ad Units for promote API
    """
    RewardedVideo = 'rewardedVideo'
    Interstitial = 'interstitial'
    Banner = 'banner'
    Offerwall = 'offerWall'


class Breakdowns(enum.Enum):
    """
    Breakdowns for promote reporting API
    """
    Day = 'day'
    Campaign = 'campaign'
    Title = 'title'
    Application = 'application'
    Country = 'country'
    OS = 'os'
    DeviceType = 'deviceType'
    Creative = 'creative'
    AdUnit = 'adUnit'
    Creatives = 'creatives'


class Platform(enum.Enum):
    """
    Platforms for promote API
    """
    iOS = 'ios'
    Android = 'android'


# class CreativeType(enum.Enum):
#     """
#     Creative types for creative API
#     Options: VideoAndCarousel, VideoAndIEC, VideoAndFullscreen, Playable, InteractiveVideo
#     """
#     VIDEO_CAROUSEL = 'videoAndCarousel'
#     VIDEO_INTERACTIVE_ENDCARD = 'videoAndInteractiveEndCard'
#     VIDEO_FULLSCREEN = 'videoAndFullScreen'


class UsageType(enum.Enum):
    """Usage Types for creative API"""
    VIDEO = 'video'
    LEFT = 'left'
    MIDDLE = 'middle'
    RIGHT = 'right'
    INTERACTIVE_ENDCARD = 'interactiveEndCard'
    PHONE_PORTRAIT = 'phonePortrait'
    PHONE_LANDSCAPE = 'phoneLandscape'
    TABLET_PORTRAIT = 'tabletPortrait'
    TABLET_LANDSCAPE = 'tabletLandscape'


class CreativeType(enum.Enum):
    """
    Creative types for creative API
    Options: VideoAndCarousel, VideoAndIEC, VideoAndFullscreen, Playable, InteractiveVideo
    """
    VIDEO_CAROUSEL = {
        'name':'videoAndCarousel',
        'usage_types':{
                'mandatory':[UsageType.VIDEO,UsageType.LEFT,UsageType.MIDDLE,UsageType.RIGHT]
            }
        }
    VIDEO_INTERACTIVE_ENDCARD = {
        'name':'videoAndInteractiveEndCard',
        'usage_types':{
            'mandatory':[UsageType.VIDEO,UsageType.INTERACTIVE_ENDCARD]
            }
        }
    VIDEO_FULLSCREEN = {
        'name':'videoAndFullScreen',
        'usage_types':{
            'mandatory':[UsageType.VIDEO,UsageType.PHONE_PORTRAIT,UsageType.PHONE_LANDSCAPE],
            'optional':[UsageType.TABLET_PORTRAIT,UsageType.TABLET_LANDSCAPE]
            }
        }


REPORTING_API = 'https://api.ironsrc.com/advertisers/v2/reports'

MULTI_BID_API = 'https://api.ironsrc.com/advertisers/v2/multibid'

AUDIENCE_API_SHOW = 'https://platform-api.supersonic.com/audience/api/show'

AUDIENCE_API_CREATE = 'https://platform-api.supersonic.com/audience/api/create'

AUDIENCE_API_DELETE = 'https://platform-api.supersonic.com/audience/api/{}'

AUDIENCE_API_UPDATE = 'https://platform-api.supersonic.com/audience/api'

TITLE_API = 'https://api.ironsrc.com/advertisers/v2/titles'

ASSETS_API = 'https://api.ironsrc.com/advertisers/v2/assets'

CREATIVES_API = 'https://api.ironsrc.com/advertisers/v2/creatives'

SKAN_REPORTING_API = 'https://api.ironsrc.com/advertisers/v4/reports/skan'

UNIVERSAL_SKAN_API = 'https://platform.ironsrc.com/partners/postback/v1'
