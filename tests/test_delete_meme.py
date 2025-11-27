import allure
import pytest

from test_data import unexisting_meme_id


@pytest.mark.memes
@pytest.mark.crud
@pytest.mark.regression
class TestDeleteMeme:
    @allure.feature('Memes')
    @allure.story('Delete meme')
    @allure.title('Successfully delete meme by its id')
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.delete
    def test_delete_meme_success(
        self, delete_meme_api, get_meme_api, meme_id, auth_headers
    ):
        delete_meme_api.delete_meme(meme_id, auth_headers)
        delete_meme_api.assert_response_status(200)
        delete_meme_api.assert_delete_message()

        get_meme_api.get_meme(meme_id, auth_headers)
        get_meme_api.assert_response_status(404)
        get_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Delete meme')
    @allure.title('Try to delete another user meme')
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.delete
    def test_delete_another_user_meme(
        self,
        delete_meme_api,
        another_user_meme,
        auth_headers,
    ):
        m_id = another_user_meme[0]
        delete_meme_api.delete_meme(m_id, auth_headers)
        delete_meme_api.assert_response_status(403)
        delete_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Delete meme')
    @allure.title('Try to delete meme by its id with wrong url')
    @pytest.mark.negative
    @pytest.mark.delete
    def test_delete_meme_with_wrong_url(
        self, delete_meme_api, meme_id, auth_headers
    ):
        delete_meme_api.delete_meme_with_wrong_url(meme_id, auth_headers)
        delete_meme_api.assert_response_status(404)
        delete_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Delete meme')
    @allure.title('Try to delete meme by its id without auth token')
    @pytest.mark.negative
    @pytest.mark.delete
    def test_delete_meme_without_auth(self, delete_meme_api, meme_id):
        delete_meme_api.delete_meme(meme_id)
        delete_meme_api.assert_response_status(401)
        delete_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Delete meme')
    @allure.title('Try to delete meme with unexisting id')
    @pytest.mark.negative
    @pytest.mark.delete
    def test_delete_meme_with_unexisting_id(
        self, delete_meme_api, auth_headers
    ):
        delete_meme_api.delete_meme(unexisting_meme_id, auth_headers)
        delete_meme_api.assert_response_status(404)
        delete_meme_api.assert_error_message()
