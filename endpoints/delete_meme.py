import allure
import requests

from endpoints import BaseAPI


class DeleteMeme(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = None
        self.expected_success_message = None
        self.actual_success_message = None

    @allure.step('Send DELETE request to delete object by its id')
    def delete_meme(self, meme_id, auth_data=None):
        self.url = f'{self.base_url}/meme/{meme_id}'
        self.response = requests.delete(url=self.url, headers=auth_data)
        self.status_code = self.response.status_code
        if self.status_code == 200:
            self.expected_success_message = (
                f'Meme with id {meme_id} successfully deleted'
            )
            self.actual_success_message = self.response.text
        else:
            if self.status_code == 401:
                self.expected_text_in_error_message = (
                    self.expected_text_in_unauthorized_error_message
                )
            elif self.status_code == 403:
                self.expected_text_in_error_message = (
                    self.expected_text_in_forbidden_error_message
                )
            elif self.status_code == 404:
                self.expected_text_in_error_message = (
                    self.expected_text_in_wrong_url_error_message
                )
            self.actual_error_message = self.response.text

    @allure.step('Send DELETE request to delete object with wrong url')
    def delete_meme_with_wrong_url(self, meme_id, auth_data=None):
        self.url = f'{self.base_url}/memes/{meme_id}'
        self.response = requests.delete(url=self.url, headers=auth_data)
        self.status_code = self.response.status_code
        self.expected_text_in_error_message = (
            self.expected_text_in_wrong_url_error_message
        )
        self.actual_error_message = self.response.text

    @allure.step('Assert successful deletion message')
    def assert_delete_message(self):
        assert self.actual_success_message == self.expected_success_message, (
            f'Expected message "{self.expected_success_message}", '
            f'but got "{self.actual_success_message}"'
        )
