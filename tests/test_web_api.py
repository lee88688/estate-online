import json
import unittest
import pprint
from tests.utils import get_client


class TestWebApi(unittest.TestCase):
    def setUp(self):
        self.client = get_client()

    def test_query(self):
        payload = {
            'region': '44',
            'page_index': 1,
            'page_size': 10
        }
        res = self.client.post('/api/query', data=json.dumps(payload), content_type='application/json')
        data = json.loads(res.data)
        self.assertNotEqual(len(data['result']), 0)

    def test_region(self):
        res = self.client.get('/api/region')
        data = json.loads(res.data)
        self.assertEqual(type(data['result']), list)
        self.assertNotEqual(len(data['result']), 0)


if __name__ == "__main__":
    unittest.main()
