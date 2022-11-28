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

    ip_address: ipaddress.IPv4Interface
    ping_results: Dict[DT.datetime, int]

    TIMEOUT_SYMBOL: int = -1

    def __init__(self, ip_address: str):
        self.ip_address = ipaddress.IPv4Interface(ip_address)
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

    def get_downtimes(self, continuous: int = 1) -> List[Tuple[DT.datetime, Optional[DT.datetime]]]:
        """
        サーバーのダウンタイム情報をすべて取得する

        Parameters
        ----------
        continuous : int, default=1
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
        ValueError
            `continuous` が 0以下に指定された
        """

        if not (continuous > 0):
            raise ValueError(f"continuous must over 0 (now {continuous})")

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
            if len(recodes) >= continuous:
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

    def get_overload_times(
        self, continuous: int = 3, time_threshold: int = 100
    ) -> List[Tuple[DT.datetime, Optional[DT.datetime]]]:
        """
        サーバーが過負荷になった期間を開始、終了日時のペアで取得する

        Parameters
        ----------
        continuous : int, default = 3
            過負荷状態と判定するために、何応答用いて平均化処理を行うかの指定。
            前方に対して平均を取り、サーバーの開始直後やタイムアウト時には、`continuous`以内の有効なデータを用いて平均を取る。
        time_threshold : int, default = 100
            過負荷状態と判定するための応答時間閾値

        Returns
        -------
        List[Tuple[datetime.datetime, datetime.datetime]]
            サーバー上に存在する過負荷状態の開始時間と終了時間のペアをリストで返す。
            最後の記録まで過負荷状態だった場合、終了時間は`None`となる。

        Raises
        ------
        ValueError
            入力値の入力範囲外の値が入力された
        """

        if not (continuous > 0):
            raise ValueError(f"continuous must over 0 (now {continuous})")
        if not (time_threshold > 0):
            raise ValueError(f"time_threshold must over 0 (now {time_threshold})")

        sorted_ping_results: List[Tuple[DT.datetime, int]] = sorted(self.ping_results.items())
        sorted_response: List[int] = [resp for _, resp in sorted_ping_results]

        # 過負荷状態の行番号を得る
        overload_list_pre: List[int] = []
        non_overload_list_pre: List[int] = []
        _is_timeout_now: bool = True
        for i in range(len(sorted_response)):
            _tmp = sorted_response[(i - continuous + 1 if i >= continuous else 0) : (i + 1)]
            _frame_timeout: bool = _tmp[-1] == Server.TIMEOUT_SYMBOL
            while Server.TIMEOUT_SYMBOL in _tmp:
                _tmp.remove(Server.TIMEOUT_SYMBOL)
            if len(_tmp) != 0:
                if (sum(_tmp) / len(_tmp)) >= time_threshold or _frame_timeout:
                    overload_list_pre.append(i)
                else:
                    non_overload_list_pre.append(i)
                _is_timeout_now = False
            else:
                if not _is_timeout_now:  # タイムアウトを検出したため、一部データのロールバックを行う
                    non_overload_list_pre.extend(overload_list_pre[-min(continuous, i) + 1 :])
                    del overload_list_pre[-min(continuous, i) + 1 :]
                    _is_timeout_now = True
                non_overload_list_pre.append(i)

        # 連続した番号をまとめる
        overload_list: List[List[int]] = [
            list(g)
            for _, g in itertools.groupby(
                overload_list_pre, key=(lambda n, c=itertools.count(): n - next(c))  # type: ignore
            )
        ]
        non_overload_list: List[int] = [
            list(g)[0]
            for _, g in itertools.groupby(
                non_overload_list_pre, key=(lambda n, c=itertools.count(): n - next(c))  # type: ignore
            )
        ]

        result: List[Tuple[DT.datetime, Optional[DT.datetime]]] = []
        for recodes in overload_list:
            target: int = recodes[0]
            while True:
                if len(non_overload_list) != 0 and non_overload_list[0] < target:
                    non_overload_list.pop(0)
                else:
                    break
            if len(non_overload_list) != 0:
                result.append((sorted_ping_results[target][0], sorted_ping_results[non_overload_list.pop(0)][0]))
            else:
                result.append((sorted_ping_results[target][0], None))
        return result


def csv_to_params(csv_text: str) -> Tuple[str, str, int]:
    """
    CSV1行の入力を、各パラメータに分解する

    Returns
    -------
    datetime : str
        日時情報
    server_address : str
        サーバーのIPアドレスとネットワークプレフィックス長のペア
    response_msec : int
        サーバーからの応答にかかった時間(ミリ秒)

    Raises
    ------
    ValueError
        正しくない入力がされた
    """

    if not (len(csv_text) != 0):
        raise ValueError("csv_text must not empty (now empty)")
    params = csv_text.split(",")
    if not (len(params) == 3):
        raise ValueError(f"'{csv_text}' is invalid format")

    datetime, server_address, result_msec_str = params
    response_msec: int = int(result_msec_str) if result_msec_str.isdigit() else Server.TIMEOUT_SYMBOL
    return datetime, server_address, response_msec


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
            if len(line_strip) == 0:  # 入力が空の場合は処理をスキップ
                continue
            datetime, server_address, result_msec = csv_to_params(line_strip)
            ip_address, _ = server_address.split("/")
            if ip_address not in _servers.keys():
                _servers[ip_address] = Server(ip_address=server_address)
            _servers[ip_address].append_ping_results(datetime, result_msec)
    return _servers


