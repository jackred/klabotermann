# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

from typing import Dict

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount, ConversationReference, Activity

from src import cmd
from src import task
from src import database
from src import scholar

class ProactiveBot(ActivityHandler):
    def __init__(self, prefix, app_id, db, adapter,
                 conversation_references: Dict[str, ConversationReference]):
        print('create bot')
        self.create_commands()
        self.prefix = prefix
        self.db = db
        self.conversation_references = conversation_references
        self.app_id = app_id
        self.adapter = adapter
        task.create_repeated_task(self.send_update_article,
                                  {'s': 30},
                                  start_now=False)

    async def send_update_article(self):
        await self.send_proactive_message('trying')
        keywords = database.get_all_keywords(self.db, {'keywords': 1})
        for k in keywords:
            articles = scholar.update_one_keywords(k['keywords'], self.db)
            if len(articles) > 0:
                titles = ['[%s](%s)' % (art.bib['title'], art.bib['url'])
                          for art in articles]
                await self.send_proactive_message(
                    'Articles found for %s:   \n- %s'
                    % (k['keywords'], '   \n- '.join(titles)))

    async def send_proactive_message(self, s='proactive hello'):
        for conversation_reference in self.conversation_references.values():
            await self.adapter.continue_conversation(
                conversation_reference,
                lambda turn_context: turn_context.send_activity(s),
                self.app_id,
            )

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        return await super().on_conversation_update_activity(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        pass

    async def on_message_activity(self, turn_context: TurnContext):
        res = self.parse_commands(turn_context.activity.text)
        if res is not None:
            await res[0](self, turn_context, res[1], self.db)

    def parse_commands(self, text):
        res = None
        if text.startswith(self.prefix):
            cmd_test = text[text.index(self.prefix) + 1:]
            cmds_test = cmd_test.split(' ')
            cmd = self.commands
            i = 0
            while (i < len(cmds_test)
                   and type(cmd) == dict
                   and cmds_test[i] in cmd):
                cmd = cmd[cmds_test[i]]
                i += 1
            if i != 0:
                res = cmd, ' '.join(cmds_test[i:])
        return res

    def create_commands(self):
        self.commands = {'keywords': {'add': cmd.keywords_cmd_add,
                                      'rm': cmd.keywords_cmd_rm,
                                      'list': cmd.keywords_cmd_list},
                         'channel': {'add': cmd.channel_cmd_add,
                                     'rm': cmd.channel_cmd_rm}
                         }
    
    def _add_conversation_reference(self, activity: Activity):
        """
        This populates the shared Dictionary that holds conversation references. In this sample,
        this dictionary is used to send a message to members when /api/notify is hit.
        :param activity:
        :return:
        """
        conversation_reference = \
            TurnContext.get_conversation_reference(activity)
        self.conversation_references[
            conversation_reference.user.id
        ] = conversation_reference

    def _rm_conversation_reference(self, activity: Activity):
        conversation_reference = \
            TurnContext.get_conversation_reference(activity)
        if conversation_reference in self.conversation_references:
            del self.conversation_references[conversation_reference.user.id]
