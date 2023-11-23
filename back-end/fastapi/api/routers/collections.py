from fastapi import APIRouter

router = APIRouter()


# コレクション作成
@router.post("/chat/collections")
async def create_collection() -> dict:
    return {}


# コレクション一覧取得
@router.get("/chat/collections")
async def add_user() -> dict:
    return {}


# ドキュメント登録
@router.get("/chat/collections/{collection_id}")
async def add_documents() -> dict:
    return {}


# コレクション削除
@router.delete("/chat/collections/{collection_id}")
async def delate_collections() -> dict:
    return {}


# ドキュメント削除
@router.delete("/chat/collections/{collection_id}/{documents_id}")
async def delate_documents() -> dict:
    return {}
