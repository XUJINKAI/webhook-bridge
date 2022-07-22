
import json
from .common import *
from .git import *

def parse_chandao_msg_to_md(payload, config):
    if not payload:
        return None
    o = json.loads(payload)
    if type(o) is not dict:
        print("Payload is not JSON")
        return None
    r = ""
    
    cfg_obj_types = safeget(config, 'object-types')
    cfg_bug_actions = safeget(config, 'bug-actions')
    cfg_products = safeget(config, 'products')

    objectType = safeget(o, 'objectType')
    action = safeget(o, 'action')
    product = safeget(o, 'product')
    if product:
        product = product.strip(",")
    text = safeget(o, 'text')
    comment = safeget(o, 'comment')

    if type(cfg_obj_types) is list and objectType not in cfg_obj_types:
        print(f"Object Type '{objectType}' not configured in {cfg_obj_types}")
        return None
    if objectType == 'bug' and type(cfg_bug_actions) is list and action not in cfg_bug_actions:
        print(f"Bug action '{action}' not configured")
        return None

    if type(cfg_products) is dict and product in cfg_products:
        r += f"产品: **{cfg_products[product]}**\n"
    r += f"{text}\n"
    if comment:
        r += f"{comment}\n"
    return r
