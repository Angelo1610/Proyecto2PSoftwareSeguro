import json
import sys, os
sys.path.append(os.path.abspath("."))

from src.app import app


def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200

def test_scan():
    client = app.test_client()
    payload = {"code": "eval('2+2')"}
    res = client.post("/scan", json=payload)
    data = json.loads(res.data)

    assert "prediction" in data
    assert "probability" in data
