from fastapi import APIRouter
router = APIRouter(prefix="/fallback", tags=["fallback"])

@router.post("/search")
def fake_enterprise_search(query: dict):
    q = query.get("q", "")
    # Return a naive canned response
    return {"results": [{"title": "Enterprise KB Hit", "snippet": f"No local match. Generic help for '{q}'."}]}
