import os
from unittest import TestCase
from unittest.mock import patch, Mock
import requests
from get_conf import get_config
import json

config = get_config()
count_files = len(config['MASS_FILES'])


class TestGet(TestCase):
    def setUp(self) -> None:
        id_cnt = 0
        for i in config['MASS_FILES']:
            id_cnt += 1
            with open(i, 'rb') as file:
                payload = file.read()
            params = {'id': str(config['ID'] + id_cnt),
                      'name': i,
                      'tag': config['TAG'] + str(config['ID'])}

            requests.post('http://' + str(config['IP']) + ':' +
                          str(config['PORT']) + '/api/upload',
                          data=payload, params=params)

    def tearDown(self) -> None:
        id_cnt = 0
        for i in config['MASS_FILES']:
            id_cnt += 1
            params = {'id': str(config['ID'] + id_cnt)}
            requests.delete('http://' + config['IP'] + ':' +
                            str(config['PORT']) + '/api/delete',
                              params=params)

    def test_get_two(self):  # tc get_3 _5
        params = 'id=' + str(config['ID'] + 1) + '&id=' + str(config['ID'] + 2)\
                 + '&tag=tag_123123'
        req_list_id = [str(config['ID'] + 1), str(config['ID'] + 2)]
        r = requests.get('http://' + str(config['IP']) + ':' +
                         str(config['PORT']) + '/api/get', params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        res_list_id = []
        for i in r.json():
            res_list_id.append(str(i.get('id')))
            self.assertIn(str(i.get('id')), req_list_id)
        self.assertEqual(req_list_id, res_list_id)
        self.assertEqual(len(r.json()), 2)

    def test_get_id(self):  # tc get_2_1
        params = 'id=' + str(config['ID'] + 1)
        r = requests.get('http://' + str(config['IP']) + ':' +
                         str(config['PORT']) + '/api/get', params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(len(r.json()), 1)
        data = r.json()
        self.assertEqual(config['ID'] + 1, data[0].get('id'))
        self.assertEqual('programmers and other.jpg', data[0].get('name'))
        self.assertEqual('tag_123123', data[0].get('tag'))

    def test_get_name(self):  # tc get_2_2
        params = 'name=programmers and other.jpg'
        r = requests.get('http://' + str(config['IP']) + ':' +
                         str(config['PORT']) + '/api/get', params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(len(r.json()), 1)
        data = r.json()
        self.assertEqual(config['ID'] + 1, data[0].get('id'))
        self.assertEqual('programmers and other.jpg', data[0].get('name'))
        self.assertEqual('tag_123123', data[0].get('tag'))

    def test_get_tag(self):  # tc get_2_3 all file have tag=tag_123123
        params = 'tag=tag_123123'
        r = requests.get('http://' + str(config['IP']) + ':' +
                         str(config['PORT']) + '/api/get', params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(len(r.json()), count_files)
        data = r.json()
        id_cnt = 0
        for i in data:
            self.assertEqual(config['ID'] + id_cnt + 1, i.get('id'))
            self.assertEqual(config['MASS_FILES'][id_cnt], i.get('name'))
            self.assertEqual('tag_123123', i.get('tag'))
            id_cnt += 1

    def test_get_all(self):  # assert counts sended and returned tc get_1
        r = requests.get('http://' + str(config['IP']) + ':' +
                         str(config['PORT']) + '/api/get')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(len(r.json()), count_files)

    def test_get_null(self):  # tc get_4
        params = 'id=' + str(config['ID'])  # id start as str(config['ID'] + 1)
        r = requests.get('http://' + str(config['IP']) + ':' +
                         str(config['PORT']) + '/api/get', params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertLess(len(r.json()), 1)

    def test_get_oneincorrect(self):  # tc get_6
        params = 'id=' + str(config['ID']) + '&id=' + str(config['ID'] + 2)\
                 + '&tag=tag_123123'
        req_id = str(config['ID'] + 2)
        r = requests.get('http://' + str(config['IP']) + ':' +
                         str(config['PORT']) + '/api/get', params=params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(len(r.json()), 1)
        self.assertEqual(str(r.json()[0].get('id')), req_id)






