import uuid

import requests


"""
this will contain some integration client-side tests for project
# todo: currently no database rollbacks (should add)
"""


def test_auth():
    with requests.Session() as session:
        resp = session.post(
            "http://127.0.0.1:8000/auth/login",
            json={"login": "default_login", "password": "default_password"},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] == True
        assert len(resp.cookies) == 1


def test_create_user_unauth():
    with requests.Session() as session:
        resp = session.post(
            "http://127.0.0.1:8000/auth/user",
            json={"uuid": str(uuid.uuid4().hex), "login": "asdfgg", "password": "asdfgggg2"},
        )
        assert resp.status_code == 401


def test_create_user_auth():
    with requests.Session() as session:
        resp = session.post(
            "http://127.0.0.1:8000/auth/login",
            json={"login": "default_login", "password": "default_password"},
        )
        assert resp.status_code == 200
        assert len(resp.cookies) == 1
        cookies=resp.cookies
        print("before", cookies)
        resp = session.post(
            "http://127.0.0.1:8000/auth/user",
            json={"uuid": str(uuid.uuid4().hex), "login": "test423", "password": "asdfghhh2"},
            cookies=cookies,
        )
        print(resp.cookies, "now")
        assert resp.status_code == 201
        assert resp.json()["success"] == True
