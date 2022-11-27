import datetime as DT
import ipaddress

from fixpoint_coding_test import Server


def test_csv_to_params_01():
    text = "20201019133124,10.20.30.1/16,2"
    datetime, ip_address, ip_prefix, result_msec = Server.csv_to_params(text)
    assert datetime == "20201019133124"
    assert ip_address == "10.20.30.1"
    assert ip_prefix == 16
    assert result_msec == 2


def test_csv_to_params_02():
    text = "20201019133124,10.20.30.1/16,-"
    datetime, ip_address, ip_prefix, result_msec = Server.csv_to_params(text)
    assert datetime == "20201019133124"
    assert ip_address == "10.20.30.1"
    assert ip_prefix == 16
    assert result_msec == Server.Server.TIMEOUT_SYMBOL


def test_csv_to_params_03():
    text = "20221019133124,10.25.30.1/20,-"
    datetime, ip_address, ip_prefix, result_msec = Server.csv_to_params(text)
    assert datetime == "20221019133124"
    assert ip_address == "10.25.30.1"
    assert ip_prefix == 20
    assert result_msec == Server.Server.TIMEOUT_SYMBOL


def test_parse_datetime_01():
    text = "20201019133124"
    datetime = Server.parse_datetime(text)
    assert datetime == DT.datetime(2020, 10, 19, 13, 31, 24)


def test_load_data_01():
    file_path = "test_case/000_00.csv"
    servers = Server.load_data(file_path)
    assert servers["10.20.30.1"].ip_address == ipaddress.IPv4Address("10.20.30.1")
    assert servers["10.20.30.1"].ip_prefix == 16
    assert servers["10.20.30.1"].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 24): 2}


def test_load_data_02():
    file_path = "test_case/000_01.csv"
    servers = Server.load_data(file_path)
    print(servers["10.20.30.1"].ping_results)
    assert servers["10.20.30.1"].ip_address == ipaddress.IPv4Address("10.20.30.1")
    assert servers["10.20.30.1"].ip_prefix == 16
    assert servers["10.20.30.1"].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 25): -1}
    assert servers["10.20.30.2"].ip_address == ipaddress.IPv4Address("10.20.30.2")
    assert servers["10.20.30.2"].ip_prefix == 16
    assert servers["10.20.30.2"].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 26): 2}


def test_load_data_03():
    file_path_0 = "test_case/000_00.csv"
    servers = Server.load_data(file_path_0)
    file_path_1 = "test_case/000_01.csv"
    servers = Server.load_data(file_path_1, servers=servers)
    assert servers["10.20.30.1"].ip_address == ipaddress.IPv4Address("10.20.30.1")
    assert servers["10.20.30.1"].ip_prefix == 16
    assert servers["10.20.30.1"].ping_results == {
        DT.datetime(2020, 10, 19, 13, 31, 24): 2,
        DT.datetime(2020, 10, 19, 13, 31, 25): -1,
    }
    assert servers["10.20.30.2"].ip_address == ipaddress.IPv4Address("10.20.30.2")
    assert servers["10.20.30.2"].ip_prefix == 16
    assert servers["10.20.30.2"].ping_results == {DT.datetime(2020, 10, 19, 13, 31, 26): 2}
