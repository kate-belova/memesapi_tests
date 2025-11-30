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


@pytest.fixture
def auth_api():
    return AuthAPI()


@pytest.fixture()
def auth_token(auth_api):
    auth_data = valid_auth_data[0]
    auth_api.get_token(auth_data)

    if auth_api.status_code == 200 and auth_api.token:
        is_alive = auth_api.check_token()
        if is_alive:
            return auth_api.token

    pytest.fail('Failed to get valid auth token')
    return None


@pytest.fixture()
def another_user_auth_token(auth_api):
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
def post_meme_api(request):
    api = PostMeme()
    created_meme_ids = []

    original_add_meme = api.add_meme

    def add_meme_with_tracking(meme_data, auth_data=None):
        result = original_add_meme(meme_data, auth_data)
        if api.id and api.id not in created_meme_ids:
            created_meme_ids.append((api.id, auth_data))
        return result

    api.add_meme = add_meme_with_tracking

    def cleanup():
        if created_meme_ids:
            delete_api = DeleteMeme()
            for meme_id, auth_data in created_meme_ids:
                if auth_data:
                    delete_api.delete_meme(meme_id, auth_data)

    request.addfinalizer(cleanup)
    return api


@pytest.fixture
def put_meme_api():
    return PutMeme()


@pytest.fixture
def delete_meme_api():
    return DeleteMeme()


@pytest.fixture
def posted_meme(post_meme_api, auth_headers):
    meme_data = PostMemeRequestSchema(**post_meme_data[0]).model_dump()
    post_meme_api.add_meme(meme_data, auth_headers)
    m_id = post_meme_api.id

    yield m_id, meme_data


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
