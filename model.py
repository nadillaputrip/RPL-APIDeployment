from fastapi import FastAPI, Body, Depends

from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field("asdf")
    password: str = Field("asdf")

    class Config:
        schema_extra = {
            "user": {
                "username": "asdf",
                "password": "asdf"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field("asdf")
    password: str = Field("asdf")

    class Config:
        schema_extra = {
            "user": {
                "username": "asdf",
                "password": "asdf"
            }
        }