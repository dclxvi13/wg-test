import pytest

from storage import storage
from websiteinfo import get_website_data


# Реализация хранения данных в фиксутре
@pytest.fixture(scope="session")
def website_data():
    return get_website_data()


# Реализация хранения данных в отдельном хранилище
@pytest.fixture
def website_data_separate():
    return storage.website_data
