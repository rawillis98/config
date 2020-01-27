#!/usr/bin/python
import os
import subprocess
import requests
import urllib.parse
from read_key import *
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl


class MyHandler(BaseHTTPRequestHandler):
    my_response = "You can close this page now."

    def do_GET(self):
        query = urllib.parse.urlsplit(self.path).query
        query_dict = urllib.parse.parse_qs(query)
        code = query_dict['code'][0]
        code = urllib.parse.unquote(code)
        TDAPI.set_code(code)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(MyHandler.my_response.encode("utf-8"))

    def do_POST(self):
        self.do_GET()


class TDAPI:
    code = ""
    refresh_token_file_name = '/home/alex/Documents/keys/td.refresh'
    pem_file = '/home/alex/Documents/keys/server.pem'

    def generate_pem(self):
        print("Generating pem")
        command = f"openssl req -new -x509 -keyout {TDAPI.pem_file} -out {TDAPI.pem_file} -days 365 -nodes" 
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print("Done generating pem")

    def __init__(self):
        # do we have a pem file?
        if not os.path.exists(TDAPI.pem_file):
            self.generate_pem()

        # do we have a refresh token?
        if os.path.exists(TDAPI.refresh_token_file_name):
            self.refresh_token = read_key(TDAPI.refresh_token_file_name)
            self.get_access_token_with_refresh(self.refresh_token)
        else:
            self.port = 4443
            self.get_auth_url()
            
            httpd = HTTPServer(('localhost', self.port), MyHandler)
            httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile=self.pem_file)
            while TDAPI.code == "":
                httpd.handle_request()

            assert TDAPI.code is not ""

            self.get_access_token_from_scratch(TDAPI.code).json()['access_token']

    def get_auth_url(self):
        redirect_uri = r'https://localhost:' + str(self.port)
        URLENCODED_REDIRECT_URI = urllib.parse.quote(redirect_uri)

        URLENCODED_Consumer_Key = '5YUDFBAZ1VDOZYN2IPI8WUBND0ACF8YP'
        auth_url = f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={URLENCODED_REDIRECT_URI}&client_id={URLENCODED_Consumer_Key}%40AMER.OAUTHAP"
        
        print("Log in to this URL: ")
        print(auth_url)
        return auth_url

    @staticmethod
    def save_str(fname, code):
        with open(fname, 'w') as f:
            f.write(code)

    @staticmethod
    def set_code(code):
        TDAPI.code = code

    def get_access_token_from_scratch(self, key):
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
        TDAPI.save_str(TDAPI.refresh_token_file_name, self.refresh_token)
        return request

    def get_access_token_with_refresh(self, refresh_token):
        endpoint = r'https://api.tdameritrade.com/v1/oauth2/token'
        parameters = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': '5YUDFBAZ1VDOZYN2IPI8WUBND0ACF8YP',
        }

        headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
        }

        request = requests.post(endpoint, data=parameters, headers=headers)
        self.access_token = request.json()['access_token']
        return request.json()
        

    def get_accounts(self, fields='positions,orders'):
        endpoint = r'https://api.tdameritrade.com/v1/accounts'
        parameters = {
                'fields': fields
        }

        headers = {
                'Authorization': f'Bearer {self.access_token}'
        }

        request = requests.get(endpoint, params=parameters, headers=headers)
        return request.json()
    
if __name__ == '__main__':
    td = TDAPI()
    a = td.get_accounts()
    a = a[0]
    a = a['securitiesAccount']
    a = a['positions']
    for position in a:
        print(position['instrument'])
