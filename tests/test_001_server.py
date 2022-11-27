import datetime as DT
import ipaddress

from fixpoint_coding_test import Server


def test_create_server_instance_01():
    ip_address = "10.20.30.1"
    ip_prefix = 16
    server = Server.Server(ip_address=ip_address, ip_prefix=ip_prefix)
    assert server.ip_address == ipaddress.IPv4Address("10.20.30.1")
    assert server.ip_prefix == 16


def test_append_ping_results_01():
    ip_address = "10.20.30.1"
    ip_prefix = 16
    datetime_str = "20201019133124"
    result_msec = 2
    server = Server.Server(ip_address=ip_address, ip_prefix=ip_prefix)
    server.append_ping_results(datetime_str, result_msec)
    assert server.ping_results == {DT.datetime(2020, 10, 19, 13, 31, 24): 2}


def test_get_downtimes_01():
    file_path = "test_case/000_01.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_downtimes() == [(DT.datetime(2020, 10, 19, 13, 31, 25), None)]
    assert servers["10.20.30.2"].get_downtimes() == []


def test_get_downtimes_02():
    file_path = "test_case/002.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_downtimes() == [
        (DT.datetime(2020, 10, 19, 13, 31, 36), DT.datetime(2020, 10, 19, 13, 31, 37)),
        (DT.datetime(2020, 10, 19, 13, 31, 38), DT.datetime(2020, 10, 19, 13, 31, 40)),
        (DT.datetime(2020, 10, 19, 13, 31, 41), DT.datetime(2020, 10, 19, 13, 31, 44)),
        (DT.datetime(2020, 10, 19, 13, 31, 45), DT.datetime(2020, 10, 19, 13, 31, 49)),
        (DT.datetime(2020, 10, 19, 13, 31, 50), DT.datetime(2020, 10, 19, 13, 31, 55)),
        (DT.datetime(2020, 10, 19, 13, 31, 56), None),
    ]


def test_get_downtimes_03():
    file_path = "test_case/002.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_downtimes(3) == [
        (DT.datetime(2020, 10, 19, 13, 31, 41), DT.datetime(2020, 10, 19, 13, 31, 44)),
        (DT.datetime(2020, 10, 19, 13, 31, 45), DT.datetime(2020, 10, 19, 13, 31, 49)),
        (DT.datetime(2020, 10, 19, 13, 31, 50), DT.datetime(2020, 10, 19, 13, 31, 55)),
        (DT.datetime(2020, 10, 19, 13, 31, 56), None),
    ]