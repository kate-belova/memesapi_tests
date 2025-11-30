import allure
import requests

from endpoints import BaseAPI
from schemas import MemeResponseSchema, PutMemeRequestSchema


class PutMeme(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = None
        self.id = None

    @allure.step('Send PUT request to fully update meme by id')
    def update_meme(self, meme_id, meme_data, auth_data=None, validate=True):
        payload = meme_data
        if validate:
            payload = PutMemeRequestSchema(**meme_data).model_dump()

        self.url = self.base_url + f'/meme/{meme_id}'
        self.response = requests.put(
            url=self.url, headers=auth_data, json=payload
        )
        self.status_code = self.response.status_code
        if self.status_code == 400:
            self.expected_text_in_error_message = (
                self.expected_text_in_bad_request_error_message
            )
        elif self.status_code == 401:
            self.expected_text_in_error_message = (
                self.expected_text_in_unauthorized_error_message
            )
        elif self.status_code == 403:
            self.expected_text_in_error_message = (
                self.expected_text_in_forbidden_error_message
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

    @allure.step('Send PUT request to fully update meme by id with wrong url')
    def update_meme_with_wrong_url(self, meme_id, meme_data, auth_data=None):
        self.url = self.base_url + f'/memes/{meme_id}'
        self.response = requests.put(
            url=self.url, headers=auth_data, json=meme_data
        )
        self.status_code = self.response.status_code
        self.expected_text_in_error_message = (
            self.expected_text_in_wrong_url_error_message
        )
        self.actual_error_message = self.response.text
