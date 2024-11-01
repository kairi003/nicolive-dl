# nicolive-dl
ニコ生タイムシフトダウンローダーです。

現状タイムシフトを想定していますが普通の生放送でも動くかも。

[Qiita: ニコ生(タイムシフト)ダウンローダーを書く](https://qiita.com/kairi003/items/62a487a2ab786cb0f502)

PR等いただけると嬉しいです。


## Installation
GitHubからpipでインストールできます。

```bash
pip install git+https://github.com/kairi003/nicolive-dl
```

別途ffmpegをインストールしてPATHを通しておく必要があります。


## Usage

### Interactive Mode
- `nicolive-dl` コマンドで起動され、ユーザ名、パスワード、生放送IDを対話的に入力します。
- 生放送IDはURLが `https://live.nicovideo.jp/watch/lv0123456789` なら `lv0123456789` です。
- 二段階認証が設定されている場合、入力を求められます。
- ユーザ名を指定しない場合または `-a` オプションを指定すると匿名でダウンロードできます。
- 【推奨】`-c` オプションで cookies.txt ファイルを指定することで cookie を用いてログインできます。
  - ブラウザでログインした状態で [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) 等を使ってニコ生の cookies.txt を保存してください。


### Command Line Options
```
usage: nicolive-dl [-h] [-u USERNAME] [-p PASSWORD] [-l LIVE_ID] [--save-comments] [-a] [-c COOKIES_FILE]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username/Email address
  -p PASSWORD, --password PASSWORD
                        Password
  -l LIVE_ID, --live-id LIVE_ID
                        Live ID or Live URL. Valid format of Live URL: https://live.nicovideo.jp/watch/lv0123456789, lv0123456789 is the Live ID in this case
  --save-comments       Whether to save comments. Comments will be saved in the same directory as the video
  -a, --anonymous       No login required. You can only watch public live streams
  -c COOKIES_FILE, --cookies-file COOKIES_FILE
                        Path to the cookies file. If not specified, cookies will not be saved
```
