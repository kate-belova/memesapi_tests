import allure
import pytest

from schemas import PostMemeRequestSchema
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
            'normal_meme_with_telegram_url',
            'minimal_meme_empty_fields',
            'maximal_meme_long_text_multiple_tags',
        ],
    )
    def test_post_meme_success(self, post_meme_api, meme_data, auth_headers):
        meme_data_validated = PostMemeRequestSchema(**meme_data).model_dump()
        post_meme_api.add_meme(meme_data_validated, auth_headers)

        post_meme_api.assert_response_is_200()
        post_meme_api.assert_meme_data(meme_data_validated)

    @allure.feature('Memes')
    @allure.story('Create meme')
    @allure.title('Try to create a meme without auth token')
    @pytest.mark.negative
    @pytest.mark.create
    def test_post_meme_without_auth(self, post_meme_api):
        meme_data_validated = PostMemeRequestSchema(
            **post_meme_data[0]
        ).model_dump()
        post_meme_api.add_meme(meme_data_validated)
        post_meme_api.assert_response_is_401()
        post_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Create meme')
    @allure.title('Try to create a meme with wrong url')
    @pytest.mark.negative
    @pytest.mark.create
    def test_post_meme_with_wrong_url(self, post_meme_api, auth_headers):
        meme_data_validated = PostMemeRequestSchema(
            **post_meme_data[0]
        ).model_dump()
        post_meme_api.add_meme_with_wrong_url(
            meme_data_validated, auth_headers
        )
        post_meme_api.assert_response_is_404()
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
            'missing_info_field',
            'missing_url_field',
            'missing_info_and_text_fields',
            'all_fields_missing',
        ],
    )
    def test_post_meme_with_invalid_data(
        self, post_meme_api, meme_data, auth_headers
    ):
        post_meme_api.add_meme(meme_data, auth_headers)
        post_meme_api.assert_response_is_400()
        post_meme_api.assert_error_message()
