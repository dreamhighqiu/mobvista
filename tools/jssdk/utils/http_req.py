# -*- coding: utf-8 -*-
'''
@author: redstar
'''
import json
import time
import urllib

import requests


_GET = "GET"
_POST = "POST"


class Request():

    def __init__(self, url, params={}, headers={}, json={}, data={}, method=_GET, verify=False, allow_redirects=False):

        self.url = url
        self.params = params
        self.headers = dict(headers, **{'User-Agent': 'python-requests/2.18.4'})
        self.json = json
        self.data = data
        self.method = method
        self.verify = verify
        self.allow_redirects = allow_redirects
        self.response = {
            'http_status': None,
            'body': {},
            'headers': {}
        }

    def __repr__(self):
        return '<SendRequest %r %r %r %r>' % (self.method, self.url, self.params, self.headers)

    def send_request(self, timeout=10.0, max_try=3):
        print("+++++++++++++++++++++++++++++Sending Request+++++++++++++++++++++++++++++\n")
        timestamp = 0
        max_try = 3
        while(max_try > 0):
            try:
                start = time.time()
                response = self.urlopen(timeout)
                timestamp = time.time() - start

                self.response['http_status'] = response.status_code
                self.response['headers'] = response.headers
                self.response['body'] = response.text
                self.response['history'] = response.history
                break

            except:
                if self.params is not None:
                    print "[Timeout]Got Exception Try Again...\n[URL] %s" % (self.url + urllib.urlencode(self.params))
                print("Timeout]Got Exception Try Again")
                max_try -= 1

        if max_try <= 0:
            raise Exception("Send http request timeout! Retry failed!")

        print "[URL] %s\n[Http Status] %s\t[Time Stamp] %s\n[Head] %s\n[Body] %s" % (response.url, response.status_code,
                                                                                     timestamp, response.headers, response.text)
        for redirect in self.response['history']:
            print "[Redirect History] %s\t[Http Status] %s" % (redirect.url, redirect.status_code)

        return self.response

    def urlopen(self, timeout):
        assert self.method in (_GET, _POST)
#         if self.params is None:
#             self.params = {}
#         self.params['tracking']='wow'


        if _GET == self.method:       
            return requests.get(self.url, params=self.params, headers=self.headers, verify=self.verify,
                                allow_redirects=self.allow_redirects, timeout=timeout)

        elif _POST == self.method:
            return requests.post(self.url, data=self.data, json=self.json, params=self.params, headers=self.headers, verify=self.verify,
                                 allow_redirects=self.allow_redirects, timeout=timeout)
