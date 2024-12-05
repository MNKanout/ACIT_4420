import unittest
from unittest.mock import mock_open, patch
from modules.data_loader import parse_json
import json

class TestDataLoader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='[{"routeName": "route1"}]')
    def test_parse_json_success(self, mock_file):
        data = parse_json('data/routes.json')
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]['routeName'], 'route1')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_parse_json_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            parse_json('data/missing.json')

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_parse_json_malformed_json(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            parse_json('data/routes.json')

if __name__ == '__main__':
    unittest.main()
