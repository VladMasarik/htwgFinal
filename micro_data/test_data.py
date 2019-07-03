import os
import tempfile

import pytest, unittest, requests, logging

import micro_data.main

def test_type_data_userRepos():
    assert(type(micro_data.main.userRepos("vladmasarik")) == list)




@pytest.fixture
def client():
    pass