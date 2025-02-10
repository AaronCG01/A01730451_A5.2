"""Program Activity 5.2 - Compute the total cost for all sales
   included in a JSON archive
   Aarón Cortés García - A01730451
"""

#  pylint: disable=invalid-name

import sys
import time
import json


def main():
    """Main function to compute total sales cost."""
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py <catalogue.json> <sales.json>")
        sys.exit(1)

    price_file, sales_file = sys.argv[1], sys.argv[2]
    start_time = time.time()  # Start measuring execution time

    try:
        with open(price_file, 'r', encoding='utf-8') as file:
            product_data = json.load(file)  # Load product price data

        with open(sales_file, 'r', encoding='utf-8') as file:
            sales_data = json.load(file)  # Load sales data
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error loading files: {error}")
        sys.exit(1)

    # Create price lookup dictionary with case-insensitive product names
    price_catalogue = {item['title']: item['price'] for item in product_data}
    total_sales = 0.0  # Store total sales amount

    for sale in sales_data:
        product = sale.get('Product', '')
        quantity = sale.get('Quantity')

        try:
            quantity = int(quantity)  # Ensure quantity is an integer
            if quantity < 0:
                print(f"W: Negative quantity detected for '{product}'.")

            if product in price_catalogue:
                cost = price_catalogue[product] * quantity
                total_sales += cost  # Accumulate total cost
            else:
                print(f"E: Product '{product}' not found in catalog.")
        except (ValueError, TypeError):
            print(f"Invalid sale entry ignored: {sale}")  # Notify invalid data

    elapsed_time = time.time() - start_time  # Compute execution time

    # Print results to console
    print(f"COST OF PRODUCTS EXTRACTED FROM THE FILE {price_file}")
    print(f"SALES INFORMATION EXTRACTED FROM THE FILE {sales_file}")
    print(f"TOTAL COST OF SALES: {total_sales:.2f}")
    print(f"EXECUTION TIME: {elapsed_time:.6f} seconds")

    # Save results to file
    with open("SalesResults.txt", "w", encoding="utf-8") as file:
        file.write(f"COST OF PRODUCTS EXTRACTED FROM THE FILE {price_file}\n")
        file.write(f"SALES INFORMATION EXTRACTED FROM THE FILE {sales_file}\n")
        file.write(f"TOTAL COST OF SALES: {total_sales:.2f}\n")
        file.write(f"EXECUTION TIME: {elapsed_time:.6f} seconds\n")


if __name__ == "__main__":
    main()
