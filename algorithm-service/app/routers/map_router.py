from fastapi import APIRouter, HTTPException

from app.core.map_loader import load_map
from app.schemas.common import success_response


router = APIRouter(prefix="/api/maps", tags=["maps"])


@router.get("/{map_id}")
def get_map(map_id: str):
    try:
        map_index = load_map(map_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return success_response("map loaded successfully", map_index.map_data)

