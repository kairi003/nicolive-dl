#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from getpass import getpass

from . import NicoLiveDl

async def main():
    nldl = NicoLiveDl()
    nldl.login(input('Account: '), getpass('Password: '))
    lvid = input('Live Id: ')
    print(await nldl.get_info(lvid))
    await nldl.download(lvid)

if __name__ == '__main__':
    asyncio.run(main())