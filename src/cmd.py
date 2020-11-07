# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

from src import scholar
from src import database


def cmd_create_keywords(keywords, db):
    res = database.get_keywords(keywords, db)
    if res is None:
        titles = scholar.create_new_keywords(keywords, db)
        msg = 'New keywords added. %d articles stored.' % (len(titles))
    else:
        msg = 'Keyword already exist'
    return msg


async def keywords_cmd_add(bot, turn_context, args, db):
    # bot._add_conversation_reference(turn_context.activity)
    msg = cmd_create_keywords(args, db)
    await turn_context.send_activity(msg)


async def keywords_cmd_rm(bot, turn_context, args, db):
    # bot._rm_conversation_reference(turn_context.activity)
    return 'rm'


async def keywords_cmd_list():
    return 'list'