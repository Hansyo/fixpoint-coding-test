# Server log analysis

サーバへの`ping`の実行結果を解析する事ができるライブラリです。

## 読み込み可能なログファイルの形式

CSVで以下の形式で書かれたログファイルを解析することができます。

```
datetime,server address,response time
20201019133125,10.20.30.1/16,-
20201019133126,10.20.30.2/16,2
...
```

### datetime

`YYYYMMDDhhmmss`形式の日付データです。  
|形式|意味|
|:--:|:--:|
|`YYYY`|4桁の西暦|
|`MM`|2桁のゼロ埋めされた月|
|`DD`|2桁のゼロ埋めされた日付|
|`hh`|2桁のゼロ埋めされた時|
|`mm`|2桁のゼロ埋めされた分|
|`ss`|2桁のゼロ埋めされた秒|

### server address

`IPv4アドレス/ネットワークプレフィックス長`形式のIPアドレス情報です。

### response time

サーバへpingを送った際のレスポンスが返ってくるまでにかかった時間(ミリ秒)です。  
タイム・アウトした際は。`-`が記録されます。

## How to Setup

1. Install [poetry](https://python-poetry.org/).
2. Run `poetry install`

## How to Test

1. Do setup
2. Run `poetry run pytest`