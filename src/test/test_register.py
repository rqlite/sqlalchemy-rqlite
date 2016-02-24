
from sqlalchemy import (
    create_engine,
)

from sqlalchemy_rqlite import pyrqlite

from sqlalchemy.dialects import registry

def test_register():
    registry.register("rqlite.pyrqlite", "sqlalchemy_rqlite.pyrqlite", "dialect")
    #engine = create_engine('rqlite+pyrqlite://localhost:4001/?detect_types=0&connect_timeout=3.0')
    #engine.dispose()
