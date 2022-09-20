
# ironsource_api_python
![Test And Lint](https://github.com/ironSource/mobile-api-lib-python/actions/workflows/deploy.yml/badge.svg)

## Installation

This module is installed via pip:

```
pip install ironsrc_mobile_api
```

## Simple Example:
```python
import os
from ironsource_api.ironsource_api import IronSourceAPI
from ironsource_api.promote_api import Metrics, Breakdowns

ironsrc_api = IronSourceAPI()

ironsrc_api.set_credentials(API_USER, API_TOKEN,API_SECRET)

#Get Monetization Data
res = ironsrc_api.monetize_api().get_monetization_data(start_date='2020-01-01', end_date='2020-01-01')


#Get Advertiser Statistics
bytes_io = ironsrc_api.promote_api().get_advertiser_statistics('2020-10-03','2020-10-04',
        [Metrics.Impressions,Metrics.Clicks,Metrics.Installs],
        [Breakdowns.Application,Breakdowns.Day],response_format='csv')

line = bytes_io_r.readline()

while len(line) > 0:
    print(line)
    line = bytes_io_r.readline()

bytes_io_r.close()



```
####  Authentication
Before starting to use the API make sure to get the credentials from ironSource dashboard.
![Account Cred](https://developers.ironsrc.com/wp-content/uploads/2019/01/1-1.png)

And set the Access Key, Secret Key and Refresh Token: 
<a id="ironsource_api.IronSourceAPI.set_credentials"></a>

#### set\_credentials

```python
def set_credentials(user: str, token: str, secret: str)
```

sets credentials for the APIs


<br>
## Modules

* [IronSourceAPI](#ironsource_api.IronSourceAPI)
    * [monetize\_api](docs/monetize_api.md)
    * [promote\_api](docs/promote_api.md)


<br>

## Contributing:
Please follow contribution [guide](/CONTRIBUTING.md)

## Dependencies
* [requests](https://github.com/psf/requests)
* [httpx](https://github.com/encode/httpx)
* [pydash](https://github.com/dgilland/pydash)