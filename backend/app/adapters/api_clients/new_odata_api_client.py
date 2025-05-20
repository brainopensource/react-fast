import requests
from requests.auth import HTTPBasicAuth

class NewODataAPIClient:
    def __init__(self, url, username, password):
        print(f"[NewODataAPIClient.__init__] Initializing with url={url}, username={username}, password={password}")
        self.url = url
        self.username = username
        self.password = password

    def fetch_data(self, endpoint: str = None):
        url = self.url
        print(f"[NewODataAPIClient.fetch_data] Called with url={url}, endpoint={endpoint}")
        print(f"[NewODataAPIClient.fetch_data] Fetching data from url={url} with username={self.username} and password={self.password}")
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        print(f"[NewODataAPIClient.fetch_data] Response status_code={response.status_code}")
        try:
            print(f"[NewODataAPIClient.fetch_data] Response JSON: {response.json()}")
        except Exception as e:
            print(f"[NewODataAPIClient.fetch_data] Could not decode JSON: {e}")
        response.raise_for_status()
        return response
