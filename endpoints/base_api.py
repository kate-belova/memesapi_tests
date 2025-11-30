import allure
import requests

from schemas import PostMemeRequestSchema


class BaseAPI:
    def __init__(self):
        self.base_url = 'http://memesapi.course.qa-practice.com'
        self.response = requests.Response
        self.status_code = None
        self.content_type = None
        self.json = None
        self.data = None
        self.response_data = None
        self.expected_text_in_bad_request_error_message = 'Bad Request'
        self.expected_text_in_wrong_url_error_message = 'Not Found'
        self.expected_text_in_unauthorized_error_message = 'Unauthorized'
        self.expected_text_in_forbidden_error_message = 'Forbidden'
        self.expected_text_in_error_message = None
        self.actual_error_message = None

    @allure.step('Assert response status is {status}')
    def assert_response_status(self, status):
        assert (
            self.status_code == status
        ), f'Expected status code {status}, but got {self.status_code}'

    @allure.step('Assert meme data in response is the one sent in request')
    def assert_meme_data(self, expected_data, ignore_missing_fields=False):
        expected_data_validated = PostMemeRequestSchema(
            **expected_data
        ).model_dump()
        for key, value in expected_data_validated.items():
            if ignore_missing_fields and key not in self.response_data:
                continue

            assert self.response_data[key] == value, (
                f'Expected {key} to be {value}, '
                f'but got {self.response_data[key]}'
            )

    @allure.step('Assert error message')
    def assert_error_message(self):
        assert (
            self.expected_text_in_error_message in self.actual_error_message
        ), (
            f'Expected message should contain '
            f'"{self.expected_text_in_error_message}", '
            f'but error message is "{self.actual_error_message}"'
        )
