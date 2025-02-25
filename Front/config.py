api_url = os.environ.get('API_URL', 'http://localhost:8000')
app_client = MLServiceClient(api_url)


def get_app_client():
    return app_client