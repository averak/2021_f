# KC3Hack 2021 F チーム

![reviewdog](https://github.com/kc3hack/2021_f/workflows/reviewdog/badge.svg)
![deploy](https://github.com/kc3hack/2021_f/workflows/deploy/badge.svg)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

[![KC3Hack](https://kc3.me/hack/wp-content/uploads/2021/01/kc3hack2021ogp@2x.png)](https://kc3.me/hack)

## プロダクト名

## プロダクト説明

インターホンの自動応対 bot です。

音声をインターフェースとした応対を可能とし，怠惰なあなたを助けます。

インターホンが鳴った時，「今は手が離せない」「ヘッドフォンを付けているため気づかない」...などの経験はありませんか？

アプリから設定するだけで，，あなたに合った bot が迅速に作れます。

## 使用技術

### PC 常駐アプリ

Nuxt.js と Electron を用いたネイティブアプリケーションです。

友人知人の時はドアを解錠，宅配の時は置き配をお願いする，などの設定をすることができる他，条件によってサイレンを鳴らすことも可能です。

- [ソースコード](https://github.com/Chige12/kc3hack-front)

### 中間サーバ

PC 常駐アプリとドアホン専用機の仲介を担います。

それぞれと Websocket で通信をし，設定の更新や応対音声の再生命令などを担当します。

- [ソースコード](https://github.com/inatatsu-tatsuhiro/kc3_server)

### 音声認識サーバ

本音声認識サーバは

1. `1~9`の数字の認識
2. 大語彙音声認識

の機能を提供します。

応対 bot が設定に応じて「友人知人の方は 1 を，宅配業者の方は 2 を...」のように応対した後，来客が発した音声を認識します。

- [ソースコード](https://github.com/kc3hack/2021_f/tree/main/asr-server)
- [API 仕様書](https://github.com/kc3hack/2021_f/wiki/ASR%E3%82%B5%E3%83%BC%E3%83%90)

### ドアホン専用機

ここでは音声の録音やドアの自動解錠，ユーザへの通知（中間サーバを経由）などを行います。

- [ソースコード](https://github.com/kc3hack/2021_f/tree/main/door_phone)

## Contributers

- [Chige12](https://github.com/Chige12)
- [Phaioka-naoya](https://github.com/Phaioka-naoya)
- [inatatsu](https://github.com/inatatsu-tatsuhiro)
- [averak](https://github.com/averak)
- [lufe](https://github.com/lufeee)
