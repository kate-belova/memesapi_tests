import allure
import pytest

from test_data import unexisting_meme_id, string_id


@pytest.mark.memes
@pytest.mark.crud
@pytest.mark.regression
class TestReadMemes:
    @allure.feature('Memes')
    @allure.story('Read memes')
    @allure.title('Successfully read all memes')
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.read
    def test_get_all_memes_success(self, get_memes_api, auth_headers):
        get_memes_api.get_memes(auth_headers)
        get_memes_api.assert_response_is_200()
        get_memes_api.assert_has_memes()

    @allure.feature('Memes')
    @allure.story('Read memes')
    @allure.title('Try to read all memes with wrong url')
    @pytest.mark.negative
    @pytest.mark.read
    def test_get_all_memes_with_wrong_url(self, get_memes_api, auth_headers):
        get_memes_api.get_memes_with_wrong_url(auth_headers)
        get_memes_api.assert_response_is_404()
        get_memes_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Read memes')
    @allure.title('Try to read all memes without auth token')
    @pytest.mark.negative
    @pytest.mark.read
    def test_get_all_memes_without_auth(self, get_memes_api):
        get_memes_api.get_memes()
        get_memes_api.assert_response_is_401()
        get_memes_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Read meme')
    @allure.title('Successfully read meme by its id')
    @pytest.mark.positive
    @pytest.mark.smoke
    @pytest.mark.read
    def test_get_meme_by_id_success(
        self, posted_meme, get_meme_api, auth_headers
    ):
        m_id, meme_data = posted_meme
        get_meme_api.get_meme(m_id, auth_headers)

        get_meme_api.assert_response_is_200()
        get_meme_api.assert_meme_id(m_id)
        get_meme_api.assert_meme_data(meme_data)

    @allure.feature('Memes')
    @allure.story('Read meme')
    @allure.title('Try to read meme by unexisting id')
    @pytest.mark.negative
    @pytest.mark.read
    def test_get_meme_with_unexisting_id(self, get_meme_api, auth_headers):
        get_meme_api.get_meme(unexisting_meme_id, auth_headers)
        get_meme_api.assert_response_is_404()
        get_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Read meme')
    @allure.title('Try to read meme by id with wrong url')
    @pytest.mark.negative
    @pytest.mark.read
    def test_get_meme_by_wrong_url(
        self, posted_meme, get_meme_api, auth_headers
    ):
        m_id = posted_meme[0]
        get_meme_api.get_meme_with_wrong_url(m_id, auth_headers)
        get_meme_api.assert_response_is_404()
        get_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Get meme')
    @allure.title('Try to read meme by id without auth token')
    @pytest.mark.negative
    @pytest.mark.read
    def test_get_meme_without_auth(self, posted_meme, get_meme_api):
        m_id = posted_meme[0]
        get_meme_api.get_meme(m_id)
        get_meme_api.assert_response_is_401()
        get_meme_api.assert_error_message()

    @allure.feature('Memes')
    @allure.story('Get meme')
    @allure.title('Try to read meme by string id')
    @pytest.mark.negative
    @pytest.mark.read
    def test_get_meme_with_string_id(self, get_meme_api, auth_headers):
        get_meme_api.get_meme(string_id, auth_headers)
        get_meme_api.assert_response_is_404()
        get_meme_api.assert_error_message()
