#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import asyncio
from getpass import getpass

from . import LIVE_URL_PREFIX, NicoLiveDL


async def _main(
        username: str | None,
        password: str | None,
        live_id: str,
        save_comments: bool = False,
        cookies_file: str | None = None):
    nldl = NicoLiveDL()
    if cookies_file:
        nldl.load_cookies(cookies_file)
    elif username and password:
        nldl.login(username, password)
    await nldl.download(live_id, save_comments=save_comments)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="Username/Email address")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument(
        "-l",
        "--live-id",
        help=f"Live ID or Live URL. Valid format of Live URL: {LIVE_URL_PREFIX}lv0123456789, lv0123456789 is the Live ID in this case",
    )
    parser.add_argument(
        "--save-comments",
        action="store_true",
        help="Whether to save comments. Comments will be saved in the same directory as the video",
    )
    parser.add_argument(
        "-a",
        "--anonymous",
        action="store_true",
        help="No login required. You can only watch public live streams",
    )
    parser.add_argument(
        "-c",
        "--cookies-file",
        help="Path to the cookies file. If not specified, cookies will not be saved",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.anonymous or args.cookies_file:
        username = None
        password = None
    else:
        username = args.username or input("Account: ").strip()
        password = args.password or getpass("Password: ").strip()
    live_id = args.live_id or input("Live Id: ")
    asyncio.run(
        _main(
            username,
            password,
            live_id,
            save_comments=args.save_comments,
            cookies_file=args.cookies_file
        )
    )


if __name__ == "__main__":
    main()
