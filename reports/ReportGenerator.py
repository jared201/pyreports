import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import defaultdict
import locale
from datetime import datetime


def generate_sales_report():
    # Set the locale to US to format the currency as US dollars
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    # Load the JSON data
    with open('../data/customers.json') as f:
        sales_data = json.load(f)

    # Load the products data
    with open('../data/products.json') as f:
        products_data = json.load(f)

    # Load the contacts data
    with open('../data/contacts.json') as f:
        contacts_data = json.load(f)

    # Create a mapping of product_id to product_name
    product_names = {product['product_id']: product['product_name'] for product in products_data}

    # Create a mapping of contact_id to contact_name
    contact_names = {contact['contact_id']: contact['name'] for contact in contacts_data}

    # Process the sales data to get the total sales for each product and each customer
    product_sales = defaultdict(int)
    customer_sales = defaultdict(int)
    customer_products = defaultdict(int)
    grand_total_sales = 0
    for record in sales_data:
        product_name = product_names.get(record['product_id'], 'Unknown Product')
        customer_name = contact_names.get(record['contact_id'], 'Unknown Customer')
        total_sales = int(record['total_sales'])
        product_sales[product_name] += total_sales
        customer_sales[customer_name] += total_sales
        customer_products[customer_name] += int(record['quantity'])
        grand_total_sales += total_sales

    # Create a figure with custom size
    fig = plt.figure(figsize=(16, 9))

    # Create a subplot for the pie chart
    ax1 = fig.add_subplot(121)  # 121 means 1 row, 2 columns, and this is the first plot

    ax1.pie(product_sales.values(), labels=product_sales.keys(), autopct='%1.1f%%')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Get the current date and format it as a string
    run_date = datetime.now().strftime('%Y-%m-%d')

    # Append the run date to the title
    plt.title(f'Power Mac Center Sales Report For {run_date}')

    # Create a subplot for the table
    ax2 = fig.add_subplot(122)  # 122 means 1 row, 2 columns, and this is the second plot
    ax2.axis('off')  # Hide the axes

    # Create the table data
    table_data = [['Customer Name', 'Total Sales', 'Number of Products Sold']]
    for customer_name in customer_sales:
        table_data.append([customer_name, locale.currency(customer_sales[customer_name], grouping=True),
                           customer_products[customer_name]])

    # Add the table to the plot
    ax2.table(cellText=table_data, cellLoc='center', loc='center')

    # Add the grand total sales as a separate text box at the bottom of the page
    plt.figtext(0.5, 0.01, f'Grand Total Sales: {locale.currency(grand_total_sales, grouping=True)}', ha='center',
                va='center', fontsize=12, weight='bold')

    # Save the pie chart and table as a PDF
    pdf_pages = PdfPages('sales_report.pdf')
    pdf_pages.savefig(fig, bbox_inches='tight')
    pdf_pages.close()


# Call the function to generate the sales report
generate_sales_report()
