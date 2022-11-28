import copy
import datetime as DT
import ipaddress
from typing import Dict, List, Optional, Set, Tuple, Union

from fixpoint_coding_test.Server import Server, csv_to_params


class Network:
    """
    同一ネットワークサブネット内のサーバーをまとめて管理する
    """

    subnet_ipaddress: ipaddress.IPv4Network
    servers: List[Server]

    def __init__(self, subnet_ipaddress: ipaddress.IPv4Network) -> None:
        self.subnet_ipaddress: ipaddress.IPv4Network = subnet_ipaddress
        self.servers: List[Server] = []

    def add_server(self, server: Server) -> None:
        """
        ネットワークにサーバーを追加する

        Parameters
        ----------
        server : Server
            ネットワークに登録する`Server`インスタンス

        Raises
        ------
        ValueError
            追加するサーバーがネットワークに所属していない
        """

        if not (self.is_inside_network_ip(server=server)):
            raise ValueError("This server is not this network's subset.")
        self.servers.append(server)

    def is_inside_network_ip(self, server: Server) -> bool:
        """
        ネットワークにサーバーが所属可能か検査する

        Parameters
        ----------
        server : Server
            確認を行う`Server`インスタンス

        Returns
        -------
        bool
            サブネットの範囲内であれば`True`
        """

        return server.ip_address in self.subnet_ipaddress

    def get_network_downtime(self, continuous: int = 3) -> List[Tuple[DT.datetime, Optional[DT.datetime]]]:
        """
        ネットワークがダウンしている期間の開始日時と終了日時を取得する。
        ネットワークがダウンしている期間は、全てのサーバーがダウンしている最短期間となる。

        Parameters
        ----------
        continuous : int, default = 3
            サーバーがダウンしていることを判定するために、何度連続で応答が無いかを決定する閾値。

        Returns
        -------
        List[Tuple[DT.datetime, Optional[DT.datetime]]]
            ネットワークがダウンしている開始日時と終了日時のペア。ログの末尾までダウンしている場合、終了日時は`None`となる。

        Raises
        ------
        ValueError
            `continuous` が 0以下に指定された


        Example1
        --------
        出力は、実際には`datetime`オブジェクト(もしくは`None`)である点に注意。\n
        server A -> 2020-10-13 10:00:00 ~ 2020-10-13 10:45:00\n
        server B -> 2020-10-13 10:15:00 ~ 2020-10-13 11:00:00\n
        Result: ["2020-10-13 10:15:00", 2020-10-13 10:45:00]

        Example2
        --------
        出力は、実際には`datetime`オブジェクト(もしくは`None`)である点に注意。\n
        server A -> 2020-10-13 10:00:00 ~ None\n
        server B -> 2020-10-13 10:15:00 ~ None\n
        Result: ["2020-10-13 10:15:00", None]
        """

        if not (continuous > 0):
            raise ValueError(f"continuous must over 0 (now {continuous})")

        # ネットワーク内の全てのサーバーのダウンタイムを取得する
        downtimes: Dict[ipaddress.IPv4Interface, List[Tuple[DT.datetime, Optional[DT.datetime]]]] = {
            server.ip_address: server.get_downtimes(continuous=continuous) for server in self.servers
        }

        results_set: Set[Tuple[DT.datetime, Optional[DT.datetime]]] = set()

        for ip_address, _tmp_downtimes in downtimes.items():
            for outer_start, outer_end in _tmp_downtimes:
                _inside_results = False
                for inner_start, inner_end in results_set:
                    # 既存のリザルトにデータが存在している場合、スキップ
                    if is_overlap_time(outer_start, outer_end, inner_start, inner_end):
                        _inside_results = True
                        break
                if _inside_results:
                    continue

                for server in self.servers:
                    if server.ip_address is ip_address:
                        continue  # 自身に対してはスキップする

                    for inner_start, inner_end in downtimes[server.ip_address]:
                        if is_overlap_time(outer_start, outer_end, inner_start, inner_end):
                            # 開始時刻の更新: 遅い方に変更する
                            outer_start = max(outer_start, inner_start)

                            # 終了時刻の更新
                            if inner_end is None:
                                # inner_endがNoneな場合 -> outer_endを残す = Do nothing.
                                pass
                            elif outer_end is None:
                                # outer_endがNoneな場合 -> inner_endを残す
                                outer_end = inner_end
                            else:
                                # どちらでもないときは終了時刻を早い方に変更
                                outer_end = min(outer_end, inner_end)

                            # 有効なペアが発見できているため、同一サーバ内の追加確認をスキップ
                            break  # breakするとfor文のelse処理に到達せずにおわる
                    else:
                        # 全てのパターンで条件に当てはまらなかったため、外側のペアを進める
                        break
                else:
                    # パターンが見つかったため、resultsに登録
                    results_set.add((outer_start, outer_end))

        return sorted(list(results_set))


