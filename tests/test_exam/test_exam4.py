import datetime as DT
import ipaddress

import pytest

from fixpoint_coding_test import Network


def test_exam4_01(capfd: pytest.CaptureFixture):
    file_path = "test_case/004_01_01.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/004_01_02.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    Network.print_networks_error(
        networks=networks, continuous=3, with_server_timeout=False, with_server_overload=False
    )

    out, _ = capfd.readouterr()
    assert (
        out
        == """\
10.20.0.0/16 has error
    10.20.0.0/16 switch down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:30
    10.20.0.0/16 switch down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:42
    10.20.0.0/16 switch down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:58
    10.20.0.0/16 switch down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    10.20.0.0/16 switch down 2020-10-19 13:32:15 ~ 
"""
    )


def test_exam4_02(capfd: pytest.CaptureFixture):
    file_path = "test_case/004_01_01.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/004_01_02.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    Network.print_networks_error(networks=networks, continuous=3, with_server_timeout=True, with_server_overload=False)

    out, _ = capfd.readouterr()
    assert (
        out
        == """\
10.20.0.0/16 has error
    10.20.30.2/16 server down 2020-10-19 13:31:25 ~ 2020-10-19 13:31:30
    10.20.0.0/16 switch down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:30
    10.20.30.1/16 server down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:31
    10.20.30.2/16 server down 2020-10-19 13:31:38 ~ 2020-10-19 13:31:42
    10.20.0.0/16 switch down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:42
    10.20.30.1/16 server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    10.20.30.2/16 server down 2020-10-19 13:31:54 ~ 2020-10-19 13:31:58
    10.20.0.0/16 switch down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:58
    10.20.30.1/16 server down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:59
    10.20.30.2/16 server down 2020-10-19 13:32:05 ~ 2020-10-19 13:32:10
    10.20.0.0/16 switch down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    10.20.30.1/16 server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:11
    10.20.30.2/16 server down 2020-10-19 13:32:14 ~ 
    10.20.0.0/16 switch down 2020-10-19 13:32:15 ~ 
    10.20.30.1/16 server down 2020-10-19 13:32:15 ~ 
"""
    )


def test_exam4_03(capfd: pytest.CaptureFixture):
    file_path = "test_case/004_01_01.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/004_01_02.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    Network.print_networks_error(
        networks=networks, continuous=3, with_server_timeout=False, with_server_overload=True, time_threshold=100
    )

    out, _ = capfd.readouterr()
    assert (
        out
        == """\
10.20.0.0/16 has error
    10.20.0.0/16 switch down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:30
    10.20.30.2/16 server overload 2020-10-19 13:31:35 ~ 2020-10-19 13:31:38
    10.20.30.1/16 server overload 2020-10-19 13:31:36 ~ 2020-10-19 13:31:39
    10.20.0.0/16 switch down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:42
    10.20.30.2/16 server overload 2020-10-19 13:31:42 ~ 2020-10-19 13:31:52
    10.20.30.1/16 server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:53
    10.20.0.0/16 switch down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:58
    10.20.30.2/16 server overload 2020-10-19 13:32:02 ~ 2020-10-19 13:32:05
    10.20.30.1/16 server overload 2020-10-19 13:32:03 ~ 2020-10-19 13:32:06
    10.20.0.0/16 switch down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    10.20.30.2/16 server overload 2020-10-19 13:32:10 ~ 2020-10-19 13:32:14
    10.20.30.1/16 server overload 2020-10-19 13:32:11 ~ 2020-10-19 13:32:15
    10.20.0.0/16 switch down 2020-10-19 13:32:15 ~ 
"""
    )


