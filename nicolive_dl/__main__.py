#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import asyncio
from getpass import getpass

from . import NicoLiveDL


async def _main(username, password, live_id, otp_required, save_comments):
    nldl = NicoLiveDL()
    nldl.login(username, password, otp_required)
    await nldl.download(live_id, save_comments=save_comments)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
    parser.add_argument("-l", "--live-id")
    parser.add_argument("--otp-required", action="store_true")
    parser.add_argument("--save-comments", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    username = args.username or input("Account: ")
    password = args.password or getpass("Password: ")
    live_id = args.live_id or input("Live Id: ")
    asyncio.run(
        _main(
            username,
            password,
            live_id,
            otp_required=args.otp_required,
            save_comments=args.save_comments,
        )
    )


if __name__ == "__main__":
    main()
