"""Module for Campaign Bids"""


from typing import Iterable


class CampaignBid:
    """Class representing a bid"""
    _bid: float
    _country: str
    _application_id = -1

    def __init__(self, bid: float, country: str, application_id: int = -1):
        """Campaign Bid Object that represents a campaign bid

        :param bid:  bid for campaign in float
        :type bid: float
        :param country: country for bid as per [ISO 3166-1 Alpha-2](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
        :type country: str
        :param application_id: application id for bid, defaults to -1
        :type application_id: int, optional
        """
        self._bid = bid
        self._country = country
        self._application_id = application_id

    def get_object(self):
        """

        :return: dictionary representing the campaign bid
        """
        obj = {
            'country': self._country,
            'bid': round(self._bid, 2)
        }
        if self._application_id != -1:
            obj['applicationId'] = self._application_id

        return obj


class CampaignBidsList:
    """Create campaign bid object

        :param campaign_id: campaign id of the bid
        :type campaign_id: int
    """
    _campaign_id: int
    _bids: Iterable[CampaignBid] = []

    def __init__(self, campaign_id: int):
        self._campaign_id = campaign_id
        self._bids = []

    def add_bid(self, bid: CampaignBid):
        """Adds a bid to the list

        :param bid: bid for the campaign bid object
        :type bid: CampaignBid
        """
        self._bids.append(bid)

    def get_campaign_id(self):
        """
        returns the campaign id
        :return: campaign id.
        """
        return self._campaign_id

    def get_object_for_update(self):
        """
        Dict object for the update bids API
        :return:
        """
        obj = {
            'bids': []
        }
        for bid in self._bids:
            obj['bids'].append(bid.get_object())
        obj['campaignId'] = self._campaign_id
        return obj

    def get_object_for_deletion(self):
        """
        Dict object for the delete bids API
        :return:
        """
        obj = {
            'bids': []
        }
        for bid in self._bids:
            bid_obj = bid.get_object()
            bid_obj.pop('bid')
            obj['bids'].append(bid_obj)

        obj['campaignId'] = self._campaign_id
        return obj
