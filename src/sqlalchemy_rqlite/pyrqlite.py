from __future__ import absolute_import

from sqlalchemy.dialects.sqlite.base import SQLiteDialect, DATETIME, DATE
from sqlalchemy import exc, pool
from sqlalchemy import types as sqltypes
from sqlalchemy import util

import os


class _SQLite_rqliteTimeStamp(DATETIME):
    def bind_processor(self, dialect):
        if dialect.native_datetime:
            return None
        else:
            return DATETIME.bind_processor(self, dialect)

    def result_processor(self, dialect, coltype):
        if dialect.native_datetime:
            return None
        else:
            return DATETIME.result_processor(self, dialect, coltype)


class _SQLite_rqliteDate(DATE):
    def bind_processor(self, dialect):
        if dialect.native_datetime:
            return None
        else:
            return DATE.bind_processor(self, dialect)

    def result_processor(self, dialect, coltype):
        if dialect.native_datetime:
            return None
        else:
            return DATE.result_processor(self, dialect, coltype)


class SQLiteDialect_rqlite(SQLiteDialect):
    default_paramstyle = 'qmark'
    supports_statement_cache = True

    colspecs = util.update_copy(
        SQLiteDialect.colspecs,
        {
            sqltypes.Date: _SQLite_rqliteDate,
            sqltypes.TIMESTAMP: _SQLite_rqliteTimeStamp,
        }
    )

    if not getattr(util, "py2k", False):
        description_encoding = None

    driver = 'pyrqlite'

    # pylint: disable=method-hidden
    @classmethod
    def import_dbapi(cls):
        try:
            # pylint: disable=no-name-in-module
            from pyrqlite import dbapi2 as sqlite
            #from sqlite3 import dbapi2 as sqlite  # try 2.5+ stdlib name.
        except ImportError:
            #raise e
            raise
        return sqlite

    # SQLAlchemy 1.x compatibility.
    dbapi = import_dbapi

    @classmethod
    def get_pool_class(cls, url):
        if url.database and url.database != ':memory:':
            return pool.NullPool
        else:
            return pool.SingletonThreadPool

    def create_connect_args(self, url):
        opts = dict(url.query.items())
        util.coerce_kw_type(opts, 'connect_timeout', float)
        util.coerce_kw_type(opts, 'detect_types', int)
        util.coerce_kw_type(opts, 'max_redirects', int)
        opts['port'] = url.port
        opts['host'] = url.host
        
        if url.username:
            opts['user'] = url.username

        if url.password:
            opts['password'] = url.password

        return ([], opts)

    def is_disconnect(self, e, connection, cursor):
        return False
    
    def do_ping(self, dbapi_connection):
        try:
            dbapi_connection.ping(reconnect=True)
        except self.dbapi.Error as err:
            if self.is_disconnect(err, dbapi_connection, None):
                return False
            else:
                raise
        else:
            return True

dialect = SQLiteDialect_rqlite
