from pathlib import Path

import pytest

from endpoints import AuthAPI, GetMemes, GetMeme, PostMeme, DeleteMeme, PutMeme
from schemas import PostMemeRequestSchema
from test_data import valid_auth_data, post_meme_data, another_user_auth_data


def pytest_configure(config):
    project_root = Path(__file__).resolve().parent
    allure_dir = project_root / 'allure-results'
    allure_dir.mkdir(exist_ok=True)
    config.option.allure_report_dir = str(allure_dir)


@pytest.fixture()
def auth_token():
    auth_api = AuthAPI()
    auth_data = valid_auth_data[0]
    auth_api.get_token(auth_data)

    if auth_api.status_code == 200 and auth_api.token:
        is_alive = auth_api.check_token()
        if is_alive:
            return auth_api.token

    pytest.fail('Failed to get valid auth token')
    return None


@pytest.fixture()
def another_user_auth_token():
    auth_api = AuthAPI()
    auth_api.get_token(another_user_auth_data)

    if auth_api.status_code == 200 and auth_api.token:
        is_alive = auth_api.check_token()
        if is_alive:
            return auth_api.token

    pytest.fail('Failed to get valid auth token for another user')
    return None


@pytest.fixture()
def auth_headers(auth_token):
    return {'Authorization': auth_token}


@pytest.fixture()
def another_user_auth_headers(another_user_auth_token):
    return {'Authorization': another_user_auth_token}


@pytest.fixture
def get_memes_api():
    return GetMemes()


@pytest.fixture
def get_meme_api():
    return GetMeme()


@pytest.fixture
def post_meme_api():
    return PostMeme()


@pytest.fixture
def put_meme_api():
    return PutMeme()


@pytest.fixture
def delete_meme_api():
    return DeleteMeme()


@pytest.fixture
def posted_meme(post_meme_api, delete_meme_api, auth_headers):
    meme_data = PostMemeRequestSchema(**post_meme_data[0]).model_dump()
    post_meme_api.add_meme(meme_data, auth_headers)
    m_id = post_meme_api.id

    yield m_id, meme_data

    delete_meme_api.delete_meme(m_id, auth_headers)


@pytest.fixture
def another_user_meme(
    post_meme_api, delete_meme_api, another_user_auth_headers
):
    meme_data = PostMemeRequestSchema(**post_meme_data[0]).model_dump()
    post_meme_api.add_meme(meme_data, another_user_auth_headers)
    m_id = post_meme_api.id

    yield m_id, meme_data

    delete_meme_api.delete_meme(m_id, another_user_auth_headers)


@pytest.fixture
def meme_id(posted_meme):
    return posted_meme[0]
