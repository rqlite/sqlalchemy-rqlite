try:
    from sqlalchemy.dialects.sqlite import base, pysqlite, pysqlcipher

    from sqlalchemy.dialects.sqlite.base import (
        BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, REAL,
        NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR, dialect,
    )

    __all__ = ('BLOB', 'BOOLEAN', 'CHAR', 'DATE', 'DATETIME', 'DECIMAL',
               'FLOAT', 'INTEGER', 'NUMERIC', 'SMALLINT', 'TEXT', 'TIME',
               'TIMESTAMP', 'VARCHAR', 'REAL', 'dialect')
except ImportError:
    # This happens when pip calls setup.py before sqlalchemy is installed.
    pass
