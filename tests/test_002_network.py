import datetime as DT
import ipaddress

import pytest

from fixpoint_coding_test import Network, Server


def test_create_network_01():
    ip_subnet = ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    network = Network.Network(ip_subnet)
    assert network.subnet_ipaddress == ip_subnet
    assert network.servers == []


def test_create_network_02():
    ip_subnet = ipaddress.IPv4Network("192.168.1.1/24", strict=False)
    network = Network.Network(ip_subnet)
    assert network.subnet_ipaddress == ip_subnet
    assert network.servers == []


def test_append_network_01():
    ip_address = "10.20.30.1/16"
    server = Server.Server(ip_address=ip_address)

    ip_subnet = ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    network = Network.Network(ip_subnet)

    network.add_server(server=server)
    assert network.subnet_ipaddress == ip_subnet
    assert network.servers == [server]


def test_append_network_error_01():
    ip_address = "10.20.30.1/16"
    server = Server.Server(ip_address=ip_address)

    ip_subnet = ipaddress.IPv4Network("192.168.11.1/24", strict=False)
    network = Network.Network(ip_subnet)

    with pytest.raises(AssertionError) as e:
        network.add_server(server=server)

    assert str(e.value) == "This server is not this network's subset."


def test_is_overlap_time_01():
    start1 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 8, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 9, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_02():
    start1 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 9, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 8, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_03():
    start1 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 9, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 8, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_04():
    start1 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 8, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 9, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_05():
    start1 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 7, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 8, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 9, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is False


def test_is_overlap_time_06():
    start1 = DT.datetime(2020, 10, 10, 8, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 9, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 7, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is False


def test_is_overlap_time_None_01():
    start1 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end1 = None
    start2 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 8, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_None_02():
    start1 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 8, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end2 = None
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_None_03():
    start1 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end1 = None
    start2 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 8, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_None_04():
    start1 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 8, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end2 = None
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_None_05():
    start1 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end1 = None
    start2 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end2 = None
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_None_06():
    start1 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end1 = None
    start2 = DT.datetime(2020, 10, 10, 7, 0, 0)
    end2 = None
    assert Network.is_overlap_time(start1, end1, start2, end2) is True


def test_is_overlap_time_None_07():
    start1 = DT.datetime(2020, 10, 10, 8, 0, 0)
    end1 = None
    start2 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end2 = DT.datetime(2020, 10, 10, 7, 0, 0)
    assert Network.is_overlap_time(start1, end1, start2, end2) is False


def test_is_overlap_time_None_08():
    start1 = DT.datetime(2020, 10, 10, 6, 0, 0)
    end1 = DT.datetime(2020, 10, 10, 7, 0, 0)
    start2 = DT.datetime(2020, 10, 10, 8, 0, 0)
    end2 = None
    assert Network.is_overlap_time(start1, end1, start2, end2) is False


def test_load_network_01():
    file_path = "test_case/000_00.csv"
    networks = Network.load_data(file_path=file_path)

    assert len(networks) == 1
    assert networks[0].subnet_ipaddress == ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    assert len(networks[0].servers) == 1
    assert networks[0].servers[0].ip_address == ipaddress.IPv4Interface("10.20.30.1/16")
    assert networks[0].servers[0].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 24): 2}


def test_load_network_02():
    file_path = "test_case/000_01.csv"
    networks = Network.load_data(file_path=file_path)

    assert len(networks) == 1
    assert networks[0].subnet_ipaddress == ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    assert len(networks[0].servers) == 2
    assert networks[0].servers[0].ip_address == ipaddress.IPv4Interface("10.20.30.1/16")
    assert networks[0].servers[0].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 25): -1}
    assert networks[0].servers[1].ip_address == ipaddress.IPv4Interface("10.20.30.2/16")
    assert networks[0].servers[1].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 26): 2}


def test_load_network_03():
    file_path = "test_case/000_00.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/000_01.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    assert len(networks) == 1
    assert networks[0].subnet_ipaddress == ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    assert len(networks[0].servers) == 2
    assert networks[0].servers[0].ip_address == ipaddress.IPv4Interface("10.20.30.1/16")
    assert networks[0].servers[0].ping_results == {
        DT.datetime(2020, 10, 19, 13, 31, 24): 2,
        DT.datetime(2020, 10, 19, 13, 31, 25): -1,
    }
    assert networks[0].servers[1].ip_address == ipaddress.IPv4Interface("10.20.30.2/16")
    assert networks[0].servers[1].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 26): 2}


def test_load_network_04():
    file_path = "test_case/000_01.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/004_00_01.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    assert len(networks) == 2

    assert networks[0].subnet_ipaddress == ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    assert len(networks[0].servers) == 2
    assert networks[0].servers[0].ip_address == ipaddress.IPv4Interface("10.20.30.1/16")
    assert networks[0].servers[0].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 25): -1}
    assert networks[0].servers[1].ip_address == ipaddress.IPv4Interface("10.20.30.2/16")
    assert networks[0].servers[1].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 26): 2}

    assert networks[1].subnet_ipaddress == ipaddress.IPv4Network("192.168.1.1/24", strict=False)
    assert len(networks[1].servers) == 2
    assert networks[1].servers[0].ip_address == ipaddress.IPv4Interface("192.168.1.1/24")
    assert networks[1].servers[0].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 25): -1}
    assert networks[1].servers[1].ip_address == ipaddress.IPv4Interface("192.168.1.2/24")
    assert networks[1].servers[1].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 26): 2}


def test_get_network_downtime_01():
    ip_address = "10.20.30.1/16"
    server_01 = Server.Server(ip_address=ip_address)

    datetime_str = "20201019133124"
    result_msec = Server.Server.TIMEOUT_SYMBOL
    server_01.append_ping_results(datetime_str, result_msec)

    ip_address = "10.20.30.2/16"
    server_02 = Server.Server(ip_address=ip_address)

    datetime_str = "20201019133125"
    result_msec = Server.Server.TIMEOUT_SYMBOL
    server_02.append_ping_results(datetime_str, result_msec)

    ip_subnet = ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    network = Network.Network(ip_subnet)

    network.add_server(server_01)
    network.add_server(server_02)

    assert network.get_network_downtime(continuous=1) == [(DT.datetime(2020, 10, 19, 13, 31, 25), None)]


def test_get_network_downtime_02():
    ip_address = "10.20.30.1/16"
    server_01 = Server.Server(ip_address=ip_address)

    datetime_str = "20201019133124"
    result_msec = Server.Server.TIMEOUT_SYMBOL
    server_01.append_ping_results(datetime_str, result_msec)
    datetime_str = "20201019133129"
    result_msec = 2
    server_01.append_ping_results(datetime_str, result_msec)

    ip_address = "10.20.30.2/16"
    server_02 = Server.Server(ip_address=ip_address)

    datetime_str = "20201019133125"
    result_msec = Server.Server.TIMEOUT_SYMBOL
    server_02.append_ping_results(datetime_str, result_msec)
    datetime_str = "20201019133130"
    result_msec = 2
    server_02.append_ping_results(datetime_str, result_msec)

    ip_subnet = ipaddress.IPv4Network("10.20.30.1/16", strict=False)
    network = Network.Network(ip_subnet)

    network.add_server(server_01)
    network.add_server(server_02)

    assert network.get_network_downtime(continuous=1) == [
        (DT.datetime(2020, 10, 19, 13, 31, 25), DT.datetime(2020, 10, 19, 13, 31, 29))
    ]
