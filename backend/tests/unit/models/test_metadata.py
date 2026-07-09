from app.db.base import Base


def test_core_tables_are_registered() -> None:
    table_names = set(Base.metadata.tables.keys())

    assert "users" in table_names
    assert "parking_applications" in table_names
