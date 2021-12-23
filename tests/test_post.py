import os
from unittest import TestCase
from unittest.mock import patch, Mock
import requests
from get_conf import get_config


config = get_config()


class TestPost(TestCase):
    @patch('requests.get')
    def setUp(self, Mockrequests) -> None:  # only for test Mock
        req = Mockrequests()
        req_json = {'id': str(config['ID']),
                    'name': config['FILE_NAME'],
                    'tag': 'ololo'}

        req.get.return_value = Mock(status_code=201, json=req_json)
        params = {'name': config['FILE_NAME']}

        r = req.get('http://' + config['IP'] + ':' +
                    str(config['PORT']) + '/api/get',
                          params=params)
        self.assertEqual(r.status_code, config['STATUS'])

    def tearDown(self):
        params = {'tag': config['TAG']}
        requests.delete('http://' + config['IP'] + ':' +
                        str(config['PORT']) + '/api/delete',
                          params=params)

        params = {'tag': 'None'}
        requests.delete('http://' + config['IP'] + ':' +
                        str(config['PORT']) + '/api/delete',
                          params=params)

    def test_post(self):
        with open(config['FILE_NAME'], 'rb') as file:
            payload = file.read()
        file_size = os.path.getsize(config['FILE_NAME'])
        params = {'id': str(config['ID']),
                  'name': config['FILE_NAME'],
                  'tag': config['TAG']}
        headers = {'Content-Type': 'image/jpeg'}
        r = requests.post('http://' + config['IP'] + ':' +
                          str(config['PORT']) + '/api/upload',
                          data=payload, params=params, headers=headers)
        resp_text = r.json()

        r_data = [resp_text.get('id'), resp_text.get('tag'),
                  resp_text.get('size'), resp_text.get('mimeType')]

        req_data = [str(config['ID']),
                    config['TAG'],
                    file_size,
                    headers.get('Content-Type')]

        self.assertEqual(r.status_code, config['STATUS'])
        self.assertEqual(r.reason, config['REASON'])
        self.assertEqual(r_data, req_data)  # for exp equal lists

    def test_post_cyr(self):
        with open(config['FILE_NAME'], 'rb') as file:
            payload = file.read()
        file_size = os.path.getsize(config['FILE_NAME'])
        params = {'name': 'трололо',
                  'tag': config['TAG']}

        r = requests.post('http://' + config['IP'] + ':' +
                          str(config['PORT']) + '/api/upload',
                          data=payload, params=params)

        self.assertEqual(r.status_code, config['STATUS'])
        self.assertEqual(r.reason, config['REASON'])
        data = r.json()
        self.assertTrue(data.get('id'))
        self.assertEqual(data.get('name'), 'трололо')
        self.assertEqual(data.get('tag'), config['TAG'])
        self.assertEqual(data.get('size'), file_size)

    def test_post_dig(self):
        with open(config['FILE_NAME'], 'rb') as file:
            payload = file.read()
        file_size = os.path.getsize(config['FILE_NAME'])
        params = {'id': 123456, 'name': 123456, 'tag': config['TAG']}

        r = requests.post('http://' + config['IP'] + ':' +
                          str(config['PORT']) + '/api/upload',
                          data=payload, params=params)

        self.assertEqual(r.status_code, config['STATUS'])
        self.assertEqual(r.reason, config['REASON'])
        data = r.json()
        self.assertEqual(data.get('id'), '123456')
        self.assertEqual(data.get('name'), '123456')
        self.assertEqual(data.get('tag'), config['TAG'])
        self.assertEqual(data.get('size'), file_size)

    def test_post_wo_params(self):
        with open(config['FILE_NAME'], 'rb') as file:
            payload = file.read()
        file_size = os.path.getsize(config['FILE_NAME'])

        r = requests.post('http://' + config['IP'] + ':' +
                          str(config['PORT']) + '/api/upload',
                          data=payload)

        self.assertEqual(r.status_code, config['STATUS'])
        self.assertEqual(r.reason, config['REASON'])
        data = r.json()
        self.assertTrue(data.get('id'))
        self.assertEqual(data.get('name'), data.get('id'))
        self.assertTrue(data.get('tag'), 'None')
        self.assertEqual(data.get('size'), file_size)