def print_server_downtime(servers: Dict[str, Server], continuous: int = 1):
    """
    サーバー群のダウン情報を表示する

    Parameters
    ----------
    servers : Dict[str, Server]
        確認を行うサーバーリスト
    threshold : int, default=1
        サーバーがダウンしていると判断するために何度連続でタイム・アウトする必要があるかを決める閾値。
        デフォルトでは1回
        0以下を指定した場合、ValueErrorとなる

    Returns
    -------
    List[Tuple[datetime.datetime, datetime.datetime]]
        サーバー上に存在するダウンタイムの開始時間と終了時間のペアを返す。
        記録された最後の記録がダウン状態だった場合、終了時間は`None`となる。

    Raises
    ------
    ValueError
        `threshold` が 0以下に指定された
    """

    for server in servers.values():
        downtime_list = server.get_downtimes(continuous=continuous)
        if len(downtime_list) != 0:
            print(f"{server.ip_address.ip} has downtime")
            for start, end in downtime_list:
                print(f"    {start} ~ {end if end is not None else ''}")
        else:
            print(f"{server.ip_address.ip} has no downtime")


def print_server_overload(servers: Dict[str, Server], continuous: int = 3, time_threshold: int = 100):
    """
    サーバー群の過負荷情報を表示する

    Parameters
    ----------
    servers : Dict[str, Server]
        確認を行うサーバーリスト
    continuous : int, default = 3
        過負荷状態と判定するために、何応答用いて平均化処理を行うかの指定。
        前方に対して平均を取り、サイバーの開始直後はすでにあるデータのみを用いて平均を取る。
    time_threshold : int, default = 100
        過負荷状態と判定するための応答時間閾値。

    Raises
    ------
    ValueError
        `continuous`か`time_threshold` が0以下に指定された。
    """

    for server in servers.values():
        overload_list = server.get_overload_times(continuous=continuous, time_threshold=time_threshold)
        if len(overload_list) != 0:
            print(f"{server.ip_address.ip} has overload")
            for start, end in overload_list:
                print(f"    {start} ~ {end if end is not None else ''}")
        else:
            print(f"{server.ip_address.ip} has no overload")


def print_server_error(servers: Dict[str, Server], continuous: int = 3, time_threshold: int = 100):
    """
    サーバー群のダウン情報と過負荷情報を表示する

    Parameters
    ----------
    servers : Dict[str, Server]
        確認を行うサーバーリスト
    continuous : int, default = 3
        ダウン/過負荷状態と判定するために、何応答分まとめて処理を行うかの指定。
    time_threshold : int, default = 100
        過負荷状態と判定するための応答時間閾値。

    Raises
    ------
    ValueError
        `continuous`か`time_threshold` が0以下に指定された。
    """

    def _add_label(
        time_pair: Tuple[DT.datetime, Optional[DT.datetime]], label: str
    ) -> Tuple[DT.datetime, Optional[DT.datetime], str]:
        return (time_pair[0], time_pair[1], label)

    for server in servers.values():
        downtime_list_pre = server.get_downtimes(continuous=continuous)
        downtime_list = [_add_label(data, "downtime") for data in downtime_list_pre]
        overload_list_pre = server.get_overload_times(continuous=continuous, time_threshold=time_threshold)
        overload_list = [_add_label(data, "overload") for data in overload_list_pre]
        errors_list = sorted(downtime_list + overload_list)

        if len(errors_list) != 0:
            print(f"{server.ip_address.ip} has error")
            for start, end, label in errors_list:
                print(f"    {label} {start} ~ {end if end is not None else ''}")
        else:
            print(f"{server.ip_address.ip} has no error")


if __name__ == "__main__":
    file_path = "test_case/002.csv"
    servers = load_data(file_path=file_path)

    # Exam 1
    print("\n****** EXAM 1 ******")
    print_server_downtime(servers=servers)

    # Exam 2
    print("\n****** EXAM 2 ******")
    for continuous in range(1, 8):
        print("##########################")
        print(f"threshold: {continuous}")
        print_server_downtime(servers=servers, continuous=continuous)

    # Exam 3
    print("\n****** EXAM 3 ******")
    file_path = "test_case/003_03.csv"
    servers = load_data(file_path=file_path)
    print_server_error(servers=servers)
