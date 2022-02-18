#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from getpass import getpass
import argparse

from . import NicoLiveDL

async def _main(username, password, live_id):
    nldl = NicoLiveDL()
    nldl.login(username, password)
    await nldl.download(live_id)

def main():
    username = input('Account: ')
    password = getpass('Password: ')
    live_id = input('Live Id: ')
    asyncio.run(_main(username, password, live_id))

if __name__ == '__main__':
    main()