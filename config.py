from dataclasses import dataclass

@dataclass
class Config:
    SECRET_KEY: str = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN: bool = True
    ADMIN: str = 'admin'
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres:postgres@0.0.0.0:5432/flask'
    
    @staticmethod
    def init_app(app):
        pass