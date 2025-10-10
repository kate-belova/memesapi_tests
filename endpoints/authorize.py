import allure
import pytest
import requests

from endpoints import BaseAPI
from schemas import AuthResponseSchema, AuthRequestSchema


class AuthAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = self.base_url + '/authorize'
        self.name = None
        self.token = None
        self.token_url = None
        self.token_response = None
        self.token_status_code = None
        self.actual_token_msg = None
        self.expected_token_alive_msg = None
        self.expected_text_in_token_invalid_msg = 'Token not found'
        self.expected_text_in_error_message = 'Internal Server Error'

    @allure.step('Send POST request to get authorization token')
    def get_token(self, auth_data=None):
        auth_data_validated = None
        if auth_data:
            auth_data_validated = AuthRequestSchema(**auth_data).model_dump()
            self.name = auth_data_validated['name']
        self.response = requests.post(url=self.url, json=auth_data_validated)
        self.status_code = self.response.status_code
        self.content_type = self.response.headers.get('content-type', '')

        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                if self.json:
                    self.data = AuthResponseSchema(**self.json)
                    self.response_data = self.data.model_dump()
                    self.token = self.response_data['token']
                    self.token_url = self.url + f'/{self.token}'
                    self.expected_token_alive_msg = (
                        f'Token is alive. Username is {self.name}'
                    )
            except requests.exceptions.JSONDecodeError:
                self.json = None
                self.actual_error_message = 'Invalid JSON response'
        else:
            self.json = None
            self.actual_error_message = self.response.text

    @allure.step('Assert user in response has the name sent in request')
    def assert_user(self, auth_data):
        if self.response_data is None:
            pytest.fail('No response data available')

        actual_name = self.response_data['user']
        expected_name = auth_data['name']
        assert (
            actual_name == expected_name
        ), f'Expected user name {expected_name}, but got {actual_name}'

    @allure.step('Assert token got')
    def assert_token(self):
        if self.response_data is None:
            pytest.fail('No response data available')

        token = self.response_data['token']
        assert token is not None, 'Token should not be none'

    @allure.step('Check if token is valid')
    def check_token(self) -> bool:
        is_alive = False
        self.token_response = requests.get(url=self.token_url)
        self.token_status_code = self.token_response.status_code
        self.actual_token_msg = self.token_response.text

        if self.token_status_code == 200:
            is_alive = True
            assert self.actual_token_msg == self.expected_token_alive_msg, (
                f'Expected {self.expected_token_alive_msg}, '
                f'but got {self.actual_token_msg}'
            )
        else:
            assert (
                self.token_status_code == 404
            ), 'Invalid token status code should be 404'
            assert (
                self.expected_text_in_token_invalid_msg
                in self.actual_token_msg
            ), (
                f'Expected {self.expected_text_in_token_invalid_msg} '
                f'in response message, but got {self.actual_token_msg}'
            )

        return is_alive

    @allure.step('Assert token is valid')
    def assert_valid_token(self):
        is_token_alive = self.check_token()
        assert is_token_alive, 'Token should be alive and valid'
