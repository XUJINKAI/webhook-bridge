import os, sys

def safeget(o, *keys):
    for key in keys:
        try:
            o = o[key]
        except KeyError:
            return None
    return o

def str_remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def get_param_value(name, default=None, required=False):
    value = os.environ.get(name)
    if value is None:
        if required:
            print(f"{name} is not set")
            exit()
        return default
    return value

def get_payload():
    return sys.argv[1]

def METHOD_GET_redirect_www(url):
    http_method = os.environ.get('hook_method', default=None)
    if http_method == "GET":
        print(f"<script>window.location.href='/www/{url}'</script>")
        exit()
