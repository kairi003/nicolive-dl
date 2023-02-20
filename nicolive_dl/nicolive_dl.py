#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
from collections import namedtuple
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup, Tag
from requests import Session
from sanitize_filename import sanitize

from .exceptions import *
from .nicolive_ws import NicoLiveCommentWS, NicoLiveWS

NicoLiveInfo = namedtuple("NicoLiveInfo", "lvid title web_socket_url")


class NicoLiveDL:
    def __init__(self):
        self.ses = Session()

    def login(self, username, password, otp_required=False):
        payload = {"mail_tel": username, "password": password}
        login_url = "https://account.nicovideo.jp/login/redirector"
        res = self.ses.post(login_url, data=payload)
        # check email for otp
        if otp_required:
            otp = input("OTP: ")
            payload2 = {
                "otp": otp,
                "loginBtn": "Login",
                "is_mfa_trusted_device": "true",
                "device_name": "nicolivedl",
            }
            otp_url = res.url
            res2 = self.ses.post(otp_url, data=payload2)
            if res2.url != "https://account.nicovideo.jp/my/account":
                raise LoginError("Failed to Login")

    async def download(self, lvid, output="{title}-{lvid}.ts", save_comments=False):
        lvid, title, web_socket_url = await self.get_info(lvid)
        title = sanitize(title)
        output_path = Path(output.format(title=title, lvid=lvid))

        if output_path.exists():
            while True:
                ans = input(f"Can you overwrite {output_path}? [y/n]")
                if ans.lower() == "y":
                    break
                elif ans.lower() == "n":
                    return
        nlws = NicoLiveWS(web_socket_url)
        asyncio.create_task(nlws.connect())

        if save_comments:
            comment_output_path = output_path.parent / (output_path.stem + ".jsonl")
            room_event = await nlws.wait_for_room()
            comment_ws = NicoLiveCommentWS(room_event, comment_output_path)
            asyncio.create_task(comment_ws.connect())

        stream_uri = await nlws.wait_for_stream()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        args = ["-y", "-i", stream_uri, "-c", "copy", output_path]
        proc = await asyncio.create_subprocess_exec("ffmpeg", *args)
        await proc.communicate()
        await nlws.close()

    async def get_info(self, lvid):
        res = self.ses.get(f"https://live.nicovideo.jp/watch/{lvid}")
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        embedded_tag = soup.select_one("#embedded-data")
        if not isinstance(embedded_tag, Tag):
            raise SelectException("Not Found #embedded-data")
        embedded_data = embedded_tag.get_attribute_list("data-props")[0]
        decoded_data = json.loads(unquote(embedded_data))
        web_socket_url = decoded_data["site"]["relive"]["webSocketUrl"]
        title = decoded_data["program"]["title"]
        return NicoLiveInfo(lvid, title, web_socket_url)
