import logging
import requests
from requests.exceptions import RequestException
from .base_fetch_data import BaseFetchDataUseCase

class FetchJsonDataUseCase(BaseFetchDataUseCase):
    def process_data(self, data):
        # Process the data as needed
        return data
