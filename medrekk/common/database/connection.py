from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .db_const import DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT

conn_url = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(conn_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def create_db_and_tables():
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as e:
        print("Error creating tables. \n", e)


def get_db():
    try:
        db = SessionLocal()
        # Base.metadata.drop_all(engine)
        # Base.metadata.create_all(engine)

        yield db
    except HTTPException as http_error:
        # All exceptions caught in the controller or router are raised as HTTPException, 
        # therefore it will be thrown as is.
        raise http_error
    except (DBAPIError, Exception):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )
    finally:
        db.close()


def get_session():
    try:
        db = SessionLocal()
        # Base.metadata.drop_all(engine)
        # Base.metadata.create_all(engine)

        yield db
    except HTTPException as http_error:
        # All exceptions caught in the controller or router are raised as HTTPException, 
        # therefore it will be thrown as is.
        raise http_error
    except (DBAPIError, Exception):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )
    finally:
        db.close()
