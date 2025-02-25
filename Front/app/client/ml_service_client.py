class MLServiceClient:
    _instance = None

    def __new__(cls, base_url=None):
        if cls._instance is None:
            if base_url is None:
                raise ValueError("base_url must be provided on the first initialization.")
            cls._instance = super(MLServiceClient, cls).__new__(cls)
            cls._instance.base_url = base_url
        return cls._instance

    def __init__(self, base_url=None):
        if hasattr(self, 'base_url'):
            return
        self.base_url = base_url

    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

