from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.groups as schema
import api.cruds.groups as cruds


router = APIRouter()


# グループリスト取得
@router.get("/chat/groups", response_model=List[schema.ResponseGroup])
async def get_group_list(
    db: AsyncSession = Depends(get_db),
) -> List[schema.ResponseGroup]:
    group_list = await cruds.get_all_group(db)
    return group_list


# グループ作成
@router.post("/chat/groups", response_model=schema.CreateResponseGroup)
async def create_group(
    group_body: schema.CreateGroup, db: AsyncSession = Depends(get_db)
) -> schema.CreateResponseGroup:
    return await cruds.create_group(db, group_body)


# グループ更新
@router.patch("/chat/group/{group_id}", response_model=schema.ResponseGroup)
async def update_group(
    group_id: int,
    group_body: schema.UpdateGroup,
    db: AsyncSession = Depends(get_db),
) -> schema.ResponseGroup:
    before_data = await cruds.get_group(db, group_id)
    if before_data is None:
        raise HTTPException(status_code=404, detail=f"{group_id} not Found")
    user_info = await cruds.update_group(db, group_body, original=before_data)
    return user_info


# グループ削除
@router.delete("/chat/group/{group_id}", response_model=schema.ResponseGroup)
async def delete_group(
    group_id: int, db: AsyncSession = Depends(get_db)
) -> schema.ResponseGroup:
    before_data = await cruds.get_group(db, group_id)
    if before_data is None:
        raise HTTPException(status_code=404, detail=f"{group_id} not Found")
    user_info = await cruds.delete_group(db, original=before_data)
    return user_info
