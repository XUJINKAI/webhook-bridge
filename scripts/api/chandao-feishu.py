#!/usr/bin/python3

import os, sys
from modules.common import *
from modules.msg_parse_chandao import *
from modules.send_msg_feishu import *

if __name__ == "__main__":
    METHOD_GET_redirect_www("")

    payload = get_payload()
    # with open("/root/webhook-bridge/log.txt", "a") as file_object:
    #     file_object.write(f"{payload}\n")

    configs = {
        # 过滤类型
        'object-types': [
            'bug',
        ],
        # 过滤动作
        'bug-actions': [
            'opened',
        ],
        # 产品名称
        'products': {
            # "10": "ID为10的产品名称",
        }
    }

    md_payload = parse_chandao_msg_to_md(payload, configs)
    if md_payload is None:
        print("md_payload is None")
        exit()
    print(f'Payload : {md_payload}')

    hook_url = get_param_value("hook_url", required=True) # 先转换并打印Payload，再获取hook_url，为空则退出，便于调试
    result = send_msg_feishu_md(hook_url, md_payload)
    print(f'Response: {result}')
