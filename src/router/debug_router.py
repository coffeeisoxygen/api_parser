from fastapi import APIRouter, Request

router = APIRouter(prefix="/v1/debug", tags=["debug"])


@router.get("/repo-status")
async def get_repo_status(request: Request):
    repos = request.app.state.repos  # dict: member, module, product, mapping

    result = {}
    for name, repo in repos.items():
        result[name] = {
            "file": str(repo.file_path),
            "total_loaded": len(repo),
            "invalid_count": repo.invalid_count,
            "last_reload": (
                repo.last_loaded_at.isoformat() if repo.last_loaded_at else None
            ),
        }

    return {"status": "ok", "repos": result}
