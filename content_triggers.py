import ast
import re

TRIGGER_NOT_FOUND = 'триггер не найден'
LINK_THUMB_URL = 'https://i.imgur.com/tokK703.png'
TEXT_THUMB_URL = 'https://i.imgur.com/O2yehMw.png'


def calc_loaded_triggers(id2triggers):
    triggers2id = dict()
    for id in id2triggers:
        for trigger in id2triggers[id]:
            triggers2id[trigger] = id
    return id2triggers, triggers2id


def load_triggers():
    with open('triggers.txt') as f:
        id2triggers = ast.literal_eval(f.read())
    return id2triggers


def dump_triggers(id2triggers):
    with open('triggers.txt') as f:
        f.write(str(id2triggers))


def get_text_from_id(file_id):
    return file_id[1:]


def check_url(url):
    regex = re.compile(
        r'^(?:https?://|)'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

