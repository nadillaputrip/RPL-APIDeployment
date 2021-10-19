from fastapi import FastAPI, Body, Depends

from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "asdf",
                "password": "asdf"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "asdf",
                "password": "asdf"
            }
        }