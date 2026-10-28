# catalog-data-tools

Checks product CSV files before import. Reports row numbers for missing values, duplicate SKUs, invalid prices and stock counts. Standard library only, Python 3.10+.

```sh
python -m unittest -v
python catalog_check.py products.csv
```

```csv
sku,name,price,stock
BRUSH-01,"Brush, small",12.99,4
OIL-02,Oil,29.50,0
```

Use UTF-8 and comma separators. Prices use a decimal point. SKUs are trimmed and case-sensitive. Stock is a whole number, zero or greater. Extra named columns are ignored. Exit codes: 0 valid, 1 invalid data, 2 unreadable file. An empty catalog with the required header is valid.

This validates file contents, not whether products exist in a store. It does not import data, change stock or connect to WooCommerce.
