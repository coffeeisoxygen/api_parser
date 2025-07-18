from src.dependencies.dep_mapping import DepValidMapping
from src.dependencies.deps_member import DepValidMember
from src.dependencies.deps_module import DepValidModule
from src.dependencies.deps_product import DepValidProduct
from src.dependencies.deps_signature import DepValidSignature
from src.dependencies.deps_whitelist import DepWhitelist

# --- shortcut alias untuk pemakaian di route (dependencies=[...]) ---
# WhitelistDep = Depends(DepWhitelist)  # Hapus baris ini, karena DepWhitelist bukan callable
# ValidModuleDep = Depends(DepValidModule)  # Hapus juga jika DepValidModule juga Annotated

# --- biar bisa auto-import dari dependencies ---
__all__ = [
    "DepValidMapping",
    "DepValidMember",
    "DepValidModule",
    "DepValidProduct",
    "DepValidSignature",
    "DepWhitelist",
]