def test_exam4_04(capfd: pytest.CaptureFixture):
    file_path = "test_case/004_01_01.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/004_01_02.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    Network.print_networks_error(
        networks=networks, continuous=3, with_server_timeout=True, with_server_overload=True, time_threshold=100
    )

    out, _ = capfd.readouterr()
    assert (
        out
        == """\
10.20.0.0/16 has error
    10.20.30.2/16 server down 2020-10-19 13:31:25 ~ 2020-10-19 13:31:30
    10.20.0.0/16 switch down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:30
    10.20.30.1/16 server down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:31
    10.20.30.2/16 server overload 2020-10-19 13:31:35 ~ 2020-10-19 13:31:38
    10.20.30.1/16 server overload 2020-10-19 13:31:36 ~ 2020-10-19 13:31:39
    10.20.30.2/16 server down 2020-10-19 13:31:38 ~ 2020-10-19 13:31:42
    10.20.0.0/16 switch down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:42
    10.20.30.1/16 server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    10.20.30.2/16 server overload 2020-10-19 13:31:42 ~ 2020-10-19 13:31:52
    10.20.30.1/16 server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:53
    10.20.30.2/16 server down 2020-10-19 13:31:54 ~ 2020-10-19 13:31:58
    10.20.0.0/16 switch down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:58
    10.20.30.1/16 server down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:59
    10.20.30.2/16 server overload 2020-10-19 13:32:02 ~ 2020-10-19 13:32:05
    10.20.30.1/16 server overload 2020-10-19 13:32:03 ~ 2020-10-19 13:32:06
    10.20.30.2/16 server down 2020-10-19 13:32:05 ~ 2020-10-19 13:32:10
    10.20.0.0/16 switch down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    10.20.30.1/16 server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:11
    10.20.30.2/16 server overload 2020-10-19 13:32:10 ~ 2020-10-19 13:32:14
    10.20.30.1/16 server overload 2020-10-19 13:32:11 ~ 2020-10-19 13:32:15
    10.20.30.2/16 server down 2020-10-19 13:32:14 ~ 
    10.20.0.0/16 switch down 2020-10-19 13:32:15 ~ 
    10.20.30.1/16 server down 2020-10-19 13:32:15 ~ 
"""
    )


def test_exam4_05(capfd: pytest.CaptureFixture):
    file_path = "test_case/004_02_01.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/004_02_02.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    Network.print_networks_error(
        networks=networks, continuous=3, with_server_timeout=True, with_server_overload=True, time_threshold=100
    )

    out, _ = capfd.readouterr()
    assert (
        out
        == """\
192.168.1.0/24 has error
    192.168.1.2/24 server down 2020-10-19 13:31:25 ~ 2020-10-19 13:31:30
    192.168.1.0/24 switch down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:30
    192.168.1.1/24 server down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:31
    192.168.1.2/24 server overload 2020-10-19 13:31:35 ~ 2020-10-19 13:31:39
    192.168.1.1/24 server overload 2020-10-19 13:31:36 ~ 2020-10-19 13:31:39
    192.168.1.0/24 switch down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    192.168.1.1/24 server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    192.168.1.2/24 server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    192.168.1.2/24 server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:52
    192.168.1.1/24 server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:53
    192.168.1.2/24 server down 2020-10-19 13:31:54 ~ 2020-10-19 13:31:58
    192.168.1.0/24 switch down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:58
    192.168.1.1/24 server down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:59
    192.168.1.2/24 server overload 2020-10-19 13:32:02 ~ 2020-10-19 13:32:06
    192.168.1.1/24 server overload 2020-10-19 13:32:03 ~ 2020-10-19 13:32:06
    192.168.1.0/24 switch down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    192.168.1.2/24 server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    192.168.1.1/24 server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:11
    192.168.1.2/24 server overload 2020-10-19 13:32:10 ~ 
    192.168.1.1/24 server overload 2020-10-19 13:32:11 ~ 
"""
    )


