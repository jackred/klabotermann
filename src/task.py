# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

import asyncio
import datetime


async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(fn_dt, coro, loop=asyncio.get_event_loop(), repeat=False):
    await wait_until(fn_dt())
    if repeat:
        print('loop')
        loop.create_task(run_at(fn_dt, coro, loop, repeat))
    print('send')
    return await coro()


def time_plus(s=0, m=0, h=0):
    return datetime.datetime.now() + datetime.timedelta(seconds=s, minutes=m,
                                                        hours=h)


def create_repeated_task(fn, time_dict, loop=asyncio.get_event_loop(),
                         start_now=False):
    if start_now:
        loop.create_task(run_at(lambda: time_plus(**{'s': 5}),
                                lambda: fn('toto'), loop))
    loop.create_task(run_at(lambda: time_plus(**time_dict), lambda: fn('tata'),
                            loop,
                            repeat=True))
