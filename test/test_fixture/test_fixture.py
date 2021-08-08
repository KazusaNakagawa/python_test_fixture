import json
import logging
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

    def tmp_response_test_(self, nest: int,
                           request_data: dict, response_data: dict,
                           first_key='data', second_key='user', idx=0) -> None:
        # TODO: nestが範囲外の handling 処理
        """ json ファイルのネスト数に応じて対応する

        nest: データのネスト数: (1, 2) のみ対応
        """

        if nest == 1:
            self.tmp_one_nest_success_response_data(request_data=request_data,
                                                    response_data=response_data,
                                                    first_key=first_key,
                                                    )

        elif nest == 2:
            self.tmp_tow_nest_success_response_data(request_data=request_data,
                                                    response_data=response_data,
                                                    first_key=first_key,
                                                    second_key=second_key,
                                                    idx=idx,
                                                    )
        else:
            logging.debug(msg='No path test')

    def tmp_one_nest_success_response_data(self, response_data: dict, request_data: dict, first_key='data') -> None:
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
                                           second_key='user') -> None:
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
