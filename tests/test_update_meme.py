import allure
import pytest

from schemas import PutMemeRequestSchema
from test_data import update_meme_data, invalid_meme_data_to_update


@pytest.mark.memes
@pytest.mark.crud
@pytest.mark.regression
class TestUpdateMeme:
    @allure.feature('Memes')
    @allure.story('Fully update meme')
    @allure.title('Successfully update (replace) meme')
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.fully_update
    def test_put_meme_success(self, put_meme_api, posted_meme, auth_headers):
        m_id = posted_meme[0]
        update_meme_data['id'] = m_id
        meme_data_validated = PutMemeRequestSchema(
            **update_meme_data
        ).model_dump()
        put_meme_api.update_meme(m_id, meme_data_validated, auth_headers)

        put_meme_api.assert_response_is_200()
        put_meme_api.assert_meme_data(meme_data_validated)

    @allure.feature('Memes')
    @allure.story('Fully update meme')
    @allure.title('Try to fully update another user meme')
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.fully_update
    def test_put_another_user_meme(
        self,
        put_meme_api,
        another_user_meme,
        auth_headers,
    ):
        m_id = another_user_meme[0]
        update_meme_data['id'] = m_id
        meme_data_validated = PutMemeRequestSchema(
            **update_meme_data
        ).model_dump()
        put_meme_api.update_meme(m_id, meme_data_validated, auth_headers)

        put_meme_api.assert_response_is_403()
        put_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Fully update meme')
    @allure.title('Try to fully update (replace) meme without auth token')
    @pytest.mark.negative
    @pytest.mark.fully_update
    def test_put_meme_without_auth(self, posted_meme, put_meme_api):
        m_id = posted_meme[0]
        update_meme_data['id'] = m_id
        meme_data_validated = PutMemeRequestSchema(
            **update_meme_data
        ).model_dump()
        put_meme_api.update_meme(m_id, meme_data_validated)

        put_meme_api.assert_response_is_401()
        put_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Fully update meme')
    @allure.title('Try to fully update (replace) meme with wrong url')
    @pytest.mark.negative
    @pytest.mark.fully_update
    def test_put_meme_with_wrong_url(
        self, posted_meme, put_meme_api, auth_headers
    ):
        m_id = posted_meme[0]
        update_meme_data['id'] = m_id
        meme_data_validated = PutMemeRequestSchema(
            **update_meme_data
        ).model_dump()
        put_meme_api.update_meme_with_wrong_url(
            m_id, meme_data_validated, auth_headers
        )

        put_meme_api.assert_response_is_404()
        put_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Fully update meme')
    @allure.title('Try to fully update (replace) meme with invalid data')
    @pytest.mark.negative
    @pytest.mark.fully_update
    @pytest.mark.parametrize(
        'meme_data',
        invalid_meme_data_to_update,
        ids=[
            'missing_url_field',
            'missing_all_fields',
            'missing_text_and_info_fields',
            'missing_info_fields',
        ],
    )
    def test_put_meme_with_invalid_data(
        self, posted_meme, put_meme_api, meme_data, auth_headers
    ):
        m_id = posted_meme[0]
        update_meme_data['id'] = m_id
        put_meme_api.update_meme(m_id, meme_data, auth_headers)

        put_meme_api.assert_response_is_400()
        put_meme_api.assert_error_message()
