#!/usr/local/bin/python3

import os, sys
from modules.common import *
from modules.msg_parse_gitlab import *
from modules.send_msg_feishu import *

if __name__ == "__main__":
    METHOD_GET_redirect_www("")

    branch_filter = get_param_value("branch_filter", "*")
    payload = get_payload()

    md_payload = parse_gitlab_msg_to_md(payload, {'branch_filter': branch_filter})
    if md_payload is None:
        print("md_payload is None")
        exit()
    print(f'Payload : {md_payload}')

    hook_url = get_param_value("hook_url", required=True) # 先转换并打印Payload，再获取hook_url，为空则退出，便于调试
    result = send_msg_feishu_md(hook_url, md_payload)
    print(f'Response: {result}')
