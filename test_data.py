valid_auth_data = [
    {'name': 'kate'},
    {'name': ''},
    {'name': 'User with spaces'},
    {'name': 'User123'},
    {'name': 'A' * 100},
]

another_user_auth_data = {'name': 'another_user'}

post_meme_data = [
    {
        'url': 'https://t.me/python_community_rus/27/168416',
        'text': 'Открыл книгу, а вот закрыть не получается..',
        'tags': ['it', 'linux', 'editors', 'vim'],
        'info': {
            'group': 'https://t.me/python_community_rus',
            'admin': 'https://t.me/artemshumeiko',
        },
    },
    {
        'url': 'https://t.me/qa_guru_chat/105051/124432',
        'text': 'min',
        'tags': [],
        'info': {},
    },
    {
        'url': 'https://t.me/qa_guru_chat/105051/123415',
        'text': 'A' * 1000,
        'tags': ['it', 'programming', 'bug', 'git', 'github'],
        'info': {
            'author': 'Lisbeth Salander',
            'source': 'Telegram',
            'colors': ['black', 'white'],
            'rating': 5,
        },
    },
]

invalid_meme_data = [
    {
        'url': 'https://t.me/python_community_rus/27/168416',
        'text': 'Открыл книгу, а вот закрыть не получается..',
        'tags': ['it', 'linux', 'editors', 'vim'],
    },
    {
        'text': 'min',
        'tags': [],
        'info': {},
    },
    {
        'url': 'https://t.me/qa_guru_chat/105051/123415',
        'tags': ['it', 'programming', 'bug', 'git', 'github'],
    },
    {},
]

update_meme_data = {
    'url': 'https://t.me/itgid_info/1802',
    'text': 'bad memory',
    'tags': [],
    'info': {},
}

invalid_meme_data_to_update = [
    {
        'text': 'min',
        'tags': [],
        'info': {},
    },
    {},
    {
        'url': 'https://t.me/qa_guru_chat/105051/123415',
        'tags': ['it', 'programming', 'bug', 'git', 'github'],
    },
    {
        'url': 'https://t.me/python_community_rus/27/168416',
        'text': 'Открыл книгу, а вот закрыть не получается..',
        'tags': ['it', 'linux', 'editors', 'vim'],
    },
]

unexisting_meme_id = 10000
string_id = 'one'
