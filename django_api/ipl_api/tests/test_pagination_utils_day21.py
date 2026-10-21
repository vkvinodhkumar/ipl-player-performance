from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from ipl_api.pagination_utils import parse_pagination_params, paginate_records

class PaginationHelperTests(SimpleTestCase):
    def test_defaults(self):
        self.assertEqual(parse_pagination_params({}), (1, 20))
    def test_valid_values(self):
        self.assertEqual(parse_pagination_params({'page': '2', 'page_size': '10'}), (2, 10))
    def test_rejects_non_integer(self):
        with self.assertRaises(ValidationError):
            parse_pagination_params({'page': 'abc'})
    def test_rejects_zero_page(self):
        with self.assertRaises(ValidationError):
            parse_pagination_params({'page': '0'})
    def test_rejects_oversized_page_size(self):
        with self.assertRaises(ValidationError):
            parse_pagination_params({'page_size': '101'})
    def test_paginates_records(self):
        records = [{'id': i} for i in range(1, 6)]
        payload = paginate_records(records, page=2, page_size=2)
        self.assertEqual(payload['count'], 5)
        self.assertEqual(payload['total_pages'], 3)
        self.assertEqual(payload['results'], [{'id': 3}, {'id': 4}])
