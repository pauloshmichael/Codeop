def calculate_discount(amount, customer_type):
    if customer_type == "premium":
        if amount >= 1000:
            discount = 0.20  # 20% discount
        elif amount >= 500:
            discount = 0.15  # 15% discount
        else:
            discount = 0.10  # 10% discount
    elif customer_type == "regular":
        if amount >= 1000:
            discount = 0.10  # 10% discount
        elif amount >= 500:
            discount = 0.05  # 5% discount
        else:
            discount = 0.02  # 2% discount
    else:
        discount = 0.0  # No discount
    
    return discount

def generate_customer_report(customers):
    print("=" * 60)
    print("TeleBirr Customer Report")
    print("=" * 60)
    print(f"{'Customer':<15} {'Type':<10} {'Amount':<10} {'Discount':<10} {'Final':<10}")
    print("-" * 60)
    
    total_revenue = 0
    total_discount = 0
    
    for customer in customers:
        name = customer.get('name', 'Unknown')
        customer_type = customer.get('type', 'regular')
        amount = customer.get('amount', 0)
        
        discount_rate = calculate_discount(amount, customer_type)
        discount_amount = amount * discount_rate
        final_amount = amount - discount_amount
        
        total_revenue += final_amount
        total_discount += discount_amount
        
        print(f"{name:<15} {customer_type:<10} {amount:<10.2f} {discount_amount:<10.2f} {final_amount:<10.2f}")
    
    print("-" * 60)
    print(f"Total Revenue: {total_revenue:.2f} ETB")
    print(f"Total Discounts Given: {total_discount:.2f} ETB")
    print(f"Number of Customers: {len(customers)}")
    print("=" * 60)

customers = [
    {"name": "Abebe", "type": "premium", "amount": 1500},
    {"name": "Kebede", "type": "regular", "amount": 750},
    {"name": "Hana", "type": "premium", "amount": 450},
    {"name": "Dawit", "type": "regular", "amount": 1200},
    {"name": "Eden", "type": "premium", "amount": 2000},
]

if __name__ == "__main__":
    generate_customer_report(customers)