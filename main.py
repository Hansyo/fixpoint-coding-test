import datetime as DT
import ipaddress
import itertools
from typing import Dict, List, Optional, Tuple


class Server:
    """
    ログデータから生成されるサーバー情報
    """

    ip_address: ipaddress.IPv4Address = ipaddress.IPv4Address("0.0.0.0")
    ip_prefix: int = 0
    ping_results: Dict[DT.datetime, int] = {}

    TIMEOUT_SYMBOL = -1

    def __init__(self, ip_address: str, ip_prefix: int):
        self.ip_address = ipaddress.IPv4Address(ip_address)
        self.ip_prefix = ip_prefix
        self.ping_results = {}

    def append_ping_results(self, datetime_str: str, response_msec: int):
        """
        サーバーに応答ログを新たに登録する

        Parameters
        ----------
        datetime : str
            ログの日時情報
            "YYYYMMDDhhmmss"形式
        result_msec : int
            サーバーの応答時間。
            タイムアウトの場合は、`Server.TIMEOUT_SYMBOL`を指定
        """

        self.ping_results[parse_datetime(datetime_str=datetime_str)] = response_msec

    def has_downtime(self) -> bool:
        """
        Serverが応答しなかったことがあるかどうか調べる
        """
        return Server.TIMEOUT_SYMBOL in self.ping_results.values()

    def get_downtimes(self) -> List[Tuple[DT.datetime, Optional[DT.datetime]]]:
        """
        サーバーのダウンタイム情報をすべて取得する

        Returns
        List[Tuple[datetime.datetime, datetime.datetime]]
            サーバー上に存在するダウンタイムの開始時間と終了時間のペアを返す。
            記録された最後の記録がダウン状態だった場合、終了時間は`None`となる。
        """

        sorted_ping_results: List[Tuple[DT.datetime, int]] = sorted(self.ping_results.items())
        sorted_response: List[int] = [resp for _, resp in sorted_ping_results]
        # ダウンした列番号を取得
        down_recode: List[int] = [i for i, resp in enumerate(sorted_response) if resp == Server.TIMEOUT_SYMBOL]
        properly_recode: List[int] = [i for i, resp in enumerate(sorted_response) if resp != Server.TIMEOUT_SYMBOL]
        # 連続した番号を削除
        down_recode_alt: List[int] = [
            list(g)[0]
            for _, g in itertools.groupby(
                down_recode, key=(lambda n, c=itertools.count(): n - next(c))  # type: ignore
            )
        ]
        properly_recode_alt: List[int] = [
            list(g)[0]
            for _, g in itertools.groupby(
                properly_recode, key=(lambda n, c=itertools.count(): n - next(c))  # type: ignore
            )
        ]
        # ペアを生成
        result: List[Tuple[DT.datetime, Optional[DT.datetime]]] = []
        for i in down_recode_alt:
            while True:
                if len(properly_recode_alt) != 0 and properly_recode_alt[0] < i:
                    properly_recode_alt.pop(0)
                else:
                    break
            if len(properly_recode_alt) != 0:
                result.append((sorted_ping_results[i][0], sorted_ping_results[properly_recode_alt.pop(0)][0]))
            else:
                result.append((sorted_ping_results[i][0], None))
        return result


def csv_to_params(csv_text: str) -> Tuple[str, str, int, int]:
    datetime, server_address, result_msec_str = csv_text.split(",")
    ip_address, ip_prefix_str = server_address.split("/")
    ip_prefix: int = int(ip_prefix_str)
    result_msec: int = int(result_msec_str) if result_msec_str.isdigit() else Server.TIMEOUT_SYMBOL
    return datetime, ip_address, ip_prefix, result_msec


def parse_datetime(datetime_str: str) -> DT.datetime:
    """
    日時情報を年月日時分秒にパースする

    Parameters
    ----------
    datetime_str : str
        "YYYYMMDDhhmmss"の文字列

    Returns
    -------
    datetime.datetime
        datetime_strから生成された`datetime`オブジェクト

    Raises
    ------
    ValueError
        `datetime` が有効な日時ではない
    """

    datetime: DT.datetime = DT.datetime.strptime(datetime_str, "%Y%m%d%H%M%S")
    return datetime


def load_data(file_path: str, servers: Dict[str, Server] = {}) -> Dict[str, Server]:
    """
    ログデータからサーバーデータを生成する

    Parameters
    ----------
    file_path : str
        ログデータのファイルパス
    servers : Dict[str, Server], optional
        既存のサーバーデータがある場合のみ指定。

    Returns
    -------
    Dict[str, Server]
        IPアドレスに紐づいたサーバーデータ
    """

    with open(file_path) as f:
        _ = f.readline()  # ファイルの先頭を読み飛ばす
        for line in f.readlines():
            line_strip = line.strip()
            datetime, ip_address, ip_prefix, result_msec = csv_to_params(line_strip)
            if ip_address not in servers.keys():
                servers[ip_address] = Server(ip_address=ip_address, ip_prefix=ip_prefix)
            servers[ip_address].append_ping_results(datetime, result_msec)
    return servers


if __name__ == "__main__":
    file_path = "test_case/001.csv"

    servers = load_data(file_path=file_path)
    for ip_address, server in servers.items():
        if server.has_downtime():
            print(f"{server.ip_address} has downtime")
            for start, end in server.get_downtimes():
                print(f"    {start} ~ {end if end is not None else ''}")
