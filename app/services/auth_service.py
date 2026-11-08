from app.db.session import AsyncSession
import app.core.security as cs
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.users import Users
from app.db.models.logins import Logins
from app.core.config import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone 
from fastapi import HTTPException
from app.schemas.auth import TokenData
from sqlalchemy import select



class AuthenticationService:

    def __init__(self):
        self.oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

    async def verify_login(self, credentials: OAuth2PasswordRequestForm, db: AsyncSession) -> TokenData:
        dummy_hash = cs.password_hash.hash('dummypassword')
        result = await db.execute(
            select(Users).where(Users.username == credentials.username)
        )
        user = result.scalar_one_or_none()
        if user:
            valid_password = cs.verify_password(credentials.password, user.passwd_hash)
        else:
            valid_password = cs.verify_password(credentials.password, dummy_hash)
        if not user or not valid_password:
            raise HTTPException(status_code=401, detail='Invaild username or password')
        if not user.is_active:
            raise HTTPException(status_code=403, detail='Account is inactive.')
        new_login = Logins(user_id=user.user_id)
        db.add(new_login)
        await db.flush()
        return TokenData(
            user_id=user.user_id,
            username=user.username,
            login_id=new_login.login_id,
        )
        

    def create_access_token(self, token_data: TokenData) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            'user_id' : token_data.user_id,
            'username' : token_data.username,
            'login_id' : token_data.login_id,
            'iss' : 'https://exampledomain.com', # make these constants JWT_ISSUER (os.getenv('...'))
            'aud' : 'https://exampledomain.com',
            'iat': now,
            'exp' : now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        try:
            token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM) 
            return token
        except:
            pass
        


    def decode_token(self, token:str) -> TokenData:
        try:
            decoded = jwt.decode(token, JWT_SECRET,algorithms=[ALGORITHM], issuer='https://exampledomain.com', audience='https://exampledomain.com')
            return TokenData(
                user_id=decoded['user_id'],
                username=decoded['username'],
                login_id=decoded['login_id']
                )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired.')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token.')


    def create_refresh_token(self, token_data:TokenData) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            'user_id' : token_data.user_id,
            'username' : token_data.username,
            'login_id' : token_data.login_id,
            'iss' : 'https://exampledomain.com',
            'aud' : 'https://exampledomain.com',
            'iat' : now,
            'exp' : now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        }
        try:
            token = self.create_access_token(token_data=token_data)
            return token
        except:
            raise ' '


auth_service = AuthenticationService()

# Token endpoint, email and password for access token
# for production grade this needs to be RS256 (RSA-SHA256 hashalgorithm or ES256(ECDSA-SHA256) smaller keys than RSA, FASTER VERIFICATION)
# EdDSA NEW, Ed25519 (Edwards-Curve Digital Signature Algorithm) smaller keys than rsa, very secure and very fast

# OAuth2, key access token short (minutes) and add refresh token or session cookie for duration
