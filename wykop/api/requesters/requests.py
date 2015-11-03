from __future__ import absolute_import
import logging

from requests import request
from requests.exceptions import RequestException

from wykop.api.exceptions import WykopAPIError
from wykop.api.requesters.base import BaseRequester
from wykop.utils import dictmap, mimetype, force_text

log = logging.getLogger(__name__)


class RequestsRequester(BaseRequester):
    """
    Requests requester class
    """

    METHOD_GET = 'GET'
    METHOD_POST = 'POST'

    def make_request(self, url, data, headers, files):
        log.debug(" Fetching url: `%s` (POST: %s, headers: `%s`)" %
                  (str(url), str(data), str(headers)))
        try:
            method = self.METHOD_POST if data or files else self.METHOD_GET
            files = dictmap(lambda x: (x.name, x, mimetype(x.name)), files)
            req = request(method, url, data=data, headers=headers, files=files)
            return force_text(req.content)
        except RequestException as e:
            raise WykopAPIError(0, str(e.reason))
