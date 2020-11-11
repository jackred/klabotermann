# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>


def get_keywords(keywords, db):
    return db['articles'].find_one({'keywords': keywords})


def get_all_keywords(db, projection=None):
    return db['articles'].find(projection=projection)


def get_title_known_articles(keywords, db):
    res = get_keywords(keywords, db)
    return [] if res is None else res['title']


def update_articles(keywords, titles, db, upsert=False):
    return db['articles'].update_one({'keywords': keywords},
                                     {'$push': {'title': {'$each': titles}}},
                                     upsert=upsert)

def rm_keywords(keywords, db):
    return db['articles'].delete_one({'keywords': keywords})
