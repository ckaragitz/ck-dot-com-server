from __future__ import print_function
from flask import Flask, request, jsonify
from requests.models import HTTPError
import requests
import sys

app = Flask(__name__)

class GitHub:

    ACCESS_TOKEN = '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' 
    API_HOST = 'https://api.github.com'
    ALL_REPO_PATH = '/users/ckaragitz/repos'
    REPO_PATH = '/repos/ckaragitz/'

    def __init__(self, repo = None):

        self.repo = repo

    def make_request(self, repo = None):

        if repo != "all":
            url = self.API_HOST + self.REPO_PATH + f"{repo}"
        else:
            url = self.API_HOST + self.ALL_REPO_PATH

        headers = {
            'Authorization': 'token %s' % self.ACCESS_TOKEN,
        }

        params = {
            "state": "open",
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def main(self, repo = None):

        try:
            results = self.make_request(repo)
            return results
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )

@app.route('/api/git/repos', methods=['GET'])
def get_repos(): 

    g = GitHub(repo = "all")

    results = g.main(repo = "all")
    return jsonify(results)

@app.route('/api/git/repos/<repo>', methods=['GET'])
def get_repo(repo): 

    g = GitHub(repo)

    results = g.main(repo)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)