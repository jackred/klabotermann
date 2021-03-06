# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

import os


class DefaultConfig:
    """ Bot Configuration """
    HOST = "0.0.0.0"
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    PREFIX = "!"


class DBConfig:
    """DB Configuration"""
    port = 27017
    host = "ng_mongo"
    db = "klabotermann"
