import json
import unittest

from api import user


class TestFixture(unittest.TestCase):

    def setUp(self, open_file='../data/response.json') -> None:
        self.request_data = user.request
        self.response_data = self._read_response_json_file(open_file=open_file)

    def tearDown(self) -> None:
        del self.request_data

    def _read_response_json_file(self, open_file='../data/response.json'):
        with open(open_file, 'r') as f:
            read_file = json.load(f)

        return read_file

    def _tmp_one_nest_success_response_data(self, first_key="data"):
        """ 1階層の response データと比較するテスト

        EX)
        {
            "data": {
                "id": 1,
                "name": "なまえ",
                "email": "sample@sample.com",
                "hobby": "baseball",
            }
        }

        """
        for key in (self.response_data[first_key].keys()):
            with self.subTest(key=key):
                self.assertEqual(self.request_data[first_key][key], self.response_data[first_key][key])

    def test_response_success1(self):
        """ 一つずつデータ比較を書く処理 """
        self.assertEqual(self.request_data["data"]["id"], self.response_data["data"]["id"])
        self.assertEqual(self.request_data["data"]["name"], self.response_data["data"]["name"])
        self.assertEqual(self.request_data["data"]["email"], self.response_data["data"]["email"])
        self.assertEqual(self.request_data["data"]["hobby"], self.response_data["data"]["hobby"])

    def test_response_success2(self):
        """ テストファイルの項目をすべて比較 """
        self._tmp_one_nest_success_response_data(first_key="data")


if __name__ == '__main__':
    unittest.main()
