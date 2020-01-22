#!/usr/bin/python
import requests
import urllib.parse
from read_key import *
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = urllib.parse.urlsplit(self.path).query
        query_dict = urllib.parse.parse_qs(query)
        code = query_dict['code'][0]
        code = urllib.parse.unquote(code)
        TDAPI.set_code(code)
        return

def encode(s):
    return urllib.parse.quote(s)
def unencode(s):
    return urllib.parse.unquote(s)


class TDAPI:
    code = ""

    def __init__(self):
        print("getting auth url")
        self.port = 4443
        self.get_auth_url()
        
        httpd = HTTPServer(('localhost', self.port), MyHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='yourpemfile.pem')
        print(f"Listening on {self.port}")
        while TDAPI.code == "":
            httpd.handle_request()

        assert TDAPI.code is not ""

        self.get_access_token(TDAPI.code).json()['access_token']

        print(self.get_account(self.access_token))
    

    def get_auth_url(self):
        redirect_uri = r'https://localhost:' + str(self.port)
        URLENCODED_REDIRECT_URI = urllib.parse.quote(redirect_uri)

        URLENCODED_Consumer_Key = '5YUDFBAZ1VDOZYN2IPI8WUBND0ACF8YP'
        auth_url = f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={URLENCODED_REDIRECT_URI}&client_id={URLENCODED_Consumer_Key}%40AMER.OAUTHAP"
        
        print("Log in to this URL: ")
        print(auth_url)
        return auth_url

    @staticmethod
    def save_code(code):
        with open('td.code', 'w') as f:
            f.write(TDAPI.code)

    @staticmethod
    def set_code(code):
        TDAPI.code = code

    def get_access_token(self, key):
        endpoint = r'https://api.tdameritrade.com/v1/oauth2/token'
        parameters = {
                'grant_type': 'authorization_code',
                'access_type': 'offline',
                'code': key,
                'client_id': '5YUDFBAZ1VDOZYN2IPI8WUBND0ACF8YP',
                'redirect_uri': r'https://localhost:' + str(self.port)
        }

        headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
        }

        request = requests.post(endpoint, data=parameters, headers=headers)
        self.access_token = request.json()['access_token']
        self.refresh_token = request.json()['refresh_token']
        return request

    def get_account(self, access_token):
        endpoint = r'https://api.tdameritrade.com/v1/accounts'
        parameters = {
                'fields': 'positions,orders'
        }

        headers = {
                'Authorization': f'Bearer {access_token}'
        }

        request = requests.get(endpoint, data=parameters, headers=headers)
        return request.json()
    
if __name__ == '__main__':
    td = TDAPI()
