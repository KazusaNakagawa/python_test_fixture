import unittest

from api import user
from test.test_fixture.test_fixture import TestFixture


class TestUser(unittest.TestCase):

    def setUp(self, open_file='../data/response.json', open_file2='../data/user.json') -> None:
        self.tf = TestFixture()
        # nest1      
        self.request_data = user.request
        self.response_data = self.tf.read_response_json_file(open_file=open_file)
        # nest2
        self.request_user = user.request_user
        self.response_user_data = self.tf.read_response_json_file(open_file=open_file2)

    def tearDown(self) -> None:
        del self.response_data
        del self.response_user_data

    def test_response_success1(self):
        """ 一つずつ、比較項目を書く処理 手間。。。 """
        self.assertEqual(self.request_data['data']['id'], self.response_data['data']['id'])
        self.assertEqual(self.request_data['data']['name'], self.response_data['data']['name'])
        self.assertEqual(self.request_data['data']['email'], self.response_data['data']['email'])
        self.assertEqual(self.request_data['data']['hobby'], self.response_data['data']['hobby'])

    def test_response_success2(self):
        """ テストファイル項目をループで簡素にすべて比較 """
        self.tf.tmp_one_nest_success_response_data(request_data=self.request_data,
                                                   response_data=self.response_data,
                                                   first_key='data')

    def test_response_success3(self):
        """ テストファイル, ２階層ネスト """
        self.tf.tmp_tow_nest_success_response_data(request_data=self.request_user,
                                                   response_data=self.response_user_data,
                                                   idx=0, first_key='data', second_key='user')
