import base64
import hashlib
from typing import Annotated

from fastapi import Depends, Request

from src.dependencies.deps_member import DepValidMember
from src.exceptions.oto_exceptions import OtoException


def _generate_signature(
    memberid: str, product: str, dest: str, refid: str, pin: str, password: str
) -> str:
    raw = f"OtomaX|{memberid}|{product}|{dest}|{refid}|{pin}|{password}"
    sha1_digest = hashlib.sha1(raw.encode()).digest()
    b64 = base64.b64encode(sha1_digest).decode()
    return b64.rstrip("=").replace("+", "-").replace("/", "_")


def _validate_signature(
    request: Request,
    member: DepValidMember,  # Inject valid member dari IP dan active
) -> bool:
    query = request.query_params

    required = ["product", "dest", "refid", "sign"]
    missing = [k for k in required if k not in query]
    if missing:
        raise OtoException.InvalidTrxCombinationError(
            f"Parameter tidak lengkap: {', '.join(missing)}"
        )

    product = query["product"]
    dest = query["dest"]
    refid = query["refid"]
    sign = query["sign"]

    expected = _generate_signature(
        member.memberid, product, dest, refid, member.pin, member.password
    )

    if sign != expected:
        raise OtoException.InvalidTrxCombinationError("Signature tidak valid")

    return True


DepValidSignature = Annotated[bool, Depends(_validate_signature)]
