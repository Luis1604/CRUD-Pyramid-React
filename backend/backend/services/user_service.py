from backend.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pyramid_tm import transaction

def create_user(db: Session, name: str, email: str, password_hash: str):
    """Registra un nuevo usuario con contraseña cifrada"""
     # Verificar si el usuario ya existe
    usuario_existente = db.query(User).filter(User.email == email).first()
    if usuario_existente:
        print("Usuario ya existe")
        return {"error": "El email ya está en uso"}
    
    user = User(
        name=name,
        email=email,
        hashed_password=User.set_password(password_hash),
    )
    db.add(user)
    try:
        transaction.manager.commit()
        return True
    except IntegrityError:
        transaction.manager.abort()
        return None
    

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        transaction.commit()
        return user
    return None