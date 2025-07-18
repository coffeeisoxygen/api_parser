from contextlib import asynccontextmanager

import aiofiles
import yaml
from fastapi import FastAPI

from src.config.app_config import settings
from src.repos.rep_mapping import MappingRepoYaml
from src.repos.rep_member import MemberRepoYaml
from src.repos.rep_module import ModuleRepoYaml
from src.repos.rep_product import ProductRepoYaml
from src.services.srv_watchdog import watch_yaml_repo
from src.utils.mylogger import logger

EXAMPLES = {
    "member_yaml_path": {
        "members": [
            {
                "memberid": "M001",
                "password": "pass123",
                "pin": "4321",
                "ip": "192.168.1.10",
                "report_url": "http://192.168.1.10/report",
                "allow_no_sign": True,
                "is_active": True,
            }
        ]
    },
    "module_yaml_path": {
        "modules": [
            {
                "name": "ExampleModule",
                "code": "EXMOD",
                "description": "Example module",
                "base_url": "http://localhost/",
                "timeout": 5,
                "method": "GET",
                "retry": 3,
                "wait_seconds": 60,
                "is_active": True,
                "parameters": {"username": "user", "password": "pass"},
            }
        ]
    },
    "product_yaml_path": {
        "products": [
            {
                "code": "EXPROD",
                "name": "Example Product",
                "provider": "EXAMPLE",
                "is_active": True,
            }
        ]
    },
    "mapping_yaml_path": {
        "product_module_mapping": [
            {
                "product_code": "EXPROD",
                "module_code": "EXMOD",
                "command": "listpaket",
                "query_params": {
                    "category": "EXAMPLE",
                    "payment_method": "EXAMPLE",
                    "json": 1,
                    "kolom": "productId,productName,total_",
                },
                "is_active": True,
            }
        ]
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Step 1: Buat file contoh jika belum ada
    for name, path in {
        "member_yaml_path": settings.member_yaml_path,
        "module_yaml_path": settings.module_yaml_path,
        "product_yaml_path": settings.product_yaml_path,
        "mapping_yaml_path": settings.mapping_yaml_path,
    }.items():
        if not path.exists():
            logger.warning(f"[Startup] File '{name}' tidak ditemukan: {path}")
            example = EXAMPLES.get(name)
            if example:
                async with aiofiles.open(path, "w") as f:
                    yaml_str = yaml.safe_dump(
                        example, sort_keys=False, allow_unicode=True
                    )
                    await f.write(yaml_str)
                logger.info(f"[Startup] File contoh '{name}' dibuat di {path}")
            else:
                logger.warning(f"[Startup] Tidak ada example YAML untuk '{name}'")

    # Step 2: Load repo + aktifkan watcher
    member_repo = await MemberRepoYaml.create(settings.member_yaml_path)
    module_repo = await ModuleRepoYaml.create(settings.module_yaml_path)
    product_repo = await ProductRepoYaml.create(settings.product_yaml_path)
    mapping_repo = await MappingRepoYaml.create(settings.mapping_yaml_path)

    watch_yaml_repo(member_repo)
    watch_yaml_repo(module_repo)
    watch_yaml_repo(product_repo)
    watch_yaml_repo(mapping_repo)

    # Simpan ke app.state (optional, kalau mau dipakai di route)
    app.state.repos = {
        "member": member_repo,
        "module": module_repo,
        "product": product_repo,
        "mapping": mapping_repo,
    }

    logger.info("[Startup] Semua repo siap dan Watchdog aktif ✅")

    yield
