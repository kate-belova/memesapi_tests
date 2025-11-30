import allure
import pytest

from test_data import post_meme_data, invalid_meme_data


@pytest.mark.memes
@pytest.mark.crud
@pytest.mark.regression
class TestCreateMeme:
    @allure.feature('Memes')
    @allure.story('Create meme')
    @allure.title('Successfully create a meme')
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.create
    @pytest.mark.parametrize(
        'meme_data',
        post_meme_data,
        ids=[
            'valid data',
            'minimal valid data',
            'long text and multiple info fields',
        ],
    )
    def test_post_meme_success(self, post_meme_api, meme_data, auth_headers):
        post_meme_api.add_meme(meme_data, auth_headers)
        post_meme_api.assert_response_status(200)
        post_meme_api.assert_meme_data(meme_data)

    @allure.feature('Memes')
    @allure.story('Create meme')
    @allure.title('Try to create a meme without auth token')
    @pytest.mark.negative
    @pytest.mark.create
    def test_post_meme_without_auth(self, post_meme_api):
        post_meme_api.add_meme(post_meme_data[0])
        post_meme_api.assert_response_status(401)
        post_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Create meme')
    @allure.title('Try to create a meme with wrong url')
    @pytest.mark.negative
    @pytest.mark.create
    def test_post_meme_with_wrong_url(self, post_meme_api, auth_headers):
        post_meme_api.add_meme_with_wrong_url(post_meme_data[0], auth_headers)
        post_meme_api.assert_response_status(404)
        post_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Create meme')
    @allure.title('Try to create a meme with invalid data')
    @pytest.mark.negative
    @pytest.mark.create
    @pytest.mark.parametrize(
        'meme_data',
        invalid_meme_data,
        ids=[
            'missing info field',
            'missing url field',
            'missing info and text fields',
            'all fields missing',
        ],
    )
    def test_post_meme_with_invalid_data(
        self, post_meme_api, meme_data, auth_headers
    ):
        post_meme_api.add_meme(meme_data, auth_headers, validate=False)
        post_meme_api.assert_response_status(400)
        post_meme_api.assert_error_message()
