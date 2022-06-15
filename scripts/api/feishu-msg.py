#!/usr/bin/python3

import os, sys
from modules.common import *
from modules.send_msg_feishu import *

if __name__ == "__main__":
    METHOD_GET_redirect_www("feishu-msg.html")

    hook_url = get_param_value("hook_url", required=True)
    msg_type = get_param_value("msg_type", required=True)
    payload = get_payload()

    result = "not match"
    if msg_type == "text":
        result = send_msg_feishu_txt(hook_url, payload)
    elif msg_type == "md":
        result = send_msg_feishu_md(hook_url, payload)
    print(result)
