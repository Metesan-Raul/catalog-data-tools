"""Validate a CSV before importing a product catalog. No writes to the source."""
import argparse
import csv
import sys
from decimal import Decimal, InvalidOperation


def validate(stream):
    reader = csv.DictReader(stream)
    required = {"sku", "name", "price", "stock"}
    if not required.issubset(reader.fieldnames or []):
        return ["header: required columns are sku, name, price, stock"]
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        return ["header: duplicate column names"]
    errors, seen = [], set()
    for row_number, row in enumerate(reader, 2):
        def fail(message):
            errors.append(f"row {row_number}: {message}")

        if None in row or any(row[key] is None for key in required):
            fail("column count does not match header")
            continue
        sku = row["sku"].strip()
        if not sku:
            fail("sku is empty")
        elif sku in seen:
            fail(f"duplicate sku {sku!r}")
        seen.add(sku)
        if not row["name"].strip():
            fail("name is empty")
        try:
            price = Decimal(row["price"].strip())
            if not price.is_finite() or price < 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            fail("price must be a finite non-negative decimal")
        stock = row["stock"].strip()
        if not stock.isascii() or not stock.isdecimal():
            fail("stock must be a non-negative integer")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    args = parser.parse_args()
    try:
        with open(args.csv_file, encoding="utf-8-sig", newline="") as stream:
            errors = validate(stream)
    except (OSError, UnicodeError, csv.Error) as exc:
        print(f"Cannot read CSV: {exc}", file=sys.stderr)
        return 2
    print("\n".join(errors) if errors else "Catalog valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
