"""Fungsi untuk membuat dan memverifikasi signature OtomaX.

Built with ❤️ by Hasan Maki and ChatGPT
"""

import base64
import hashlib

from fastapi import Depends

from src.exceptions.app_exceptions import AppException
from src.schemas.sch_member import MemberRequestWithSignature
from src.services.srv_member import MemberService
from src.services.srv_result import handle_result


def generate_signature(
    memberid: str, product: str, dest: str, refid: str, pin: str, password: str
) -> str:
    """Generate SHA1 signature untuk OtomaX request."""
    raw = f"OtomaX|{memberid}|{product}|{dest}|{refid}|{pin}|{password}"
    sha1_digest = hashlib.sha1(raw.encode()).digest()
    b64_encoded = base64.b64encode(sha1_digest).decode()
    return b64_encoded.replace("+", "-").replace("/", "_").rstrip("=")


def verify_signature(
    request: MemberRequestWithSignature,
    member_service: MemberService = Depends(),  # noqa: B008
) -> bool:
    """Validasi signature OtomaX terhadap member berdasarkan pin/password."""
    member = handle_result(member_service.get_by_id(request.memberid))

    # Ensure member is valid before accessing attributes
    if member is None or not hasattr(member, "pin") or not hasattr(member, "password"):
        raise AppException.MemberNotFoundError(request.memberid)

    expected = generate_signature(
        memberid=request.memberid,
        product=request.product,
        dest=request.dest,
        refid=request.refid,
        pin=member.pin,
        password=member.password,
    )

    if request.signature != expected:
        raise AppException.InvalidSignatureError(request.signature)

    return True
