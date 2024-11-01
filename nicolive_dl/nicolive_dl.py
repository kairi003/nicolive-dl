#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from http.cookiejar import MozillaCookieJar
import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup, Tag
from requests import Session
from sanitize_filename import sanitize

from .exceptions import *
from .nicolive_ws import NicoLiveCommentWS, NicoLiveWS

LIVE_URL_PREFIX = "https://live.nicovideo.jp/watch/"

@dataclass
class NicoLiveInfo:
    lvid: str
    title: str
    web_socket_url: str


class NicoLiveDL:
    def __init__(self):
        self.ses = Session()
    
    def load_cookies(self, cookies_file: str):
        jar = MozillaCookieJar(cookies_file)
        jar.load()
        self.ses.cookies.update(jar)

    def login(self, username: str, password: str):
        payload = {
            "mail_tel": username,
            "password": password
        }
        login_url = "https://account.nicovideo.jp/login/redirector"
        resp = self.ses.post(login_url, data=payload)

        # check email for otp
        if resp.url.startswith("https://account.nicovideo.jp/mfa"):
            otp = input("OTP: ")
            payload2 = {
                "otp": otp,
                "loginBtn": "Login",
                "is_mfa_trusted_device": "true",
                "device_name": "nicolivedl",
            }
            otp_url = resp.url
            resp = self.ses.post(otp_url, data=payload2)
        
        if resp.url != "https://account.nicovideo.jp/my/account":
            raise LoginError("Failed to Login")

    async def download(self,
                       lvid: str,
                       output: str = "{title}-{lvid}.ts",
                       save_comments: bool = False) -> None:
        if lvid.startswith(LIVE_URL_PREFIX):
            lvid = lvid[len(LIVE_URL_PREFIX):]
        info = await self.get_info(lvid)
        title = sanitize(info.title)
        output_path = Path(output.format(title=title, lvid=lvid))

        if output_path.exists():
            ans = input(f"Can you overwrite {output_path}? [y/n]")
            if ans.lower().strip() not in ["y", "yes"]:
                raise FileExistsError(f"{output_path} already exists")
        print(info)
        nlws = NicoLiveWS(info.web_socket_url)
        asyncio.create_task(nlws.connect())

        if save_comments:
            comment_output_path = output_path.parent / \
                (output_path.stem + ".jsonl")
            room_event = await nlws.room_event
            comment_ws = NicoLiveCommentWS(room_event, comment_output_path)
            asyncio.create_task(comment_ws.connect())

        stream_uri = await nlws.stream_uri
        output_path.parent.mkdir(parents=True, exist_ok=True)
        args = ["-y", "-i", stream_uri, "-c", "copy", output_path]
        proc = await asyncio.create_subprocess_exec("ffmpeg", *args)
        await proc.communicate()
        await nlws.close()

    async def get_info(self, lvid: str) -> NicoLiveInfo:
        res = self.ses.get(f"{LIVE_URL_PREFIX}{lvid}")
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "lxml")
        embedded_tag = soup.select_one("#embedded-data")
        if not isinstance(embedded_tag, Tag):
            raise SelectException("Not Found #embedded-data")
        embedded_data = embedded_tag.attrs["data-props"]
        decoded_data = json.loads(unquote(embedded_data))
        web_socket_url = decoded_data["site"]["relive"]["webSocketUrl"]
        if not web_socket_url:
            raise ValueError("webSocketUrl is empty")
        title = decoded_data["program"]["title"]
        return NicoLiveInfo(lvid, title, web_socket_url)
