# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

from typing import Dict

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount, ConversationReference, Activity

from .task import create_repeated_task

class ProactiveBot(ActivityHandler):
    def __init__(self,  app_id, adapter, conversation_references: Dict[str, ConversationReference]):
        print('create bot')
        self.conversation_references = conversation_references
        self.app_id = app_id
        self.adapter = adapter
        create_repeated_task(self.send_proactive_message, {'s': 10},
                             start_now=True)
        
    async def send_proactive_message(self, s='proactive hello'):
        for conversation_reference in self.conversation_references.values():
            await self.adapter.continue_conversation(
                conversation_reference,
                lambda turn_context: turn_context.send_activity(s),
                self.app_id,
            )
        
    async def on_conversation_update_activity(self, turn_context: TurnContext):
        self._add_conversation_reference(turn_context.activity)
        return await super().on_conversation_update_activity(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Welcome to the Proactive Bot sample.  Navigate to "
                    "http://localhost:3978/api/notify to proactively message everyone "
                    "who has previously messaged this bot."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        self._add_conversation_reference(turn_context.activity)
        return await turn_context.send_activity(
            f"You sent: {turn_context.activity.text}"
        )

    def _add_conversation_reference(self, activity: Activity):
        """
        This populates the shared Dictionary that holds conversation references. In this sample,
        this dictionary is used to send a message to members when /api/notify is hit.
        :param activity:
        :return:
        """
        conversation_reference = TurnContext.get_conversation_reference(activity)
        self.conversation_references[
            conversation_reference.user.id
        ] = conversation_reference
