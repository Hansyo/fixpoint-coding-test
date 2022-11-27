import datetime as DT

from fixpoint_coding_test import Server


def test_exam2_01(capfd):
    file_path = "test_case/000_01.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_downtime(servers=servers)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has downtime
    2020-10-19 13:31:25 ~ 
10.20.30.2 has no downtime
"""
    )


def test_exam2_02(capfd):
    file_path = "test_case/002.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_downtime(servers=servers, threshold=1)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has downtime
    2020-10-19 13:31:36 ~ 2020-10-19 13:31:37
    2020-10-19 13:31:38 ~ 2020-10-19 13:31:40
    2020-10-19 13:31:41 ~ 2020-10-19 13:31:44
    2020-10-19 13:31:45 ~ 2020-10-19 13:31:49
    2020-10-19 13:31:50 ~ 2020-10-19 13:31:55
    2020-10-19 13:31:56 ~ 
"""
    )


def test_exam2_03(capfd):
    file_path = "test_case/002.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_downtime(servers=servers, threshold=3)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has downtime
    2020-10-19 13:31:41 ~ 2020-10-19 13:31:44
    2020-10-19 13:31:45 ~ 2020-10-19 13:31:49
    2020-10-19 13:31:50 ~ 2020-10-19 13:31:55
    2020-10-19 13:31:56 ~ 
"""
    )


def test_exam2_04(capfd):
    file_path = "test_case/002.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_downtime(servers=servers, threshold=6)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has downtime
    2020-10-19 13:31:56 ~ 
"""
    )


def test_exam2_05(capfd):
    file_path = "test_case/002.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_downtime(servers=servers, threshold=7)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has no downtime
"""
    )
