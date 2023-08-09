import json
import uuid
import secrets
from datetime import datetime       
from fastapi import APIRouter, Body
from fastapi import HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_sqlalchemy import db
from pydantic import BaseModel
from superagi.helper.auth import get_user_organisation
from superagi.helper.auth import check_auth
from superagi.models.api_key import ApiKey
from typing import Optional, Annotated
router = APIRouter()

class ApiKeyIn(BaseModel):
    id:int
    name: str
    class Config:
        orm_mode = True

@router.post("/")
def create_api_key(name: Annotated[str,Body(embed=True)], Authorize: AuthJWT = Depends(check_auth), organisation=Depends(get_user_organisation)):
    api_key=str(uuid.uuid4())
    obj=ApiKey(key=api_key,name=name,org_id=organisation.id)
    db.session.add(obj)
    db.session.commit()
    db.session.flush()
    return api_key

@router.get("/")
def get_all(Authorize: AuthJWT = Depends(check_auth), organisation=Depends(get_user_organisation)):
    api_keys=ApiKey.get_all_by_org_id(db.session, organisation.id)
    return api_keys

@router.delete("/")
def delete_api_key(id: Annotated[int,Body(embed=True)], Authorize: AuthJWT = Depends(check_auth), organisation=Depends(get_user_organisation)):
    api_key=ApiKey.get_by_id(db.session,id)
    if api_key is None:
        return "API key not found"
    ApiKey.delete_by_id(db.session,id)
    return {"API key successfully deleted"}

@router.put("/")
def edit_api_key(api_key_in:ApiKeyIn,Authorize: AuthJWT = Depends(check_auth), organisation=Depends(get_user_organisation)):
    api_key=ApiKey.get_by_id(db.session,api_key_in.id)
    if api_key is None:
        return "API key not found"
    ApiKey.edit_by_id(db.session,api_key_in.id,api_key_in.name)
    return {"API key successfully edited"}

