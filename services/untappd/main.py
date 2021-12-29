from __future__ import print_function
from flask import Flask, request, jsonify
from requests.models import HTTPError
import requests
import sys

app = Flask(__name__)

class Untappd:

    ACCESS_TOKEN = '' 
    API_HOST = 'https://api.untappd.com/v4'
    USER_PATH = '/user/info/CamXC'
    USER_BEER_PATH = '/user/beers/CamXC'

    def __init__(self):

        pass

    def make_request(self, type = None):

        if type == 'userInfo':
            url = self.API_HOST + self.USER_PATH
        elif type == 'userBeers':
            url = self.API_HOST + self.USER_BEER_PATH

        headers = {
            'Authorization': 'bearer %s' % self.ACCESS_TOKEN,
        }

        params = {
            "": "",
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def main(self, type = None):

        try:
            results = self.make_request(type)
            return results
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )

@app.route('/api/tap/user', methods=['GET'])
def get_user(): 

    type = 'userInfo'

    tap = Untappd()

    results = tap.main(type)
    return jsonify(results)

@app.route('/api/tap/beers', methods=['GET'])
def get_beers(): 

    type = 'userBeers'

    tap = Untappd()

    results = tap.main(type)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)