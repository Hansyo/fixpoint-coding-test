# Server log analysis

サーバへの`ping`の実行結果を解析する事ができるライブラリです。  
このライブラリでは、以下のことが可能です。
1. サーバーがいつダウンしたかを、何度応答が連続で返ってこなかったかで判定できる
2. サーバーが過負荷になっていたかを、応答にかかった時間を指定して判別できる
3. ネットワークスイッチが落ちていた場合、ネットワークスイッチが落ちていることを判別できる
   1. ただし、多段のネットワークスイッチが落ちているかどうかを現状では判定できません。例えば、`10.20.0.0/16`配下の`10.20.10.0/24`と`10.20.20.0/24`があった時、`10.20.0.0/16`が落ちていたとしても、`10.20.10.0/24`と`10.20.20.0/24`の2つのスイッチが落ちていると判定されます。


## 簡易的な使用方法
関数ごとの詳細な情報は、`docs`配下にあるファイルを閲覧してください。  
また、各種関数の具体的な使用例については、`tests`配下にあるコードが参考になるはずです。  

### サーバー群のダウン情報及び過負荷情報が知りたい場合
1. `servers = Server.load_file("/path/to/file")`を使用してサーバー群の情報を解析可能にする。
2. `Server.print_server_error(servers, continuous=3, time_threshold=100)`を実行する。

### ネットワーク群のダウン情報及び過負荷情報が知りたい場合
1. `Networks = Network.load_file("/path/to/file")`を使用してネットワーク群の情報を解析可能にする。
2. `Network.print_networks_error(networks, continuous=3, with_server_timeout=True, with_server_overload=True, time_threshold=100)`を実行する。

### 補足
先頭が`print_`で始まる関数を用いることで、各種情報を確認することができます。  
メッセージはおおよそ以下の情報が表示されます。(`[]`内の情報は表示されない場合もあります)
```
<IPアドレス情報> <エラーの有無>
    [サーバー/スイッチのIPアドレス] ["switch down"|"server down"|"server overload"] <ログの開始時間> ~ [<ログの終了時間>]
    [サーバー/スイッチのIPアドレス] ["switch down"|"server down"|"server overload"] <ログの開始時間> ~ [<ログの終了時間>]
    ...
```

## 読み込み可能なログファイルの形式

以下の形式で書かれたログファイルを解析することができます。

```csv
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