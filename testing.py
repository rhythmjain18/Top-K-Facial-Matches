import unittest
from h11 import Data
import requests
import os


class Test(unittest.TestCase):
    def test_get_face_info1(self):
        form = {'id': 45}
        r = requests.post('http://127.0.0.1:5000/get_face_info/', data=form)
        dict = r.json()
        self.assertEqual(dict['Status'], 'Success')

    def test_get_face_info2(self):
        form = {'id': 45}
        r = requests.post('http://127.0.0.1:5000/get_face_info/', data=form)
        dict = r.json()
        self.assertEqual(dict['Body']['Name'], 'Salma_Hayek')

    def test_add_face(self):
        fo = open(f'{os.getcwd()}/uploads/Aaron_Eckhart_0001.jpg', 'rb')
        file = {"file": fo}
        form = {"name": "Aaron_Eckhart", "version": "0001",
                "date": "2022-03-09", "location": "USA"}
        r = requests.post('http://127.0.0.1:5000/add_face/',
                          files=file, data=form)
        fo.close()
        dict = r.json()
        self.assertEqual(dict['status'], 'Success')

    def test_add_faces_in_bulk(self):
        fo = open(f'{os.getcwd()}/uploads/test_dataset.zip', 'rb')
        file = {"file": fo}
        r = requests.post(
            'http://127.0.0.1:5000/add_faces_in_bulk/', files=file)
        fo.close()
        dict = r.json()
        self.assertEqual(dict['Status'], 'Success')

    def test_search_faces(self):
        fo = open(f'{os.getcwd()}/uploads/Abdullah_Gul_0003.jpg', 'rb')
        file = {"file": fo}
        form = {"k": "5", "confidence": "60"}
        r = requests.post(
            'http://127.0.0.1:5000/search_faces/', files=file, data=form)
        fo.close()
        dict = r.json()
        self.assertEqual(dict['Status'], 'Success')


if __name__ == '__main__':
    unittest.main()
