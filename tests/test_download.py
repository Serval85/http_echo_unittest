from unittest import TestCase
import requests
from get_conf import get_config


class TestGet(TestCase):
    def setUp(self) -> None:
        self.config, self.main_uri = get_config()
        self.count_files = len(self.config['MASS_FILES'])
        id_cnt = 0
        for i in self.config['MASS_FILES']:
            id_cnt += 1
            with open(i, 'rb') as file:
                payload = file.read()
            params = {'id': str(self.config['ID'] + id_cnt),
                      'name': i,
                      'tag': self.config['TAG'] + str(self.config['ID'])}
            headers = {'Content-Type': self.config['FILE_TYPE']}
            requests.post(self.main_uri + '/api/upload',
                          data=payload, params=params, headers=headers)

    def tearDown(self) -> None:
        id_cnt = 0
        for i in self.config['MASS_FILES']:
            id_cnt += 1
            params = {'id': str(self.config['ID'] + id_cnt)}
            requests.delete(self.main_uri + '/api/delete',
                              params=params)

    def test_download(self):  # tc
        params = 'id=' + str(self.config['ID'] + 1)
        r = requests.get(self.main_uri + '/api/get', params=params)
        data = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(len(r.json()), 1)
        self.assertEqual(self.config['ID'] + 1, data[0].get('id'))
        self.assertEqual('programmers and other.jpg', data[0].get('name'))
        self.assertEqual('tag_123123', data[0].get('tag'))

        id_cnt = 0
        for i in self.config['MASS_FILES']:
            id_cnt += 1
            with open(i, 'rb') as file:
                source_file = file.read()
            params = {'id': str(self.config['ID'] + id_cnt)}

            r = requests.get(self.main_uri + '/api/download', params=params)
            downloaded_file = r.content
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.headers.get('Content-Disposition'),
                             'attachment; filename=' + i)
            self.assertEqual(source_file, downloaded_file)
            self.assertEqual(r.headers.get('Content-Type'),
                             self.config['FILE_TYPE'])

    def test_no_file(self):
        params = {'id': 'no_file'}
        r = requests.get(self.main_uri + '/api/download', params=params)

        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.reason, 'Not found')


