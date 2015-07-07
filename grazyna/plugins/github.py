from ..utils.event_loop import loop
from ..format import color, bold

import requests
import asyncio

API_URL = "https://api.github.com/repos/{user}/{repo}/{action}"
state_colors = {
    'open': color.green,
    'closed': color.red,
    'reopened': color.green,
    'subscribed': color.green,
    'merged': color.green,
    'assigned': color.purple,
    'unassigned': color.purple,
    'milestoned': color.olive,
    'demilestoned': color.olive,
    'locked': color.red,
    'unlocked': color.green,
    'renamed': color.dark_gray
}


class NothingChangeException(Exception):
    pass


@loop(time_config_key="commits_time", default=60)
def commits(irc_protocol, plugin, config):
    try:
        data = github_action('commits', plugin, config)
    except (requests.HTTPError, NothingChangeException):
        return

    msg = "‼ {commit} '{msg}' by {committer} {url}".format(
        commit=bold('COMMIT'),
        msg=strip(data['commit']['message']),
        committer=data['commit']['author']['name'],
        url=data['html_url']
    )

    for chan in config['channels'].split(','):
        irc_protocol.say(chan.strip(), msg)


@loop(time_config_key="events_time", default=60)
def events(irc_protocol, plugin, config):
    try:
        data = github_action('issues/events', plugin, config)
    except (requests.HTTPError, IndexError, NothingChangeException):
        return

    issue = data['issue']
    state = data['event']
    state_color = state_colors.get(state, color.black)
    assignee = issue['assignee']
    assignee_login = assignee['login'] if assignee is not None else None
    msg = ("‼ {issue} {labels} '{title}' by {user} "
           "{assignee} {state} {url}").format(
        issue=bold('ISSUE'),
        labels=' '.join('[%s]' % label['name'] for label in issue['labels']),
        title=strip(issue['title']),
        state=bold(color(' %s ' % state, color.white, state_color)),
        user=issue['user']['login'],
        assignee="assigned to %s" % assignee_login if assignee_login else '',
        url=issue['html_url'],
    )

    for chan in config['channels'].split(','):
        irc_protocol.say(chan.strip(), msg)


@loop(time_config_key="comments_time", default=60)
def comments(irc_protocol, plugin, config):
    try:
        data = github_action('issues/comments', plugin, config)
    except (requests.HTTPError, IndexError, NothingChangeException):
        return

    msg = "‼ {issue} by {nick} '{msg}' {url}".format(
        issue=bold('COMMENT'),
        msg=strip(data['body']),
        nick=data['user']['login'],
        url=data['html_url'],
    )

    for chan in config['channels'].split(','):
        irc_protocol.say(chan.strip(), msg)


def strip(msg):
    lines = msg.splitlines()
    line = lines[0]
    if len(lines) == 0:
        return ''
    elif len(lines) == 1:
        return line if len(line) < 50 else line[:50] + "…"
    else:
        return line[:50] + "…"


def github_action(action, plugin, config, sort_by='updated'):
    url = API_URL.format(
        api=API_URL,
        user=config['user'],
        repo=config['repository'],
        action=action,
    )
    query = {'sort': sort_by, 'direction': 'desc'}
    headers = {'Accept': 'application/vnd.github.v3+json'}
    etag = plugin.temp.get(action)
    if etag is not None:
        headers['If-None-Match'] = etag

    req = requests.get(url, params=query, headers=headers, timeout=5)
    req.raise_for_status()
    plugin.temp[action] = req.headers.get('etag')
    if req.status_code == 304 or etag is None:  # etag must be cached first
        raise NothingChangeException(etag)
    return req.json()[0]
