import asyncio
from aiohttp import ClientSession, ClientError
from grazyna.utils.event_loop import loop
from grazyna.format import color, bold


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


POSSIBLE_EXCEPTIONS = (
    ClientError, IndexError, NothingChangeException, asyncio.TimeoutError
)

@loop(time_config_key="commits_time", default=60)
def commits(irc_protocol, plugin, config):
    try:
        data = yield from github_action('commits', plugin, config)
    except POSSIBLE_EXCEPTIONS:
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
        data = yield from github_action('issues/events', plugin, config)
    except POSSIBLE_EXCEPTIONS:
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
        data = yield from github_action('issues/comments', plugin, config)
    except POSSIBLE_EXCEPTIONS:
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


@asyncio.coroutine
def github_action(action, plugin, config, sort_by='updated'):
    url = API_URL.format(
        api=API_URL,
        user=config['user'],
        repo=config['repository'],
        action=action,
    )
    query = {
        'sort': sort_by,
        'direction': 'desc',
        'sha': config.get('branch', 'master')
    }
    headers = {'Accept': 'application/vnd.github.v3+json'}
    etag = plugin.temp.get(action)
    if etag is not None:
        headers['If-None-Match'] = etag

    session = ClientSession()
    try:
        resp = yield from asyncio.wait_for(
            session.get(url, params=query, headers=headers),
            timeout=5
        )
        try:
            plugin.temp[action] = resp.headers.get('etag')
            if resp.status != 200 or etag is None:  # etag must be cached first
                raise NothingChangeException(etag)
            data = yield from resp.json()
        finally:
            resp.close()
    finally:
        session.close()
    return data[0]
