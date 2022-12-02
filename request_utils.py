class RequestUtils:

    @staticmethod
    def configure_bearer_token_header(token: str) -> str:
        return 'Bearer ' + token

    @staticmethod
    def configure_api_endpoint(api_version: str, phone_number_id: str):
        return f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"

    @staticmethod
    def configure_headers(token: str):
        return {
            'Authorization': RequestUtils.configure_bearer_token_header(token=token),
            'Content-Type': 'application/json'
        }

    @staticmethod
    def configure_number_with_country_code(number:str, country_code: str = +91):
        return country_code[1:] + number