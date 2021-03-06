import urllib

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import url_concat

from tornado_virtuoso_client import settings

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

DEFAULT_FORMAT = "application/sparql-results+json"
URL_ENCODED = "application/x-www-form-urlencoded"
DEFAULT_CONTENT_TYPE = URL_ENCODED


class VirtuosoConnection(object):

    def __init__(self, io_loop=None):
        if hasattr(settings, "SPARQL_ENDPOINT"):
            self.endpoint_url = settings.SPARQL_ENDPOINT
        else:
            self.host = settings.SPARQL_ENDPOINT_HOST
            self.port = settings.SPARQL_ENDPOINT_PORT
            self.endpoint_url = self.host + ":" + str(self.port) + "/sparql"

        self.io_loop = io_loop or IOLoop.instance()
        self.client = AsyncHTTPClient(io_loop=io_loop)
        self._set_credentials()

    def _set_credentials(self):
        try:
            self.user = settings.SPARQL_ENDPOINT_USER
            self.password = settings.SPARQL_ENDPOINT_PASSWORD
            self.auth_mode = settings.SPARQL_ENDPOINT_AUTH_MODE
        except AttributeError:
            self.user = self.password = self.auth_mode = None

    @gen.engine
    def query(self, callback, query, *args, **kw):
        method = kw.get("method", "POST")
        result_format = kw.get("result_format", DEFAULT_FORMAT)
        content_type = DEFAULT_CONTENT_TYPE

        headers = {
            "Content-Type": content_type,
        }

        params = {
            "query": query,
            "format": result_format
        }

        url = self.endpoint_url

        if method == "GET":
            url = url_concat(url, params)
            body = None
        elif method == "POST":
            body = urllib.urlencode(params)

        request = HTTPRequest(url=url,
                              method=method,
                              headers=headers,
                              body=body,
                              auth_username=self.user,
                              auth_password=self.password,
                              auth_mode=self.auth_mode
                              )
        response = yield gen.Task(self.client.fetch, request)
        callback(response, *args, **kw)

    def status():
        raise NotImplementedError("not implemented")
