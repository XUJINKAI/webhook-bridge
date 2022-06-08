import requests

def send_msg_feishu_txt(url, text):
    data = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    try:
        res = requests.post(url, json=data)
        return res.json()
    except Exception as e:
        return {"error": e}

def send_msg_feishu_md(url, text):
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": text,
                }
            ]
        }
    }
    try:
        res = requests.post(url, json=data)
        return res.json()
    except Exception as e:
        return {"error": e}
