"""Service untuk validasi akses Member dari request."""

from fastapi import Depends

from src.exceptions.app_exceptions import AppException
from src.schemas.sch_member import (
    MemberRequestWithoutSignature,
    MemberRequestWithSignature,
)
from src.security.signature import generate_signature
from src.services.srv_member import MemberService
from src.services.srv_result import ServiceResult, handle_result


class ValidationService:
    def __init__(self, member_service: MemberService = Depends()):  # noqa: B008
        self.member_service = member_service

    def validate_with_signature(
        self, request: MemberRequestWithSignature
    ) -> ServiceResult:
        member = handle_result(self.member_service.get_by_id(request.memberid))

        expected = generate_signature(
            memberid=request.memberid,
            product=request.product,
            dest=request.dest,
            refid=request.refid,
            pin=member.pin,
            password=member.password,
        )

        if request.signature != expected:
            return ServiceResult(AppException.InvalidSignatureError(request.signature))

        return ServiceResult(member)

    def validate_with_pin_password(
        self, request: MemberRequestWithoutSignature
    ) -> ServiceResult:
        member = handle_result(self.member_service.get_by_id(request.memberid))

        if member.pin != request.pin or member.password != request.password:
            return ServiceResult(AppException.InvalidCredentialsError(request.memberid))

        return ServiceResult(member)

    def validate_member_access(
        self, request: MemberRequestWithSignature | MemberRequestWithoutSignature
    ) -> ServiceResult:
        member = handle_result(self.member_service.get_by_id(request.memberid))

        if member.allow_no_sign:
            if isinstance(request, MemberRequestWithoutSignature):
                return self.validate_with_pin_password(request)
            return ServiceResult(
                AppException.InvalidCredentialsError(request.memberid)
            )  # Salah mode
        else:
            if isinstance(request, MemberRequestWithSignature):
                return self.validate_with_signature(request)
            return ServiceResult(
                AppException.InvalidSignatureError("signature required")
            )
