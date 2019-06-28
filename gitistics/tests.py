from django.test import TestCase
import unittest, requests, logging

import gitistics.views

class TestConn(TestCase):
    def test_type_web_auth_logged_out(self):
        log = logging.getLogger("Web Auth")
        resp = requests.get("http://127.0.0.1:8000/api/repoList?search_term=vladmasarik")
        resp = resp.json()
        self.assertIsInstance(resp, dict)
        
    def test_type_web_auth_logged_in(self):
        log = logging.getLogger("Web Auth")

        cookies = {'username': 'q', "password": "q"}
        resp = requests.get("http://127.0.0.1:8000/api/repoList?search_term=vladmasarik", cookies = cookies)
        resp = resp.json()
        if type(resp) != dict:
            log.warning("Response with logged user was not JSON but {}".format(type(resp)))   
        
    def test_type_web_repo_list(self):
        action = {
            "label": "listRepo",
            "gitUser": "vladmasarik",
        }
        self.assertIsInstance(gitistics.views.collectData(action), list)


if __name__ == '__main__':
    unittest.main()