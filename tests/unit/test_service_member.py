from src.exceptions.app_exceptions import AppExceptionError
from src.schemas.sch_member import Member
from src.services.srv_member import MemberService
from src.services.srv_result import ServiceResult


def test_get_by_ip(member_repo):
    service = MemberService(member_repo)
    members = member_repo.all()
    if members:
        ip = members[0].ip
        result = service.get_by_ip(ip)
        assert isinstance(result, ServiceResult)
        assert result.success
        assert isinstance(result.data, Member)
        assert result.data.ip == ip
    else:
        result = service.get_by_ip("127.0.0.1")
        assert not result.success
        assert result.data is None or isinstance(result.data, AppExceptionError)
        if isinstance(result.data, AppExceptionError):
            assert "ip" in result.data.context


def test_get_by_id(member_repo):
    service = MemberService(member_repo)
    members = member_repo.all()
    if members:
        memberid = members[0].memberid
        result = service.get_by_id(memberid)
        assert result.success
        assert isinstance(result.data, Member)
        assert result.data.memberid == memberid
    else:
        result = service.get_by_id("dummyid")
        assert not result.success
        assert result.data is None or isinstance(result.data, AppExceptionError)
        if isinstance(result.data, AppExceptionError):
            assert "memberid" in result.data.context


def test_verify_pin_password(member_repo):
    service = MemberService(member_repo)
    members = member_repo.all()
    if members:
        m = members[0]
        result = service.verify_pin_password(m.memberid, m.pin, m.password)
        assert result.success
        assert isinstance(result.data, Member)
        assert result.data.memberid == m.memberid
        # Test wrong pin
        result_fail = service.verify_pin_password(m.memberid, "wrong", m.password)
        assert not result_fail.success
        assert result_fail.data is None or isinstance(
            result_fail.data, AppExceptionError
        )
        if isinstance(result_fail.data, AppExceptionError):
            assert "memberid" in result_fail.data.context
    else:
        result = service.verify_pin_password("dummyid", "1234", "pass")
        assert not result.success
        assert result.data is None or isinstance(result.data, AppExceptionError)
        if isinstance(result.data, AppExceptionError):
            assert "memberid" in result.data.context


def test_is_signature_required(member_repo):
    service = MemberService(member_repo)
    members = member_repo.all()
    if members:
        m = members[0]
        result = service.is_signature_required(m.memberid)
        assert isinstance(result, ServiceResult)
        assert result.success
        assert isinstance(result.data, bool)
    else:
        result = service.is_signature_required("dummyid")
        assert result.success
        assert result.data is True


def test_get_report_url(member_repo):
    service = MemberService(member_repo)
    members = member_repo.all()
    if members:
        m = members[0]
        result = service.get_report_url(m.memberid)
        assert result.success
        assert isinstance(result.data, str)
    else:
        result = service.get_report_url("dummyid")
        assert not result.success
        assert result.data is None or isinstance(result.data, AppExceptionError)
        if isinstance(result.data, AppExceptionError):
            assert "memberid" in result.data.context


def test_all_members(member_repo):
    service = MemberService(member_repo)
    result = service.all_members()
    assert result.success
    assert isinstance(result.data, list)
