import telebot
from content_triggers import *


with open('secrets/token.txt') as f:
    bot = telebot.TeleBot(f.read().strip())

id2triggers, triggers2id = calc_loaded_triggers(load_triggers())


def get_variants(trig):
    variants = []
    for trigger in triggers2id:
        ind = trigger.find(trig)
        if ind == -1 or trigger == TRIGGER_NOT_FOUND:
            continue
        variants.append((ind != 0, len(trigger), trigger))
    variants.sort()
    return [var[-1] for var in variants]


def get_content_type(file_id):
    if file_id[0] == '#':
        text = get_text_from_id(file_id)
        return ('text', 'link')[check_url(text)]
    dir = bot.get_file(file_id).file_path.split('/')[0]
    typ = {'photos': 'photo',
           'animations': 'gif',
           'stickers': 'sticker',
           'videos': 'video'}.get(dir, dir)
    return typ


def get_inline_content(trig, index):
    file_id = triggers2id[trig]
    typ = get_content_type(file_id)
    if typ == 'photo':
        return telebot.types.InlineQueryResultCachedPhoto(index, file_id, trig)
    elif typ == 'video':
        return telebot.types.InlineQueryResultCachedVideo(index, file_id, trig)
    elif typ == 'gif':
        return telebot.types.InlineQueryResultCachedGif(index, file_id, trig)
    elif typ == 'sticker':
        return telebot.types.InlineQueryResultCachedSticker(index, file_id)
    elif trig == TRIGGER_NOT_FOUND:
        msg = telebot.types.InputTextMessageContent(get_text_from_id(file_id))
        return telebot.types.InlineQueryResultArticle(index, trig, msg)
    elif typ == 'text':
        thumb = TEXT_THUMB_URL
        text = get_text_from_id(file_id)
        message = telebot.types.InputTextMessageContent(
            text, parse_mode='Markdown',
            disable_web_page_preview=False)
        return telebot.types.InlineQueryResultArticle(index, trig, message,
                                                      description=text,
                                                      thumb_url=thumb)
    elif typ == 'link':
        thumb = LINK_THUMB_URL
        link = get_text_from_id(file_id)
        message = telebot.types.InputTextMessageContent(
            link, parse_mode='Markdown',
            disable_web_page_preview=trig in ('rickroll', 'рикролл'))
        return telebot.types.InlineQueryResultArticle(index, trig, message,
                                                      url=link,
                                                      hide_url=False,
                                                      thumb_url=thumb)
    else:
        print('Unknown content type:', typ)
        print('Trigger:', trig)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline(query):
    trig = query.query.lower()
    variants = get_variants(trig)
    if len(variants) == 0:
        variants.append(TRIGGER_NOT_FOUND)
    content = []
    content_file_ids = set()
    for trigger in variants:
        if len(content) == 20:
            break
        file_id = triggers2id[trigger]
        if file_id in content_file_ids:
            continue
        content_file_ids.add(file_id)
        content.append(get_inline_content(trigger, len(content)))
    return bot.answer_inline_query(query.id, content)


if __name__ == '__main__':
    bot.infinity_polling(timeout=10, none_stop=True)
