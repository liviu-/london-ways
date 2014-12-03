import sys
import json
import os.path 
import unittest

import fakeredis

# Ummm
main_package = os.path.join(os.path.dirname(os.path.abspath('.')),
                            os.path.basename(os.path.dirname(
                                os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(main_package)
import londonways

TEST_STATION = 'Harlington Corner'
TEST_STATION_ID = '57321'

class TestDataBase(unittest.TestCase):

    def setUp(self):
        self.conn = fakeredis.FakeStrictRedis()
        self.conn.set(TEST_STATION_ID, TEST_STATION)

    def test_redis_keys_store_data_correctly(self):
        assert TEST_STATION_ID.encode() in self.conn.keys()

    def test_redis_values_store_data_correctly(self):
        assert TEST_STATION.encode() in self.conn.mget(self.conn.keys())
    
class TestInterface(unittest.TestCase):
    def setUp(self):
        self.conn = fakeredis.FakeStrictRedis()
        self.conn.set(TEST_STATION_ID, TEST_STATION)
        self.app = londonways.app.test_client()

        # The stations are precalculated in the app
        londonways.STATIONS = zip([TEST_STATION_ID], [TEST_STATION])

    def test_title_on_main_page(self):
        rv = self.app.get('/')
        assert b'London Ways' in rv.data

    def test_form_exists(self):
        rv = self.app.get('/')
        assert b'<form' in rv.data
        assert b'</form>' in rv.data

    def test_submit_button_exists(self):
        rv = self.app.get('/')
        assert b'submit' in rv.data

    def test_data_appears_in_the_dropdown_list(self):
        rv = self.app.get('/')
        assert TEST_STATION.encode() in rv.data

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.app = londonways.app.test_client()

    def test_status_code(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_mimetype_is_html(self):
        rv = self.app.get('/')
        assert 'text/html' in rv.mimetype

    def test_chartset_is_utf_8(self):
        rv = self.app.get('/')
        assert 'utf-8' in rv.content_type

class TestBusStationPage(unittest.TestCase):
    def setUp(self):
        self.app = londonways.app.test_client()

    def test_title_is_correct(self):
        rv = self.app.get('/{}'.format(TEST_STATION_ID))
        assert TEST_STATION.encode() in rv.data

    def test_table_exists(self):
        rv = self.app.get('/{}'.format(TEST_STATION_ID))
        assert b'<table' in rv.data
        assert b'</table>' in rv.data

    def test_table_has_3_columns(self):
        rv = self.app.get('/{}'.format(TEST_STATION_ID))
        assert 3 == (rv.data.count(b'</td>') / 
                     rv.data.count(b'</tr>'))

    def test_table_headers_are_correct(self):
        rv = self.app.get('/{}'.format(TEST_STATION_ID))
        assert (b'Bus' and b'Destination' and b'Time left'
                in rv.data)

class TestAJAXRequests(unittest.TestCase):
    def setUp(self):
        self.app = londonways.app.test_client()

    def test_AJAX_returns_200_with_no_get_args(self):
        rv = self.app.get('/data/json')
        assert 200 == rv.status_code

    def test_AJAX_returns_200_with_get_args(self):
        rv = self.app.get('/data/json?bus_id={}'.format(TEST_STATION_ID))
        assert 200 == rv.status_code

    def test_AJAX_returns_JSON_data(self):
        rv = self.app.get('/data/json?bus_id={}'.format(TEST_STATION_ID))
        assert json.loads(rv.data.decode())

if __name__ == '__main__':
    unittest.main()
