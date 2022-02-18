# nicolive-dl
ニコ生タイムシフトダウンローダーです。

現状タイムシフトを想定していますが普通の生放送でも動くかも。

[Qiita: ニコ生(タイムシフト)ダウンローダーを書く](https://qiita.com/kairi003/items/62a487a2ab786cb0f502)

PRとかくれると嬉しいです。


## Installation
GitHubからpipでインストールできます。

```bash
pip install git+https://github.com/kairi003/nicolive-dl
```

別途ffmpegをインストールしてPATHを通しておく必要があります。


## Usage

`nicolive_dl` コマンドで起動され、ユーザ名、パスワード、生放送IDを対話的に入力します。

生放送IDはURLが `https://live.nicovideo.jp/watch/lv0123456789` なら `lv0123456789` です。