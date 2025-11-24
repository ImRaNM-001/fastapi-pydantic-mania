from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends
from typing import Dict

app: FastAPI = FastAPI()

# create UserSignup model
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    passwd: str


# create UserSettings model
class Settings(BaseModel):
    app_name: str = 'T0z0 app'
    admin_email: str = 'admin@t0z0fry.com'


def get_settings() -> Settings:
    return Settings()


# create routes
@app.post('/signup')
def signup(user: UserSignup) -> Dict[str, str]:
    return {
        'message': f'User {user.username} signed up successfully'
    }


@app.get('/settings')
def get_settings_endpoint(usrSettings: Settings = Depends(get_settings)) -> Settings:
    return usrSettings


user_dict: Dict[str, str] = {
    'username' : 'kabir',
    'email' : 'kbr@smartCx.com',
    'passwd' : 'jfg5677'
}

# create users
kabir_user: UserSignup = UserSignup(**user_dict)






