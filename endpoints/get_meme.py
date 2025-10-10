import allure
import pytest
import requests

from endpoints import BaseAPI
from schemas import MemesResponseSchema, MemeResponseSchema


class GetMemes(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = self.base_url + '/meme'
        self.wrong_url = self.base_url + '/memes'
        self.response = None

    @allure.step('Send GET request to get all memes')
    def get_memes(self, auth_headers=None):
        self.response = requests.get(self.url, headers=auth_headers)
        self.status_code = self.response.status_code
        self.content_type = self.response.headers.get('content-type', '')

        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                if self.json:
                    self.data = MemesResponseSchema(**self.json)
                    self.response_data = self.data.model_dump()
            except requests.exceptions.JSONDecodeError:
                self.json = None
                self.actual_error_message = 'Invalid JSON response'
        else:
            self.json = None
            self.expected_text_in_error_message = (
                self.expected_text_in_unauthorized_error_message
            )
            self.actual_error_message = self.response.text

    @allure.step('Send GET request to get all memes with wrong url')
    def get_memes_with_wrong_url(self, auth_headers=None):
        self.response = requests.get(self.wrong_url, headers=auth_headers)
        self.status_code = self.response.status_code
        self.expected_text_in_error_message = (
            self.expected_text_in_wrong_url_error_message
        )
        self.actual_error_message = self.response.text

    @allure.step('Assert there is at least one meme in the list')
    def assert_has_memes(self, min_count: int = 1):
        if self.response_data is None:
            pytest.fail('No response data available')

        memes_list = self.response_data['data']
        assert len(memes_list) >= min_count, (
            f'Expected at least {min_count} meme(s), '
            f'but got {len(memes_list)}'
        )


class GetMeme(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = None
        self.wrong_url = None
        self.id = None

    @allure.step('Send GET request to get meme by id')
    def get_meme(self, meme_id, auth_headers=None):
        self.url = self.base_url + f'/meme/{meme_id}'
        self.response = requests.get(self.url, headers=auth_headers)
        self.status_code = self.response.status_code
        if self.status_code == 401:
            self.expected_text_in_error_message = (
                self.expected_text_in_unauthorized_error_message
            )
        elif self.status_code == 404:
            self.expected_text_in_error_message = (
                self.expected_text_in_wrong_url_error_message
            )

        self.content_type = self.response.headers.get('content-type', '')

        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                if self.json:
                    self.data = MemeResponseSchema(**self.json)
                    self.response_data = self.data.model_dump()
                    self.id = self.response_data['id']
            except requests.exceptions.JSONDecodeError:
                self.json = None
                self.actual_error_message = 'Invalid JSON response'
        else:
            self.json = None
            self.actual_error_message = self.response.text

    @allure.step('Send GET request to get meme by wrong url')
    def get_meme_with_wrong_url(self, meme_id, auth_headers=None):
        self.wrong_url = self.base_url + f'/memes/{meme_id}'
        self.response = requests.get(self.wrong_url, headers=auth_headers)
        self.status_code = self.response.status_code
        self.expected_text_in_error_message = (
            self.expected_text_in_wrong_url_error_message
        )
        self.actual_error_message = self.response.text

    @allure.step('Assert meme id in response is the one sent in request')
    def assert_meme_id(self, meme_id):
        assert (
            self.id == meme_id
        ), f'Expected meme id is {meme_id}, but actual is {self.id}'
