import base64
import hashlib
from typing import Annotated

from fastapi import Depends, Request

from src.dependencies.deps_member import DepValidMember
from src.exceptions.oto_exceptions import OtoException
from src.utils.mylogger import logger


def _generate_signature(
    memberid: str, product: str, dest: str, refid: str, pin: str, password: str
) -> str:
    raw = f"OtomaX|{memberid}|{product}|{dest}|{refid}|{pin}|{password}"
    sha1_digest = hashlib.sha1(raw.encode()).digest()
    signature = base64.b64encode(sha1_digest).decode().rstrip("=")
    signature = signature.replace("+", "-").replace("/", "_")
    logger.info(f"Generated signature: {signature} (raw: {raw})")
    return signature


def _validate_signature(
    request: Request,
    member: DepValidMember,  # Inject valid member dari IP dan active
) -> bool:
    logger.info("Start signature validation process")
    query = request.query_params

    required = ["product", "dest", "refid", "sign"]
    missing = [k for k in required if k not in query]
    if missing:
        logger.info(f"Missing parameters: {missing}")
        raise OtoException.InvalidTrxCombinationError(
            f"Parameter tidak lengkap: {', '.join(missing)}"
        )

    product = query["product"].strip()
    dest = query["dest"].strip()
    refid = query["refid"].strip()
    sign = query["sign"].strip()

    logger.info(f"member.pin: {member.pin}, member.password: {member.password}")
    logger.info(f"Received signature: {sign}")
    logger.info(
        f"Params sebelum generate signature: memberid={member.memberid.upper()}, product={product}, dest={dest}, refid={refid}, pin={member.pin}, password={member.password}"
    )
    expected = _generate_signature(
        member.memberid.upper(), product, dest, refid, member.pin, member.password
    )

    logger.info(
        f"Comparing generated signature vs received signature: {expected} vs {sign}"
    )

    if sign != expected:
        logger.info("Signature tidak valid")
        raise OtoException.InvalidTrxCombinationError("Signature tidak valid")

    logger.info("Signature valid, proses selesai")
    return True


DepValidSignature = Annotated[bool, Depends(_validate_signature)]

# NOTE: kalau ada yang aneh atau miss , ini pasti gara gara uppercase dan lowercase pada parameter tertentu, jadi make sure jeli dan standarisasi penulisan parameter
