import allure
import requests


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

    @allure.step('Assert response status is OK')
    def assert_response_is_200(self):
        assert (
            self.status_code == 200
        ), f'Expected status code 200, but got {self.status_code}'

    @allure.step('Assert response status is Bad Request')
    def assert_response_is_400(self):
        assert (
            self.status_code == 400
        ), f'Expected status code 400, but got {self.status_code}'

    @allure.step('Assert response status is Unauthorized')
    def assert_response_is_401(self):
        assert (
            self.status_code == 401
        ), f'Expected status code 401, but got {self.status_code}'

    @allure.step('Assert response status is Forbidden')
    def assert_response_is_403(self):
        assert (
            self.status_code == 403
        ), f'Expected status code 403, but got {self.status_code}'

    @allure.step('Assert response status is Not Found')
    def assert_response_is_404(self):
        assert (
            self.status_code == 404
        ), f'Expected status code 404, but got {self.status_code}'

    @allure.step('Assert response status is Server Error')
    def assert_response_is_500(self):
        assert (
            self.status_code == 500
        ), f'Expected status code 500, but got {self.status_code}'

    @allure.step('Assert meme data in response is the one sent in request')
    def assert_meme_data(self, expected_data):
        for key, value in expected_data.items():
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
