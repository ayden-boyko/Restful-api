import unittest
from tests.test_utils import *
import json


class TestExample(unittest.TestCase):


    def setUp(self):  
        post_rest_call(self, 'http://localhost:5000/manage/init')
        print("DB Should be reset now")

    def test_hello_world(self):
        expected = { '1' : 'hello, world!' }
        actual = get_rest_call(self, 'http://localhost:5000')
        self.assertEqual(expected, actual)

    def test_get_info_rider(self):
        result = get_rest_call(self, 'http://localhost:5000/accountinfo/rider/1')
        self.assertIsNotNone(result)

    def test_get_info_driver(self):
        result = get_rest_call(self, 'http://localhost:5000/accountinfo/driver/1')
        self.assertIsNotNone(result)
    
    def test_get_past_ride_info(self):
        result = get_rest_call(self, 'http://localhost:5000/rideinfo')
        self.assertEqual(2, len(result))

    def test_get_accounts_info(self):
        result = get_rest_call(self, 'http://localhost:5000/accountinfo/accounts')
        self.assertEqual(4, len(result))

    def test_get_receipts(self):
        result = get_rest_call(self, 'http://localhost:5000//transaction/reciept',
                                {'id':'1', 'reciepts': '5'})
        self.assertEqual(2, len(result))

    def test_delete_accounts_driver(self):
        delete_rest_call(self, 'http://localhost:5000/accountinfo/driver/1')
        after = get_rest_call(self, 'http://localhost:5000/accountinfo/driver/1')
        self.assertEqual(False, after[7])

    def test_delete_accounts_rider(self):
        delete_rest_call(self, 'http://localhost:5000/accountinfo/rider/1')
        after = get_rest_call(self, 'http://localhost:5000/accountinfo/rider/1')
        self.assertEqual(False, after[6]) 

    def test_add_accounts_driver(self):
        result = [2]
        after = post_rest_call(self, 'http://localhost:5000/accountinfo/driver/0', 
                                params=json.dumps({'role': 'driver', 'name':'Sam Frombogen', 'date':'2001-10-16'}),
                                post_header={'Content-Type':'application/json'})
        self.assertNotEqual(result, after) 

    def test_add_accounts_rider(self):
        result = [3]
        after = post_rest_call(self, 'http://localhost:5000/accountinfo/rider/0',
                                params=json.dumps({'role': 'rider', 'name':'Alex Person', 'date':'2000-10-16'}),
                                post_header={'Content-Type': 'application/json'})
        self.assertEqual(result, after)

    def test_edit_accounts_info_rider(self):
        before = get_rest_call(self, 'http://localhost:5000/accountinfo/rider/1')
        put_rest_call(self, 'http://localhost:5000/accountinfo/rider/0',
                               params=json.dumps({'id':'1', 'instructions':'i dont needem'}),
                               put_header={'Content-Type': 'application/json'})
        after = get_rest_call(self, 'http://localhost:5000/accountinfo/driver/1')
        self.assertNotEqual(before,after )

    def test_edit_accounts_info_driver(self):
        before = get_rest_call(self, 'http://localhost:5000/accountinfo/driver/1')
        put_rest_call(self, 'http://localhost:5000/accountinfo/driver/0',
                               params=json.dumps({'id':'1', 'instructions':'i dont needem'}),
                               put_header={'Content-Type':'application/json'})
        after = get_rest_call(self, 'http://localhost:5000/accountinfo/driver/1')
        self.assertNotEqual(before, after )

    def test_remove_nonexistant_rider(self):
        result = delete_rest_call(self, 'http://localhost:5000/accountinfo/rider/6', expected_code=400)
    
    def test_add_pre_existing_rider(self):
        result = post_rest_call(self, 'http://localhost:5000/accountinfo/rider/0',
                                params=json.dumps({'role': 'rider', 'name':'Ayden Boyko', 'date':'2003-11-24'}),
                                post_header={'Content-Type': 'application/json'}, expected_code=400)
        
    def test_remove_nonexistant_driver(self):
        result = delete_rest_call(self, 'http://localhost:5000/accountinfo/driver/6', expected_code=400)
    
    def test_add_pre_existing_driver(self):
        result = post_rest_call(self, 'http://localhost:5000/accountinfo/driver/0',
                                params=json.dumps({'role': 'driver', 'name':'Ray Magliozzi', 'date':'1995-10-16'}),
                                post_header={'Content-Type': 'application/json'}, expected_code=400)