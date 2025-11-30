import allure
import pytest

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
        put_meme_api.update_meme(m_id, update_meme_data, auth_headers)

        put_meme_api.assert_response_status(200)
        put_meme_api.assert_meme_data(
            update_meme_data, ignore_missing_fields=True
        )

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
        put_meme_api.update_meme(m_id, update_meme_data, auth_headers)

        put_meme_api.assert_response_status(403)
        put_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Fully update meme')
    @allure.title('Try to fully update (replace) meme without auth token')
    @pytest.mark.negative
    @pytest.mark.fully_update
    def test_put_meme_without_auth(self, posted_meme, put_meme_api):
        m_id = posted_meme[0]
        update_meme_data['id'] = m_id
        put_meme_api.update_meme(m_id, update_meme_data)

        put_meme_api.assert_response_status(401)
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
        put_meme_api.update_meme_with_wrong_url(
            m_id, update_meme_data, auth_headers
        )

        put_meme_api.assert_response_status(404)
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
            'missing url field',
            'missing all fields',
            'missing text and info fields',
            'missing info fields',
        ],
    )
    def test_put_meme_with_invalid_data(
        self, posted_meme, put_meme_api, meme_data, auth_headers
    ):
        m_id = posted_meme[0]
        update_meme_data['id'] = m_id
        put_meme_api.update_meme(m_id, meme_data, auth_headers, validate=False)

        put_meme_api.assert_response_status(400)
        put_meme_api.assert_error_message()