def test_exam4_06(capfd: pytest.CaptureFixture):
    file_path = "test_case/004_01_01.csv"
    networks = Network.load_data(file_path=file_path)
    file_path = "test_case/004_01_02.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)
    file_path = "test_case/004_02_01.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)
    file_path = "test_case/004_02_02.csv"
    networks = Network.load_data(file_path=file_path, networks=networks)

    Network.print_networks_error(
        networks=networks, continuous=3, with_server_timeout=True, with_server_overload=True, time_threshold=100
    )

    out, _ = capfd.readouterr()
    assert (
        out
        == """\
10.20.0.0/16 has error
    10.20.30.2/16 server down 2020-10-19 13:31:25 ~ 2020-10-19 13:31:30
    10.20.0.0/16 switch down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:30
    10.20.30.1/16 server down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:31
    10.20.30.2/16 server overload 2020-10-19 13:31:35 ~ 2020-10-19 13:31:38
    10.20.30.1/16 server overload 2020-10-19 13:31:36 ~ 2020-10-19 13:31:39
    10.20.30.2/16 server down 2020-10-19 13:31:38 ~ 2020-10-19 13:31:42
    10.20.0.0/16 switch down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:42
    10.20.30.1/16 server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    10.20.30.2/16 server overload 2020-10-19 13:31:42 ~ 2020-10-19 13:31:52
    10.20.30.1/16 server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:53
    10.20.30.2/16 server down 2020-10-19 13:31:54 ~ 2020-10-19 13:31:58
    10.20.0.0/16 switch down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:58
    10.20.30.1/16 server down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:59
    10.20.30.2/16 server overload 2020-10-19 13:32:02 ~ 2020-10-19 13:32:05
    10.20.30.1/16 server overload 2020-10-19 13:32:03 ~ 2020-10-19 13:32:06
    10.20.30.2/16 server down 2020-10-19 13:32:05 ~ 2020-10-19 13:32:10
    10.20.0.0/16 switch down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    10.20.30.1/16 server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:11
    10.20.30.2/16 server overload 2020-10-19 13:32:10 ~ 2020-10-19 13:32:14
    10.20.30.1/16 server overload 2020-10-19 13:32:11 ~ 2020-10-19 13:32:15
    10.20.30.2/16 server down 2020-10-19 13:32:14 ~ 
    10.20.0.0/16 switch down 2020-10-19 13:32:15 ~ 
    10.20.30.1/16 server down 2020-10-19 13:32:15 ~ 
192.168.1.0/24 has error
    192.168.1.2/24 server down 2020-10-19 13:31:25 ~ 2020-10-19 13:31:30
    192.168.1.0/24 switch down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:30
    192.168.1.1/24 server down 2020-10-19 13:31:26 ~ 2020-10-19 13:31:31
    192.168.1.2/24 server overload 2020-10-19 13:31:35 ~ 2020-10-19 13:31:39
    192.168.1.1/24 server overload 2020-10-19 13:31:36 ~ 2020-10-19 13:31:39
    192.168.1.0/24 switch down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    192.168.1.1/24 server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    192.168.1.2/24 server down 2020-10-19 13:31:39 ~ 2020-10-19 13:31:43
    192.168.1.2/24 server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:52
    192.168.1.1/24 server overload 2020-10-19 13:31:43 ~ 2020-10-19 13:31:53
    192.168.1.2/24 server down 2020-10-19 13:31:54 ~ 2020-10-19 13:31:58
    192.168.1.0/24 switch down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:58
    192.168.1.1/24 server down 2020-10-19 13:31:55 ~ 2020-10-19 13:31:59
    192.168.1.2/24 server overload 2020-10-19 13:32:02 ~ 2020-10-19 13:32:06
    192.168.1.1/24 server overload 2020-10-19 13:32:03 ~ 2020-10-19 13:32:06
    192.168.1.0/24 switch down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    192.168.1.2/24 server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:10
    192.168.1.1/24 server down 2020-10-19 13:32:06 ~ 2020-10-19 13:32:11
    192.168.1.2/24 server overload 2020-10-19 13:32:10 ~ 
    192.168.1.1/24 server overload 2020-10-19 13:32:11 ~ 
"""
    )
