# src/services/srv_query_builder.py

from urllib.parse import urlencode

from fastapi import Request

from src.schemas.sch_mapping import ProductModuleMapping
from src.schemas.sch_module import Module
from src.schemas.sch_transaction import TrxRequest
from src.utils.mylogger import logger


def build_final_query(
    request: Request, module: Module, mapping: ProductModuleMapping, trx: TrxRequest
) -> str:
    logger.info("[QueryBuilder] Bangun query final...")

    # Ambil parameter default dari module (bisa None)
    module_params = module.parameters or {}
    logger.debug(f"[QueryBuilder] Parameter dari module: {module_params}")

    # Ambil parameter dari mapping
    mapping_params = mapping.query_params or {}
    logger.debug(f"[QueryBuilder] Parameter dari mapping: {mapping_params}")

    # Ambil parameter dari client (request query)
    client_params = dict(request.query_params)
    logger.debug(f"[QueryBuilder] Parameter dari client: {client_params}")

    # Gabungkan semuanya (urutan: module < mapping < client)
    final_query = {**module_params, **mapping_params, **client_params}
    logger.info(f"[QueryBuilder] Final query: {final_query}")

    # Encode ke query string (misal buat GET forwarding)
    encoded_query = urlencode(final_query, doseq=True)
    logger.info(f"[QueryBuilder] Final encoded query: {encoded_query}")

    return encoded_query
