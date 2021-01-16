# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

from src import scholar
from src import database

from pymongo import ASCENDING


def cmd_create_keywords(keywords, db, proxy):
    res = database.get_keywords(keywords, db)
    if res is None:
        titles = scholar.create_new_keywords(keywords, db, proxy)
        msg = 'New keywords added. %d articles stored.' % (len(titles))
    else:
        msg = 'Keyword already exist'
    return msg


async def keywords_cmd_add(bot, turn_context, args, db, proxy):
    msg = cmd_create_keywords(args, db, proxy)
    await turn_context.send_activity(msg)


async def keywords_cmd_rm(bot, turn_context, args, db, proxy):
    res = database.rm_keywords(args, db)
    if res.acknowledged:
        if res.deleted_count == 1:
            msg = "Keywords deleted"
        elif res.deleted_count == 0:
            msg = "Keywords '%s' was not found. No deletion" % (args)
        else:
            msg = "Problem with the operation: deleted %d keywords" \
                % (res.deleted)
    else:
        msg = "Problem with the operation"
    await turn_context.send_activity(msg)


async def keywords_cmd_list(bot, turn_context, args, db, proxy):
    res = [k['keywords'] for k in
           database.get_all_keywords(db, {'keywords': 1})
           .sort('keywords', ASCENDING)]
    msg = '%d keywords watched%s%s' % (len(res), '' if len(res) == 0 else ':   \n- ', '\n- '.join(res))
    await turn_context.send_activity(msg)


async def channel_cmd_add(bot, turn_context, args, db, proxy):
    bot._add_conversation_reference(turn_context.activity)
    await turn_context.send_activity('this channel now receive update')


async def channel_cmd_rm(bot, turn_context, args, db, proxy):
    bot._rm_conversation_reference(turn_context.activity)
    await turn_context.send_activity("this channel doesn't receive update"
                                     + " anymore")
