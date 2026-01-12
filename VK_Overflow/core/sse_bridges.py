import json
import urllib.request

from django.conf import settings


class Centrifugo:
    @staticmethod
    def publish(channel, data):
        payload = {
            'method': 'publish',
            'params': {
                'channel': channel,
                'data': data
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'apikey {settings.CENTRIFUGO_API_KEY}'
        }

        try:
            req = urllib.request.Request(
                settings.CENTRIFUGO_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers
            )
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Failed to publish to Centrifugo: {e}")
