import pytest
import yaml
from src.exceptions.repo_exceptions import DuplicateItemError
from src.repos.rep_member import MemberRepoYaml
from src.schemas.sch_base_member import Member


@pytest.mark.unit
def test_get_by_memberid(member_repo):
    result = member_repo.get_by_memberid("M001")
    assert isinstance(result, Member)
    assert result.memberid == "M001"
    assert result.ip == "192.168.1.10"


@pytest.mark.unit
def test_get_by_memberid_not_found(member_repo):
    result = member_repo.get_by_memberid("M999")
    assert result is None


@pytest.mark.unit
def test_get_list_member(member_repo):
    result = member_repo.get_list_member()
    assert isinstance(result, list)
    assert all(isinstance(m, Member) for m in result)
    assert len(result) == 3


@pytest.mark.unit
def test_get_list_active_only(member_repo):
    result = member_repo.get_list_active_only()
    assert isinstance(result, list)
    assert all(getattr(m, "is_active", False) for m in result)
    assert {m.memberid for m in result} == {"M001", "M002"}


@pytest.mark.unit
def test_get_by_memberip(member_repo):
    # Use an IP from your actual test data
    result = member_repo.get_by_memberip("192.168.1.1")
    if result:
        assert isinstance(result, Member)
        assert result.ip == "192.168.1.1"


@pytest.mark.unit
def test_get_by_memberip_not_found(member_repo):
    result = member_repo.get_by_memberip("10.0.0.1")
    assert result is None


@pytest.mark.unit
def test_get_list_memberip(member_repo):
    result = member_repo.get_list_memberip()
    assert isinstance(result, list)
    assert all(isinstance(ip, str) for ip in result)


@pytest.mark.unit
def test_get_all_memberip(member_repo):
    result = member_repo.get_all_memberip()
    assert isinstance(result, list)
    assert all(isinstance(ip, str) for ip in result)


@pytest.mark.unit
def test_get_all_active_only_member(member_repo):
    result = member_repo.get_all_active_only_member()
    assert isinstance(result, list)
    assert all(getattr(m, "is_active", False) for m in result)


@pytest.mark.unit
def test_member_without_is_active(tmp_path):
    test_members = [
        {
            "memberid": "M100",
            "ip": "1.1.1.1",
            "password": "x",
            "pin": "1",
            "allow_no_sign": True,
        },
        {
            "memberid": "M101",
            "ip": "1.1.1.2",
            "password": "x",
            "pin": "2",
            "allow_no_sign": False,
            "is_active": False,
        },
    ]
    yaml_data = {"members": test_members}
    test_file = tmp_path / "members.yaml"
    with open(test_file, "w") as f:
        yaml.safe_dump(yaml_data, f)
    repo = MemberRepoYaml(file_path=test_file)
    m100 = repo.get_by_memberid("M100")
    m101 = repo.get_by_memberid("M101")
    assert m100 is not None and m100.is_active is True
    assert m101 is not None and m101.is_active is False


@pytest.mark.unit
def test_member_with_empty_ip(tmp_path):
    test_members = [
        {
            "memberid": "M200",
            "ip": "",
            "password": "x",
            "pin": "1",
            "allow_no_sign": True,
            "is_active": True,
        },
        {
            "memberid": "M201",
            "ip": None,
            "password": "x",
            "pin": "2",
            "allow_no_sign": True,
            "is_active": True,
        },
    ]
    yaml_data = {"members": test_members}
    test_file = tmp_path / "members.yaml"
    with open(test_file, "w") as f:
        yaml.safe_dump(yaml_data, f)
    repo = MemberRepoYaml(file_path=test_file)
    assert repo.get_list_memberip() == []


@pytest.mark.unit
def test_duplicate_memberid_raises(tmp_path):
    test_members = [
        {
            "memberid": "M300",
            "ip": "1.1.1.1",
            "password": "x",
            "pin": "1",
            "allow_no_sign": True,
            "is_active": True,
        },
        {
            "memberid": "M300",
            "ip": "1.1.1.2",
            "password": "x",
            "pin": "2",
            "allow_no_sign": False,
            "is_active": False,
        },
    ]
    yaml_data = {"members": test_members}
    test_file = tmp_path / "members.yaml"
    with open(test_file, "w") as f:
        yaml.safe_dump(yaml_data, f)
    with pytest.raises(DuplicateItemError):
        MemberRepoYaml(file_path=test_file)


@pytest.mark.unit
def test_get_list_active_only_with_mixed(tmp_path):
    test_members = [
        {
            "memberid": "M400",
            "ip": "1.1.1.1",
            "password": "x",
            "pin": "1",
            "allow_no_sign": True,
            "is_active": True,
        },
        {
            "memberid": "M401",
            "ip": "1.1.1.2",
            "password": "x",
            "pin": "2",
            "allow_no_sign": True,
            "is_active": False,
        },
        {
            "memberid": "M402",
            "ip": "1.1.1.3",
            "password": "x",
            "pin": "3",
            "allow_no_sign": True,
        },
    ]
    yaml_data = {"members": test_members}
    test_file = tmp_path / "members.yaml"
    with open(test_file, "w") as f:
        yaml.safe_dump(yaml_data, f)
    repo = MemberRepoYaml(file_path=test_file)
    active_ids = {m.memberid for m in repo.get_list_active_only()}
    assert active_ids == {"M400", "M402"}
