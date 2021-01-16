# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

from scholarly import scholarly
from src import database


def request_publication(keywords, proxy):
    scholarly.use_proxy(proxy[0])
    res = scholarly.search_pubs(' '.join(keywords), to_sort=1)
    return res


def compile_until_last_article(publications, last_titles, max_title=9):
    if len(publications._rows) > 0:
        pub = next(publications)
    res = []
    while ((len(publications._rows) > publications._pos < max_title)
           and (pub.bib['title'] not in last_titles)):
        res.append(pub)
        pub = next(publications)
    return res


def build_message_new_articles(new_articles):
    return '\n'.join([art.bib['title'] for art in new_articles])


def get_last_article_for_search(keywords, db, proxy):
    last_titles = database.get_title_known_articles(keywords, db)
    pubs = request_publication(keywords, proxy)
    new_articles = compile_until_last_article(pubs, last_titles)
    return new_articles


def update_one_keywords(keywords, db, proxy, upsert=False):
    new_articles = get_last_article_for_search(keywords, db, proxy)
    titles = [art.bib['title'] for art in new_articles]
    titles.reverse()
    database.update_articles(keywords, titles, db, upsert)
    return new_articles


def create_new_keywords(keywords, db, proxy):
    return update_one_keywords(keywords, db, proxy, True)
