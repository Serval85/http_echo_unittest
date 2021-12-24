from unittest import TestCase
import requests
from get_conf import get_config


class TestDelete(TestCase):
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

            requests.post(self.main_uri + '/api/upload',
                          data=payload, params=params)

        self.one_name = 'one_name'
        self.one_tag = 'one_tag'
        params = {'id': str(self.config['ID'] + 10),
                  'name': self.one_name,
                  'tag': self.one_tag}

        requests.post(self.main_uri + '/api/upload',
                      data=payload, params=params)

        self.r_get = requests.get(self.main_uri + '/api/get').json()

    def tearDown(self) -> None:
        id_cnt = 0
        for i in self.config['MASS_FILES']:
            id_cnt += 1
            params = {'id': str(self.config['ID'] + id_cnt)}
            requests.delete(self.main_uri + '/api/delete',
                            params=params)

        params = {'id': str(self.config['ID'] + 10),
                  'name': self.one_name,
                  'tag': self.one_tag}
        requests.delete(self.main_uri + '/api/delete',
                        params=params)

    def test_delete_id(self):
        params = {'id': str(self.config['ID'] + 1)}
        r = requests.delete(self.main_uri + '/api/delete',
                            params=params)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, '1 files deleted')

        r_new_get = requests.get(self.main_uri + '/api/get').json()
        self.assertIsNone(next((item for item in r_new_get
                                if item['id'] == self.config['ID'] + 1), None))

    def test_delete_name(self):
        params = {'name': self.one_name}
        r = requests.delete(self.main_uri + '/api/delete',
                            params=params)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, '1 files deleted')

        r_new_get = requests.get(self.main_uri + '/api/get').json()
        self.assertIsNone(next((item for item in r_new_get
                                if item['name'] == self.one_name), None))

    def test_delete_tag(self):
        params = {'tag': self.one_tag}
        r = requests.delete(self.main_uri + '/api/delete',
                            params=params)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, '1 files deleted')

        r_new_get = requests.get(self.main_uri + '/api/get').json()
        self.assertIsNone(next((item for item in r_new_get
                                if item['tag'] == self.one_tag), None))

        params = {'tag': self.config['TAG'] + str(self.config['ID'])}
        r = requests.delete(self.main_uri + '/api/delete',
                            params=params)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, '6 files deleted')

        r_new_get = requests.get(self.main_uri + '/api/get').json()

        # we delete all files at this moment
        self.assertEqual(len(r_new_get), 0)
        self.assertIsNone(next((item for item in r_new_get
                                if item['tag'] == self.config['TAG'] +
                                str(self.config['ID'])), None))

    def test_delete_noone_params(self):
        params = {'name': self.one_name, 'tag': self.one_tag}
        r = requests.delete(self.main_uri + '/api/delete',
                            params=params)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, '1 files deleted')

        r_new_get = requests.get(self.main_uri + '/api/get').json()
        self.assertIsNone(next((item for item in r_new_get
                                if (item['name'] == self.one_name and
                                    item['tag'] == self.one_tag)), None))

        fn = self.config['MASS_FILES'][1]
        params = {'id': str(self.config['ID'] + 2),
                  'name': fn,
                  'tag': self.config['TAG'] + str(self.config['ID'])}
        r = requests.delete(self.main_uri + '/api/delete',
                            params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, '1 files deleted')

        r_new_get = requests.get(self.main_uri + '/api/get').json()
        self.assertIsNone(next((item for item in r_new_get
                                if (item['id'] == str(self.config['ID'] + 2) and
                                    item['name'] == fn and
                                    item['tag'] == self.config['TAG'] +
                                    str(self.config['ID']))), None))

    def test_delete_wo_params(self):
        r = requests.delete(self.main_uri + '/api/delete')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.reason, 'No parameters')

        r_new_get = requests.get(self.main_uri + '/api/get').json()
        self.assertEqual(self.r_get, r_new_get)

    def delete_wrong_params(self):
        params = {'name': 'sfghsthy', 'tag': self.one_tag}
        r = requests.delete(self.main_uri + '/api/delete',
                            params=params)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, '0 files deleted')

        r_new_get = requests.get(self.main_uri + '/api/get').json()
        self.assertEqual(self.r_get, r_new_get)

