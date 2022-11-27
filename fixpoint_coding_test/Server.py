import copy
import datetime as DT
import ipaddress
import itertools
from typing import Dict, List, Optional, Tuple


class Server:
    """
    ログデータから生成されるサーバー情報

    TIMEOUT_SYMBOL: int = -1
        タイムアウトした際に記録される数値
    """

    ip_address: ipaddress.IPv4Address = ipaddress.IPv4Address("0.0.0.0")
    ip_prefix: int = 0
    ping_results: Dict[DT.datetime, int] = {}

    TIMEOUT_SYMBOL: int = -1

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

    def get_downtimes(self, threshold: int = 1) -> List[Tuple[DT.datetime, Optional[DT.datetime]]]:
        """
        サーバーのダウンタイム情報をすべて取得する

        Parameters
        ----------
        threshold : int, default=1
            サーバーがダウンしていると判断するために何度連続でタイム・アウトする必要があるかを決める閾値。
            デフォルトでは1回
            0以下を指定した場合、AssertionErrorとなる

        Returns
        -------
        List[Tuple[datetime.datetime, datetime.datetime]]
            サーバー上に存在するダウンタイムの開始時間と終了時間のペアをリストで返す。
            最後の記録までダウン状態と判別された場合、終了時間は`None`となる。

        Raises
        ------
        AssertionError
            `threshold` が 0以下に指定された
        """

        assert threshold > 0, "Value Error -> threshold must over 0"
        sorted_ping_results: List[Tuple[DT.datetime, int]] = sorted(self.ping_results.items())
        sorted_response: List[int] = [resp for _, resp in sorted_ping_results]
        # ダウンした列番号を取得
        down_recode: List[int] = [i for i, resp in enumerate(sorted_response) if resp == Server.TIMEOUT_SYMBOL]
        properly_recode: List[int] = [i for i, resp in enumerate(sorted_response) if resp != Server.TIMEOUT_SYMBOL]
        # 連続した番号をまとめる
        down_recode_alt: List[List[int]] = [
            list(g)
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
        for recodes in down_recode_alt:
            if len(recodes) >= threshold:
                target: int = recodes[0]
                while True:
                    if len(properly_recode_alt) != 0 and properly_recode_alt[0] < target:
                        properly_recode_alt.pop(0)
                    else:
                        break
                if len(properly_recode_alt) != 0:
                    result.append((sorted_ping_results[target][0], sorted_ping_results[properly_recode_alt.pop(0)][0]))
                else:
                    result.append((sorted_ping_results[target][0], None))
        return result


def csv_to_params(csv_text: str) -> Tuple[str, str, int, int]:
    """
    CSV1行の入力を、各パラメータに分解する
    """

    # TODO: validation
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
        追記形式でデータを読み込む

    Returns
    -------
    Dict[str, Server]
        IPアドレスに紐づいたサーバーデータ
    """

    _servers = copy.copy(servers)  # copyを行い、既存のserversを参照しないようにする
    with open(file_path) as f:
        _ = f.readline()  # ファイルの先頭は説明文なので読み飛ばす
        for line in f.readlines():
            line_strip = line.strip()
            datetime, ip_address, ip_prefix, result_msec = csv_to_params(line_strip)
            if ip_address not in _servers.keys():
                _servers[ip_address] = Server(ip_address=ip_address, ip_prefix=ip_prefix)
            _servers[ip_address].append_ping_results(datetime, result_msec)
    return _servers


def print_server_downtime(servers: Dict[str, Server], threshold=1):
    """
    サーバー郡のダウン情報を表示する

    Parameters
    ----------
    servers : Dict[str, Server]
        確認を行うサーバーリスト
    threshold : int, default=1
        サーバーがダウンしていると判断するために何度連続でタイム・アウトする必要があるかを決める閾値。
        デフォルトでは1回
        0以下を指定した場合、AssertionErrorとなる

    Returns
    -------
    List[Tuple[datetime.datetime, datetime.datetime]]
        サーバー上に存在するダウンタイムの開始時間と終了時間のペアを返す。
        記録された最後の記録がダウン状態だった場合、終了時間は`None`となる。

    Raises
    ------
    AssertionError
        `threshold` が 0以下に指定された
    """

    for server in servers.values():
        downtime_list = server.get_downtimes(threshold=threshold)
        if len(downtime_list) != 0:
            print(f"{server.ip_address} has downtime")
            for start, end in downtime_list:
                print(f"    {start} ~ {end if end is not None else ''}")
        else:
            print(f"{server.ip_address} has no downtime")


if __name__ == "__main__":
    file_path = "test_case/002.csv"
    servers = load_data(file_path=file_path)

    # Exam 1
    print("\n****** EXAM 1 ******")
    print_server_downtime(servers=servers)

    # Exam 2
    print("\n****** EXAM 2 ******")
    for threshold in range(1, 8):
        print("##########################")
        print(f"threshold: {threshold}")
        print_server_downtime(servers=servers, threshold=threshold)
