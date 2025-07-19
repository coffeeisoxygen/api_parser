from collections import OrderedDict
from urllib.parse import quote_plus

from fastapi import Request

from src.schemas.sch_mapping import ProductModuleMapping
from src.schemas.sch_module import Module
from src.schemas.sch_transaction import TrxRequest
from src.utils.mylogger import logger

FORBIDDEN_KEYS = {"sign", "qty", "pin", "pass", "password", "product", "memberid"}

# Urutan final param yang diinginkan (urutan penting)
ORDERED_KEYS = [
    "username",
    "category",
    "to",
    "payment_method",
    "up_harga",
    "duration",
    "kolom",  # <--- encode manual (tanpa %2C)
    "json",
    "refid",
]


def build_final_query(
    request: Request, module: Module, mapping: ProductModuleMapping, trx: TrxRequest
) -> str:
    logger.info("[QueryBuilder] Bangun query final...")

    # STEP 1: Ambil base info
    base_url = module.base_url.rstrip("/")
    endpoint = mapping.command
    module_params = module.parameters or {}
    mapping_params = mapping.query_params or {}
    raw_query = dict(request.query_params)

    logger.debug(f"[QueryBuilder] base_url: {base_url}")
    logger.debug(f"[QueryBuilder] endpoint: {endpoint}")
    logger.debug(f"[QueryBuilder] module_params: {module_params}")
    logger.debug(f"[QueryBuilder] mapping_params: {mapping_params}")
    logger.debug(f"[QueryBuilder] raw_query: {raw_query}")
    logger.debug(f"[QueryBuilder] trx.refid: {trx.refid}")

    # STEP 2: Bersihkan dan rename param dari client
    client_params = {
        ("to" if k == "dest" else k): v
        for k, v in raw_query.items()
        if k.lower() not in FORBIDDEN_KEYS
    }
    logger.debug(f"[QueryBuilder] filtered_client_params: {client_params}")

    # STEP 3: Gabungkan param
    combined = {}
    combined.update(module_params)
    combined.update(mapping_params)
    combined.update(client_params)

    # Inject refid kalau belum ada
    if trx.refid:
        combined.setdefault("refid", trx.refid)

    logger.debug(f"[QueryBuilder] combined query (pre-order): {combined}")

    # STEP 4: Atur urutan parameter (pakai OrderedDict)
    ordered_query = OrderedDict()
    for key in ORDERED_KEYS:
        if key in combined:
            ordered_query[key] = combined.pop(key)

    # Tambahkan sisanya (tidak diatur urutannya)
    ordered_query.update(combined)

    # STEP 5: Encode, raw kolom
    query_parts = []
    for k, v in ordered_query.items():
        if k == "kolom":
            query_parts.append(f"{k}={v}")  # raw
        else:
            query_parts.append(f"{k}={quote_plus(str(v))}")

    query_string = "&".join(query_parts)
    full_url = f"{base_url}/{endpoint}?{query_string}"

    logger.info(f"[QueryBuilder] Final URL: {full_url}")
    return full_url
