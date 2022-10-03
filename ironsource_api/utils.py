"""
Utils package
"""
import sys
import gzip
import json
import os
import base64
from typing import Union
from urllib import request, parse
import io
from dataclasses import dataclass
import httpx

from ironsource_api import __version__

if sys.version_info >= (3, 8):
    # pylint: disable=ungrouped-imports
    from typing import get_args, get_origin
else:
    from typing_extensions import get_args, get_origin # pylint: disable=import-error


BARRIER_AUTH_URL = "https://platform.ironsrc.com/partners/publisher/auth"

@dataclass
class ResponseInterface:
    """interface for http response"""
    msg = ''
    error_code = -1

    def __init__(self):
        """init for ResponseInterface"""
        self.msg = ''
        self.error_code = -1


def get_basic_auth(username: str, secret: str) -> str:
    """

    :param username: username from ironsource platform
    :param secret: secret key from ironsource platform
    :return str: Basic Auth token
    """
    return base64.b64encode('{}:{}'.format(username, secret).encode('utf8')).decode('utf8')


async def get_bearer_auth(secret: str, token: str) -> str:
    """
    :param secret: secret key from ironsource platform
    :param token: token from ironsource platform
    :return str: temporary bearer token
    """
    uri = BARRIER_AUTH_URL
    options = {
        'headers': {
            'secretkey': secret,
            'refreshToken': token
        }
    }
    res = await execute_request(method='get', url=uri, **options)
    return res.msg.lstrip("\"").rstrip("\"")


async def execute_request(method: str, url: str, is_gzip=False, **kwargs) -> ResponseInterface:
    """
    execute http request
    :param method: http method type ('get','post','del','put'..)
    :param url: http request url
    :param is_gzip: is response is gzipped
    :param kwargs: args that defined by httpx
    :return ResponseInterface: ResponseInterface with err_code if exists, else -1 and msg as response body
    """
    response_obj = ResponseInterface()
    try:
        client = httpx.AsyncClient(timeout=60.0)
        client.headers['user-agent'] = f"{client.headers['user-agent']} IronSource - Python API Library {__version__}"
        res = await client.request(method=method, url=url, **kwargs)
        if res.status_code >= 400:
            response_obj.msg = res.text
            response_obj.error_code = res.status_code
            return response_obj
        response_obj.msg = res.text if not is_gzip else gzip.decompress(
            res.content)
        return response_obj

    except Exception as exception:
        response_obj.msg = str(exception)
        response_obj.error_code = 500
        return response_obj
    finally:
        if client and not client.is_closed:
            await client.aclose()


def execute_request_as_stream(url: str, is_gzip: bool) -> io.BytesIO:
    """
    return stream of data from a url
    :param url: url to open
    :param is_gzip: if response is gzipped the stream will be decompressed
    :return io.BytesIO: stream of bytes
    """
    try:
        req = request.Request(url,headers={"user-agent": f"{request.URLopener.version} IronSource - Python API Library {__version__}"})
        response = request.urlopen(req)
        if is_gzip:
            return gzip.GzipFile(fileobj=response)

        return response

    except Exception as exception:
        raise exception


# pylint: disable= too-many-branches
def execute_request_with_pagination(url: str, pipe_w: int, data_key: str, err_string: str, options: dict, as_bytes=False):
    """
    execute requests that it's response could have pagination and write the response to a pipe stream
    if response is of json format `data_key` will be used to extract the data out of the json.
    :param url: The url to execute request to
    :param pipe_w: fd where the pipe exists
    :param data_key: json key where the data should be extracted from
    :param err_string: In case of exception use this string as well
    :param options: http headers and query params
    :return:
    """
    client = httpx.Client(timeout=60.0)
    next_page: str = ''
    try:
        client.headers['user-agent'] = f"{client.headers['user-agent']} IronSource - Python API Library {__version__}"
        res = client.request(method='get', url=url, **options)

        if res.status_code >= 400:
            raise Exception('{}: Error Code: {} Error: {}'.format(
                err_string, res.status_code, res.text))
        if 'format' not in options['params'] or options['params']['format'] == 'json':
            if not res.text:
                os.close(pipe_w)
                return

            res_json = json.loads(res.text)
            data_to_write =  (json.dumps(res_json[data_key])+"\n").encode('utf-8')
            data_to_write = bytes(data_to_write,'utf-8') if as_bytes is True else data_to_write
            os.write(pipe_w, data_to_write)
            if 'paging' in res_json and 'next' in res_json['paging']:
                next_page = res_json['paging']['next']
            else:
                os.close(pipe_w)
                return

        elif options['params']['format'] == 'csv':
            if res.status_code == 204 and not res.text:
                os.close(pipe_w)
                return
            data_to_write = bytes(
                res.text,'utf-8') if as_bytes is True else res.text.encode('utf-8')
            os.write(pipe_w, data_to_write)

            if 'link' in res.headers:
                next_page = res.headers['link'].replace(
                    '<', '').replace('>; rel="next"', '')
            else:
                os.close(pipe_w)
                return

        if next_page:
            split_url = parse.urlsplit(next_page)
            new_params = dict(parse.parse_qsl(split_url.query))
            options['params'] = new_params
            url = split_url.scheme + '://' + split_url.netloc + split_url.path
            execute_request_with_pagination(
                url, pipe_w, data_key, err_string, options, as_bytes)

    except Exception as exception:
        raise Exception('{}: {}'.format(
            err_string, str(exception))) from exception
    finally:
        try:
            os.close(pipe_w)
        except OSError:
            pass


def check_instance(value, value_type, key):
    """returns True if value is of type value_type else raises TypeError for key"""
    if value or value == []:
        if get_origin(value_type) is Union:
            if not isinstance(value, get_args(value_type)):
                TypeError('{} must be type {}, not {}.'.format(
                    key, str(value_type), type(value)))
        elif not isinstance(value, value_type):
            TypeError('{} must be type {}, not {}.'.format(
                key, str(value_type), type(value)))
    elif not value:
        return False
    return True
