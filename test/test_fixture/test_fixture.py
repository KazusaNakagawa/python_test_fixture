import json
import unittest


class TestFixture(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def read_response_json_file(self, open_file='../data/response.json'):
        with open(open_file, 'r') as f:
            read_file = json.load(f)

        return read_file

    def tmp_one_nest_success_response_data(self, response_data: dict, request_data: dict, first_key='data'):
        """ 1階層の response データと比較するテスト

        ExSample:
        {
          "data": {
            "id": 1,
            "name": "なまえ",
            "email": "sample@sample.com",
            "hobby": "baseball",
          }
        }

        """
        for key in (response_data[first_key].keys()):
            with self.subTest(key=key):
                self.assertEqual(request_data[first_key][key], response_data[first_key][key])

    def tmp_tow_nest_success_response_data(self, response_data: dict, request_data: dict, idx=0, first_key='data',
                                           second_key='user'):
        """ 2階層の response データと比較するテスト

        ExSample:
        [
          {
            "data": {
              "user": {
                "id": 1,
                "name": "なまえ",
                "email": "sample@sample.com",
                "post_number": "111-1111",
                "address1": "大阪府",
                "address2": "大阪市",
                "job": "witter"
              }
            }
          }
        ]
        """
        for key in response_data[idx][first_key][second_key].keys():
            with self.subTest(key=key):
                self.assertEqual(
                    request_data[idx][first_key][second_key][key],
                    response_data[idx][first_key][second_key][key]
                )


if __name__ == '__main__':
    unittest.main()
