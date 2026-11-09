# catalog-data-tools

Checks product CSV files before import. Errors report the line where the record ends, including records with quoted newlines. Standard library only, Python 3.10+.

```sh
python -m unittest -v
python catalog_check.py products.csv
python catalog_check.py products.csv --delimiter ";"
python catalog_check.py products.tsv --delimiter tab
```

```csv
sku,name,price,stock
BRUSH-01,"Brush, small",12.99,4
OIL-02,Oil,29.50,0
```

Use UTF-8. Commas are the default separator; select semicolon or tab explicitly. Prices use a decimal point. SKUs are trimmed and case-sensitive. Stock is a non-negative integer. Extra named columns can be empty, but each record must have the same number of fields as the header. Exit codes: 0 valid, 1 invalid data, 2 unreadable or malformed CSV. A header-only catalog is valid.

This validates file contents, not whether products exist in a store. It does not import data, change stock or connect to WooCommerce.
