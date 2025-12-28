from typing import Optional, Dict

def get_pagination(
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    min_discount: Optional[float] = None,
    max_discount: Optional[float] = None,
    sort_by: str = "id",
    sort_dir: str = "desc",
) -> Dict:
    return {
        "skip": skip,
        "limit": limit,
        "q": q,
        "min_discount": min_discount,
        "max_discount": max_discount,
        "sort_by": sort_by,
        "sort_dir": sort_dir,
    }
