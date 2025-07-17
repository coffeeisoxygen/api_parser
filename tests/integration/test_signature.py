from unittest.mock import Mock

import pytest
from src.exceptions.app_exceptions import AppException
from src.schemas.sch_member import Member, MemberRequestWithSignature
from src.security.signature import generate_signature, verify_signature
from src.services.srv_result import ServiceResult


def test_generate_signature_php_fixture():
    # Data sesuai PHP
    memberid = "YUSUF"
    product = "X10"
    dest = "08123456789"
    refid = "2140669"
    pin = "1144"
    password = "abcd"
    expected_php = "Cp9NLVuKWBt5Sey_uMlYsvnKvJI"
    result = generate_signature(memberid, product, dest, refid, pin, password)
    assert result == expected_php


def test_verify_signature_valid():
    member = Member(
        memberid="YUSUF",
        password="abcd",
        pin="1144",
        ip="127.0.0.1",
        report_url=None,
        allow_no_sign=False,
    )
    member_service = Mock()
    member_service.get_by_id.return_value = ServiceResult(member)
    request = MemberRequestWithSignature(
        memberid="YUSUF",
        product="X10",
        dest="08123456789",
        refid="2140669",
        signature="Cp9NLVuKWBt5Sey_uMlYsvnKvJI",
    )
    assert verify_signature(request, member_service=member_service) is True


def test_verify_signature_invalid():
    member = Member(
        memberid="YUSUF",
        password="abcd",
        pin="1144",
        ip="127.0.0.1",
        report_url=None,
        allow_no_sign=False,
    )
    member_service = Mock()
    member_service.get_by_id.return_value = ServiceResult(member)
    request = MemberRequestWithSignature(
        memberid="YUSUF",
        product="X10",
        dest="08123456789",
        refid="2140669",
        signature="WRONGSIGNATURE",
    )
    with pytest.raises(AppException.InvalidSignatureError):
        verify_signature(request, member_service=member_service)
