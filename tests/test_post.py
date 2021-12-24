import os
from unittest import TestCase
from unittest.mock import patch, Mock
import requests
from get_conf import get_config
from datetime import datetime


class TestPost(TestCase):
    @patch('requests.get')
    def setUp(self, Mockrequests) -> None:  # only for test Mock
        self.config, self.main_uri = get_config()
        self.file_size = os.path.getsize(self.config['FILE_NAME'])
        with open(self.config['FILE_NAME'], 'rb') as file:
            self.payload = file.read()

        req = Mockrequests()
        req_json = {'id': str(self.config['ID']),
                    'name': self.config['FILE_NAME'],
                    'tag': 'ololo'}

        req.get.return_value = Mock(status_code=201, json=req_json)
        params = {'name': self.config['FILE_NAME']}

        r = req.get(self.main_uri + '/api/get',
                    params=params)
        self.assertEqual(r.status_code, self.config['STATUS'])

    def tearDown(self):
        params = {'tag': self.config['TAG']}
        requests.delete(self.main_uri + '/api/delete',
                        params=params)

        params = {'tag': 'None'}
        requests.delete(self.main_uri + '/api/delete',
                        params=params)

    def test_post(self):
        params = {'id': str(self.config['ID']),
                  'name': self.config['FILE_NAME'],
                  'tag': self.config['TAG']}
        headers = {'Content-Type': 'image/jpeg'}
        r = requests.post(self.main_uri + '/api/upload',
                          data=self.payload, params=params, headers=headers)
        resp_text = r.json()

        r_data = [resp_text.get('id'), resp_text.get('tag'),
                  resp_text.get('size'), resp_text.get('mimeType')]

        req_data = [str(self.config['ID']),
                    self.config['TAG'],
                    self.file_size,
                    headers.get('Content-Type')]
        self.assertEqual(r.status_code, self.config['STATUS'])
        self.assertEqual(r.reason, self.config['REASON'])
        self.assertEqual(r_data, req_data)  # for exp equal lists

    def test_post_cyr(self):
        params = {'name': 'трололо',
                  'tag': self.config['TAG']}

        r = requests.post(self.main_uri + '/api/upload',
                          data=self.payload, params=params)
        data = r.json()
        self.assertEqual(r.status_code, self.config['STATUS'])
        self.assertEqual(r.reason, self.config['REASON'])
        self.assertTrue(data.get('id'))
        self.assertEqual(data.get('name'), 'трололо')
        self.assertEqual(data.get('tag'), self.config['TAG'])
        self.assertEqual(data.get('size'), self.file_size)

    def test_post_dig(self):
        params = {'id': 123456, 'name': 123456, 'tag': self.config['TAG']}

        r = requests.post(self.main_uri + '/api/upload',
                          data=self.payload, params=params)
        data = r.json()
        self.assertEqual(r.status_code, self.config['STATUS'])
        self.assertEqual(r.reason, self.config['REASON'])
        self.assertEqual(data.get('id'), '123456')
        self.assertEqual(data.get('name'), '123456')
        self.assertEqual(data.get('tag'), self.config['TAG'])
        self.assertEqual(data.get('size'), self.file_size)

    def test_post_wo_params(self):
        r = requests.post(self.main_uri + '/api/upload',
                          data=self.payload)
        data = r.json()
        self.assertEqual(r.status_code, self.config['STATUS'])
        self.assertEqual(r.reason, self.config['REASON'])
        self.assertTrue(data.get('id'))
        self.assertEqual(data.get('name'), data.get('id'))
        self.assertTrue(data.get('tag'), 'None')
        self.assertEqual(data.get('size'), self.file_size)

    def test_post_rewrite(self):
        params = {'id': str(self.config['ID']),
                  'name': self.config['FILE_NAME'],
                  'tag': self.config['TAG']}
        headers = {'Content-Type': 'image/jpeg'}
        r = requests.post(self.main_uri + '/api/upload',
                          data=self.payload, params=params, headers=headers)
        resp_text = r.json()

        r_data_first = [resp_text.get('id'), resp_text.get('tag'),
                        resp_text.get('size'), resp_text.get('mimeType'),
                        resp_text.get('name'),
                        resp_text.get('modificationTime')]

        rw = requests.post(self.main_uri + '/api/upload',
                           data=self.payload, params=params, headers=headers)

        resp_text_rw = rw.json()

        r_data_second = [resp_text_rw.get('id'), resp_text_rw.get('tag'),
                         resp_text_rw.get('size'), resp_text_rw.get('mimeType'),
                         resp_text_rw.get('name'),
                         resp_text_rw.get('modificationTime')]

        self.assertGreater(datetime.fromisoformat(r_data_second[5]),
                           datetime.fromisoformat(r_data_first[5]))
        self.assertEqual(r_data_first[:5], r_data_second[:5])

        nn = 'new_name'
        params = {'id': str(self.config['ID']),
                  'name': nn,
                  'tag': self.config['TAG']}
        headers = {'Content-Type': 'image/jpeg'}

        rw_nn = requests.post(self.main_uri + '/api/upload',
                           data=self.payload, params=params, headers=headers)

        resp_text_rw_nn = rw_nn.json()

        r_data_third = [resp_text_rw_nn.get('id'), resp_text_rw_nn.get('tag'),
                        resp_text_rw_nn.get('size'),
                        resp_text_rw_nn.get('mimeType'),
                        resp_text_rw_nn.get('name'),
                        resp_text_rw_nn.get('modificationTime')]

        self.assertEqual(r_data_third[4], nn)
        self.assertGreater(datetime.fromisoformat(r_data_third[5]),
                           datetime.fromisoformat(r_data_second[5]))
        self.assertEqual(r_data_first[:4], r_data_third[:4])

    def test_file_data(self):
        params = {'id': str(self.config['ID']),
                  'name': self.config['FILE_NAME'],
                  'tag': self.config['TAG']}
        headers = {'Content-Type': 'image/jpeg'}
        requests.post(self.main_uri + '/api/upload',
                      data=self.payload, params=params, headers=headers)

        r = requests.get(self.main_uri + '/api/download', params=params)
        downloaded_file = r.content
        self.assertEqual(r.headers.get('Content-Disposition'),
                         self.config['FILE_NAME'])
        self.assertEqual(self.payload, downloaded_file)




