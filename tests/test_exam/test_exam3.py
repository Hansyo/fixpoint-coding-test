from fixpoint_coding_test import Server


def test_exam3_00_01(capfd):
    file_path = "test_case/003_00.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:31:41 ~ 
10.20.30.2 has no overload
"""
    )


def test_exam3_01_01(capfd):
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=1, time_threshold=100)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:31:36 ~ 2020-10-19 13:31:37
    2020-10-19 13:31:38 ~ 2020-10-19 13:31:40
    2020-10-19 13:31:41 ~ 2020-10-19 13:31:44
    2020-10-19 13:31:45 ~ 2020-10-19 13:31:49
    2020-10-19 13:31:50 ~ 2020-10-19 13:31:55
    2020-10-19 13:31:56 ~ 
"""
    )


def test_exam3_01_02(capfd):
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=3, time_threshold=100)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:31:43 ~ 2020-10-19 13:31:44
    2020-10-19 13:31:47 ~ 2020-10-19 13:31:49
    2020-10-19 13:31:52 ~ 2020-10-19 13:31:55
    2020-10-19 13:31:58 ~ 
"""
    )


def test_exam3_01_03(capfd):
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=6, time_threshold=100)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:32:01 ~ 
"""
    )


def test_exam3_01_04(capfd):
    file_path = "test_case/003_01.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=7, time_threshold=100)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has no overload
"""
    )


def test_exam3_02_01(capfd):
    file_path = "test_case/003_02.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=3, time_threshold=1)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:31:24 ~ 
"""
    )


def test_exam3_02_02(capfd):
    file_path = "test_case/003_02.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=3, time_threshold=5)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:31:28 ~ 
"""
    )


def test_exam3_02_03(capfd):
    file_path = "test_case/003_02.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=3, time_threshold=30)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:31:53 ~ 
"""
    )


def test_exam3_02_04(capfd):
    file_path = "test_case/003_02.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_overload(servers=servers, continuous=5, time_threshold=30)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has overload
    2020-10-19 13:31:54 ~ 
"""
    )


def test_exam3_03_01(capfd):
    file_path = "test_case/003_03.csv"
    servers = Server.load_data(file_path=file_path)
    Server.print_server_error(servers=servers, continuous=3, time_threshold=100)
    out, _ = capfd.readouterr()
    assert (
        out
        == """10.20.30.1 has error
    server down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:31
    server overload 2020-10-19 13:31:36 ~ 2020-10-19 13:31:39
    server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:53
    server down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:59
    server overload 2020-10-19 13:32:03 ~ 2020-10-19 13:32:06
    server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:11
    server overload 2020-10-19 13:32:11 ~ 
"""
    )
