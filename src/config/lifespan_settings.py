from contextlib import asynccontextmanager

import aiofiles
import yaml
from fastapi import FastAPI

from src.config.base_settings import settings
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
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Validate YAML files, create example if missing."""
    for name, path in {
        "member_yaml_path": settings.member_yaml_path,
        "module_yaml_path": settings.module_yaml_path,
        "product_yaml_path": settings.product_yaml_path,
        "mapping_yaml_path": settings.mapping_yaml_path,
    }.items():
        if not path.exists():
            logger.error(f"[Startup Error] File '{name}' tidak ditemukan: {path}")
            # Create example file
            example = EXAMPLES.get(name)
            if example:
                async with aiofiles.open(path, "w") as f:
                    yaml_str = yaml.safe_dump(
                        example, sort_keys=False, allow_unicode=True
                    )
                    await f.write(yaml_str)
                logger.info(f"Created example YAML for '{name}' at {path}")
            else:
                logger.warning(f"No example available for '{name}'")
    yield
