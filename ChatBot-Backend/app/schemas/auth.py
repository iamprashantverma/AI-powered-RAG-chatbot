from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Registered user email",
        examples=["prashant@example.com"]
    )
    password: str = Field(
        ...,
        description="User password",
        examples=["Test@1234"]
    )


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None
