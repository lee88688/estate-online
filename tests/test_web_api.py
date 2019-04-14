import json
import unittest
import pprint
from tests.utils import get_client


class TestWebApi(unittest.TestCase):
    def setUp(self):
        self.client = get_client()

    def test_query(self):
        payload = {
            'region': '44'
        }
        res = self.client.post('/api/query', data=json.dumps(payload), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data['result']), 10)


if __name__ == "__main__":
    unittest.main()
