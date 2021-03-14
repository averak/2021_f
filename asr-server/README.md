# 音声認識サーバ

KC3Hack2021 で使用する音声認識サーバです。

大語彙連続音声認識ではなく，辞書にある音声の分類問題として音声認識を実現します。

## 実行環境

- Python ~> 3.8
- Tensorflow

## インストール

```sh
$ pipenv install
```

独自に学習モデルを作成する場合には，`portaudio`が必要になります。

- Ubuntu - `sudo apt-get install portaudio19-dev`
- macOS - `brew install portaudio`

## 使い方

### 1. 教師データを作成

```sh
$ pipenv run record
$ pipenv run build
```

### 2. 学習

```sh
$ pipenv run train
```

### 3. ASR サーバを起動

```sh
$ pipenv run start
```

使い方の詳細を知りたい場合は，下記コマンドを実行してください。

```sh
$ pipenv run help
```

### データディレクトリについて

```sh
data
├── record
│  ├── noise
│  │  ├── xxx.wav
│  │  └── xxx.wav
│  └── speech
│     ├── xxx.wav
│     └── xxx.wav
└── teacher
   ├── x.npy
   └── y.npy
```
