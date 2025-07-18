# from fastapi import Depends, HTTPException, Request

# from src.services.srv_whitelistip import WhitelistIPService
# from src.utils.mylogger import logger


# # Inject service (bisa diubah jadi singleton jika perlu)
# def get_whitelist_service(request: Request) -> WhitelistIPService:
#     """Ambil instance repo dari app.state (yang udah di-load waktu startup)."""
#     member_repo = request.app.state.repos["member"]
#     module_repo = request.app.state.repos["module"]
#     return WhitelistIPService(member_repo, module_repo)


# # Actual validator (langsung dijalankan sebagai dependency)
# def ip_whitelist_guard(
#     request: Request,
#     service: WhitelistIPService = Depends(get_whitelist_service),  # noqa: B008
# ):
#     """Guard to check if the client's IP is whitelisted."""
#     if request.client is None:
#         raise HTTPException(status_code=400, detail="Tidak dapat menentukan IP client")
#     client_ip = request.client.host
#     result = service.get_all_ip()
#     logger.info(f"Memeriksa IP {client_ip} pada whitelist")
#     logger.debug(f"Daftar IP whitelist yang di-fetch: {result.data}")

#     if not result.success:
#         raise HTTPException(status_code=500, detail="Gagal ambil IP whitelist")

#     if not result.data or client_ip not in result.data:
#         raise HTTPException(status_code=403, detail=f"IP '{client_ip}' tidak diizinkan")
