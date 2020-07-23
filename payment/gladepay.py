import requests
from django.conf import settings
import json


class GladePay:
    """
    gladepay integration
    """
    key = settings.GP_KEY
    mid = settings.GP_MID

    def call(self, request_body, method='payment'):
        url = settings.GP_BASE_URL + method
        response = requests.post(
            url=url,
            headers={
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'key': self.key,
                'mid': self.mid
            },
            data=request_body,
            timeout=400
        )
        return response
