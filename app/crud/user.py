from sqlalchemy.orm import Session
from app.models.content import User
from app.schemas.content import UserCreate
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt
from app.core.config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ALGORITHM = 'HS256'

# ACCESS_TOKEN_EXPIRE_MINUTES:int = 1



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  
    
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class UserCRUD:
    def create_user(self, db: Session, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, password=hashed_password, role=user.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def authenticate_user(self, db: Session, email: str, password: str) -> User | None:
        user = self.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password):
            return None
        # If authentication is successful, create an access token
        access_token = create_access_token(data={"sub": user.email})
        return {"user": user, "access_token": access_token}

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True


    
user_crud = UserCRUD() 