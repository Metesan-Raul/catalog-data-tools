import io
import csv
import unittest
from catalog_check import validate


class CatalogTests(unittest.TestCase):
    def check(self, rows):
        return validate(io.StringIO("sku,name,price,stock\n" + rows))

    def test_valid_quoted_names_zero_and_decimal(self):
        self.assertEqual(self.check('P1,"Brush, small",12.99,4\nP2,Oil,0,0\n'), [])

    def test_missing_header(self):
        self.assertIn("header:", validate(io.StringIO("sku,name\n"))[0])

    def test_duplicate_header(self):
        self.assertEqual(validate(io.StringIO("sku,name,price,stock,price\n")),
                         ["header: duplicate column names"])

    def test_duplicate_trimmed_sku(self):
        self.assertIn("duplicate sku", self.check("P1,A,1,0\n P1 ,B,2,1\n")[0])

    def test_missing_values_and_extra_cells(self):
        for row in ("P1,A,1\n", "P1,A,1,0,extra\n"):
            with self.subTest(row=row):
                self.assertIn("column count", self.check(row)[0])

    def test_bad_prices(self):
        for price in ("-1", "NaN", "Infinity", "", "abc"):
            with self.subTest(price=price):
                self.assertIn("price must", self.check(f"P1,A,{price},0\n")[0])

    def test_bad_stock(self):
        for stock in ("-1", "1.5", "1e2", "", "²"):
            with self.subTest(stock=stock):
                self.assertIn("stock must", self.check(f"P1,A,1,{stock}\n")[0])

    def test_empty_identifiers(self):
        errors = self.check(" , ,1,0\n")
        self.assertEqual(len(errors), 2)

    def test_reports_multiple_rows(self):
        errors = self.check("P1,A,-1,0\nP2,B,1,-2\n")
        self.assertTrue(errors[0].startswith("row 2:"))
        self.assertTrue(errors[1].startswith("row 3:"))

    def test_semicolon_with_quoted_separator(self):
        data = 'sku;name;price;stock\nA;"Brush; small";12.99;4\n'
        self.assertEqual(validate(io.StringIO(data), delimiter=";"), [])

    def test_tab_separated_catalog(self):
        data = "sku\tname\tprice\tstock\nA\tBrush\t12.99\t4\n"
        self.assertEqual(validate(io.StringIO(data), delimiter="\t"), [])

    def test_wrong_separator_does_not_silently_pass(self):
        self.assertIn("header:", validate(io.StringIO("sku;name;price;stock\n"))[0])

    def test_unclosed_quoted_field(self):
        with self.assertRaises(csv.Error):
            self.check('A,"Unclosed,1,0\n')


if __name__ == "__main__":
    unittest.main()
