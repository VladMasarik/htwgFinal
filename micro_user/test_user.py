import os
import tempfile

import pytest, unittest, requests, logging

import micro_user.main


def test_type_user_listGroups():
    resp = requests.get("http://127.0.0.1:5000/listGroups").json()
    assert(type(resp) == list)




@pytest.fixture
def client():
    pass