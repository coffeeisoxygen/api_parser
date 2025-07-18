from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

router = APIRouter(prefix="/digipos", tags=["Digipos"])


class DigiposRequest(BaseModel):
    memberid: str
    product: str
    dest: str
    refid: str
    sign: str | None = None
    pin: str | None = None
    password: str | None = None

    # Param tambahan dari Digipos
    kolom: str = "productId,productName,total_"
    markup: str = "100"
    category: str = "DATA"
    payment_method: str = "LINKAJA"

    model_config = {"str_strip_whitespace": True, "extra": "ignore"}


@router.get("")
@router.get("/", response_class=PlainTextResponse)
def digipos_handler(req: DigiposRequest = Depends()):  # noqa: B008, D103
    if not req.sign and not (req.pin and req.password):
        return "status=91&message=Signature atau PIN/PASSWORD wajib"

    return (
        f"status=50&message=Transaksi diterima dan sedang diproses"
        f"&dest={req.dest}&refid={req.refid}&product={req.product}"
    )


# @router.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors and return a custom plain text response.

    Parameters
    ----------
    request : Request
        The incoming HTTP request.
    exc : RequestValidationError
        The validation error exception.

    Returns:
    -------
    PlainTextResponse
        A response with status code 422 and a message indicating missing fields.
    """
    missing_fields = [err["loc"][-1] for err in exc.errors()]
    message = f"{', '.join(missing_fields)} wajib diisi"
    return PlainTextResponse(
        content=f"status=91&message={message}",
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )
