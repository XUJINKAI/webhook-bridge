
import json
from .common import *
from .git import *

def parse_gitlab_msg_to_md(payload, config):
    if not payload:
        return ""
    o = json.loads(payload)
    if type(o) is not dict:
        return None
    r = ""

    def multiline_regroup(text, trim_empty=True, line_joint="\n> ", max_line_len=3):
        text = [x for x in text.split('\n') if x or not trim_empty]
        text = text[:max_line_len]
        return line_joint.join(text)

    def in_repo_link(o):
        repo_name = safeget(o,'repository','name')
        repo_url = safeget(o,'repository','homepage')
        repo_link = f"[{repo_name}]({repo_url})"
        return f"at repository {repo_link}";

    def username(o):
        if 'user_name' in o:
            username = o['user_name']
        else:
            username = safeget(o, 'user', 'name')
        return f'**{username}**'

    action = o.get("object_kind", None)
    if action == "push":
        ref_name = str_remove_prefix(safeget(o,'ref'),'refs/heads/')
        ref_filter = config.get('branch_filter', '*')
        if not name_match_filter(ref_name, ref_filter):
            print(f"Branch name not match filter: {ref_filter}")
            return None
        r += f"{username(o)} pushed to branch **{ref_name}** {in_repo_link(o)}\n"
        for c in safeget(o,'commits'):
            c_id = c.get('id','')[0:8]
            c_url = c.get('url','')
            r += f"> [{c_id}]({c_url}):{safeget(c,'title')}\n"
    elif action == "tag_push":
        tag_name = str_remove_prefix(safeget(o,'ref'),'refs/tags/')
        r += f"{username(o)} pushed tag **{tag_name}** {in_repo_link(o)}\n"
        tag_message = safeget(o,'message')
        if tag_message:
            r += f"> {tag_message}\n"
    elif action == "issue":
        issue_action = safeget(o,'object_attributes','action')
        issue_title = safeget(o,'object_attributes','title')
        issue_url = safeget(o,'object_attributes','url')
        issue_link = f"[{issue_title}]({issue_url})"
        r += f"{username(o)} {issue_action} Issue {issue_link} {in_repo_link(o)}\n"
        if issue_action == "open":
            r += f"> {multiline_regroup(safeget(o,'object_attributes','description'))}\n"
    elif action == "note":
        note_type = safeget(o,'object_attributes','noteable_type')
        if note_type == "Issue":
            issue_title = safeget(o,'issue','title')
            issue_url = safeget(o,'issue','url')
            issue_link = f"[{issue_title}]({issue_url})"
            r += f"{username(o)} comment Issue {issue_link} {in_repo_link(o)}\n"
            r += f"> {multiline_regroup(safeget(o,'object_attributes','note'))}\n"
        elif note_type == "Commit":
            commit_title = safeget(o,'object_attributes','commit_id')[0:8]
            commit_url = safeget(o,'object_attributes','url')
            commit_link = f"[{commit_title}]({commit_url})"
            r += f"{username(o)} comment Commit {commit_link} {in_repo_link(o)}\n"
            r += f"> {multiline_regroup(safeget(o,'object_attributes','note'))}\n"
        else:
            r += f"{username(o)} note {note_type} {in_repo_link(o)}\n"
    else:
        r += f"{username(o)} do **{action}** {in_repo_link(o)}\n"
    return r