def is_overlap_time(
    start1: DT.datetime, end1: Optional[DT.datetime], start2: DT.datetime, end2: Optional[DT.datetime]
) -> bool:
    """
    2つの時刻の範囲が重複しているか判定する。
    """
    flag_s1_e2 = end2 is None or start1 <= end2
    flag_e1_s2 = end1 is None or end1 >= start2

    return flag_s1_e2 and flag_e1_s2


def load_data(file_path: str, networks: List[Network] = []) -> List[Network]:
    """
    ログデータからネットワーク切り分けの行われたサーバーデータを生成する

    Parameters
    ----------
    file_path : str
        ログデータのファイルパス
    networks : List[Network], optional
        既存のデータがある場合のみ指定。
        追記形式でデータを読み込む

    Returns
    -------
    List[Network]
        IPアドレスで切り分けられたネットワークリスト
    """

    _networks = copy.copy(networks)
    with open(file_path) as f:
        _ = f.readline()  # ファイルの先頭は説明文なので読み飛ばす
        for line in f.readlines():
            line_strip = line.strip()
            if len(line_strip) == 0:  # 入力が空の場合は処理をスキップ
                continue
            datetime, ip_address, response_msec = csv_to_params(line_strip)
            _tmp_ip = ipaddress.IPv4Interface(ip_address)
            for network in _networks:
                if network.subnet_ipaddress == _tmp_ip.network:
                    # 既存ネットワーク上にデータを記録する
                    for server in network.servers:
                        if server.ip_address == _tmp_ip:
                            # 既存のサーバに記録する
                            server.append_ping_results(datetime_str=datetime, response_msec=response_msec)
                            break
                    else:
                        # 新規サーバーに記録する
                        server = Server(ip_address=ip_address)
                        server.append_ping_results(datetime_str=datetime, response_msec=response_msec)
                        network.add_server(server=server)
                    break
            else:
                # 新規ネットワーク & 新規サーバに記録する
                server = Server(ip_address=ip_address)
                server.append_ping_results(datetime_str=datetime, response_msec=response_msec)

                network = Network(_tmp_ip.network)
                network.add_server(server=server)
                _networks.append(network)

    return _networks


def print_networks_error(
    networks: List[Network],
    continuous: int = 3,
    with_server_timeout: bool = True,
    with_server_overload: bool = True,
    time_threshold: int = 100,
) -> None:
    """ネットワーク内のエラー情報を含めたサーバーエラー情報を出力する

    Parameters
    ----------
    networks : List[Network]
        表示するネットワークリスト
    continuous : int, default = 3
        ダウン/過負荷状態と判定するために、何応答分まとめて処理を行うかの指定。
    with_server_timeout : bool, default = True
        サーバータイムアウト情報を同時に出力するかどうかを指定する
    with_server_overload : bool, default = True
        サーバー過負荷情報を同時に出力するかどうかを指定する
    time_threshold : int, default = 100
        過負荷状態と判定するための応答時間閾値

    Raises
    ------
    ValueError
        入力値の入力範囲外の値が入力された
    """

    if not (continuous > 0):
        raise ValueError(f"continuous must over 0 (now {continuous})")
    if not (time_threshold > 0):
        raise ValueError(f"time_threshold must over 0 (now {time_threshold})")

    def _add_label(
        time_pair: Tuple[DT.datetime, Optional[DT.datetime]],
        address: Union[ipaddress.IPv4Interface, ipaddress.IPv4Network],
        label: str,
    ) -> Tuple[DT.datetime, Optional[DT.datetime], Union[ipaddress.IPv4Interface, ipaddress.IPv4Network], str]:
        return (time_pair[0], time_pair[1], address, label)

    SWITCH_DOWN_LABEL = "switch down"
    DOWNTIME_LABEL = "downtime"
    OVERLOAD_LABEL = "overload"

    for network in networks:
        network_downtime_list_pre = network.get_network_downtime(continuous=continuous)
        network_downtime_list = [
            _add_label(data, network.subnet_ipaddress, SWITCH_DOWN_LABEL) for data in network_downtime_list_pre
        ]

        downtime_list = []
        overload_list = []
        for server in network.servers:
            if with_server_timeout:
                downtime_list_pre = server.get_downtimes(continuous=continuous)
                downtime_list.extend(
                    [_add_label(data, server.ip_address, DOWNTIME_LABEL) for data in downtime_list_pre]
                )
            if with_server_overload:
                overload_list_pre = server.get_overload_times(continuous=continuous, time_threshold=time_threshold)
                overload_list.extend(
                    [_add_label(data, server.ip_address, OVERLOAD_LABEL) for data in overload_list_pre]
                )

        errors_list = sorted(network_downtime_list + downtime_list + overload_list, key=lambda x: x[0:2])
        if len(errors_list) != 0:
            print(f"{network.subnet_ipaddress}", "has error" if len(network_downtime_list) != 0 else "summary")
            for start, end, address, label in errors_list:
                print(f"    {address} {label} {start} ~ {end if end is not None else ''}")
        else:
            print(f"{network.subnet_ipaddress} has no error")
