import datetime as DT
import ipaddress

from fixpoint_coding_test import Server


def test_create_server_instance_01():
    ip_address = "10.20.30.1/16"
    server = Server.Server(ip_address=ip_address)
    assert server.ip_address == ipaddress.IPv4Interface("10.20.30.1/16")


def test_append_ping_results_01():
    ip_address = "10.20.30.1/16"
    datetime_str = "20201019133124"
    result_msec = 2
    server = Server.Server(ip_address=ip_address)
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


def test_get_downtimes_04():
    file_path = "test_case/003_03.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_downtimes(5) == [
        (DT.datetime(2020, 10, 19, 13, 31, 26), DT.datetime(2020, 10, 19, 13, 31, 31)),
        (DT.datetime(2020, 10, 19, 13, 32, 6), DT.datetime(2020, 10, 19, 13, 32, 11)),
    ]


def test_get_overload_01():
    file_path = "test_case/003_00.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_overload_times() == [
        (DT.datetime(2020, 10, 19, 13, 31, 41), None),
    ]
    assert servers["10.20.30.2"].get_overload_times() == []


def test_get_overload_02():
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_overload_times(continuous=3) == [
        (DT.datetime(2020, 10, 19, 13, 31, 43), DT.datetime(2020, 10, 19, 13, 31, 44)),
        (DT.datetime(2020, 10, 19, 13, 31, 47), DT.datetime(2020, 10, 19, 13, 31, 49)),
        (DT.datetime(2020, 10, 19, 13, 31, 52), DT.datetime(2020, 10, 19, 13, 31, 55)),
        (DT.datetime(2020, 10, 19, 13, 31, 58), None),
    ]


def test_get_overload_03():
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_overload_times(continuous=5) == [
        (DT.datetime(2020, 10, 19, 13, 31, 54), DT.datetime(2020, 10, 19, 13, 31, 55)),
        (DT.datetime(2020, 10, 19, 13, 32, 00), None),
    ]


def test_get_overload_04():
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_overload_times(time_threshold=60) == [
        (DT.datetime(2020, 10, 19, 13, 31, 38), None),
    ]


def test_get_overload_05():
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_overload_times(continuous=5, time_threshold=80) == [
        (DT.datetime(2020, 10, 19, 13, 31, 42), DT.datetime(2020, 10, 19, 13, 31, 44)),
        (DT.datetime(2020, 10, 19, 13, 31, 45), None),
    ]


def test_get_overload_06():
    file_path = "test_case/003_03.csv"
    servers = Server.load_data(file_path=file_path)
    assert servers["10.20.30.1"].get_overload_times(continuous=5, time_threshold=60) == [
        (DT.datetime(2020, 10, 19, 13, 31, 35), DT.datetime(2020, 10, 19, 13, 31, 59)),
        (DT.datetime(2020, 10, 19, 13, 32, 3), DT.datetime(2020, 10, 19, 13, 32, 6)),
        (DT.datetime(2020, 10, 19, 13, 32, 11), None),
    ]
