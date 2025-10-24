import pytest
from app import app as flask_app
from DAL import DataAccessLayer


@pytest.fixture
def app(tmp_path):
    """Create a Flask app configured for testing and use a temporary SQLite DB."""
    # Create a temporary DB path inside pytest's tmp_path
    db_path = tmp_path / "test_projects.db"

    # Initialize a fresh DataAccessLayer that uses the temporary DB
    dal = DataAccessLayer(db_name=str(db_path))

    # Configure the Flask app for testing and swap in the test DAL
    flask_app.config.update({
        "TESTING": True,
    })
    flask_app.dal = dal

    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
