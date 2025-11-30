import allure
import pytest

from endpoints import AuthAPI
from test_data import valid_auth_data


@pytest.mark.auth
@pytest.mark.regression
class TestAuth:
    @allure.feature('Memes')
    @allure.story('Authorization')
    @allure.title('Successful authorization')
    @pytest.mark.parametrize(
        'auth_data',
        valid_auth_data,
        ids=[
            'valid_name_kate',
            'empty_name',
            'name_with_spaces',
            'name_with_numbers',
            'long_name',
        ],
    )
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_successful_authorization(self, auth_data):
        auth_api = AuthAPI()
        auth_api.get_token(auth_data)

        auth_api.assert_response_status(200)
        auth_api.assert_user(auth_data)
        auth_api.assert_token()
        auth_api.assert_valid_token()

    @allure.feature('Memes')
    @allure.story('Authorization')
    @allure.title('Unsuccessful authorization without necessary auth data')
    @pytest.mark.negative
    def test_authorization_without_necessary_fields(self):
        auth_api = AuthAPI()
        auth_api.get_token()

        auth_api.assert_response_status(500)
        auth_api.assert_error_message()
