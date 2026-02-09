from contextlib import contextmanager
import psycopg
from src.config import DbConfig

@contextmanager
def get_conn():
    cfg = DbConfig()
    with psycopg.connect(cfg.dsn) as conn:
        yield conn
