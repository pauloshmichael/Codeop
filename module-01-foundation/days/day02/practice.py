# 1. Temperature label
print("=== Temperature Label ===")
temp = float(input("Enter temperature in °C: "))
if temp < 15:
    print("cold")
elif temp <= 28:
    print("warm")
else:
    print("hot")

# 2. Receipt loop
print("=== Receipt Loop ===")
for i in range(1, 11):
    print(f"Receipt #{i}")

# 3. Even numbers
print("=== Even Numbers ===")
for num in range(1, 21):
    if num % 2 == 0:
        print(num)

# 4. Discount function
print("=== Discount Function ===")
def apply_discount(price, percent=10):
    discount_amount = price * (percent / 100)
    return price - discount_amount

# Test with default discount (10%)
print(f"Price $100 with default 10% discount: ${apply_discount(100):.2f}")
# Test with custom discount (20%)
print(f"Price $100 with 20% discount: ${apply_discount(100, 20):.2f}")
# Test with another custom discount (15%)
print(f"Price $50 with 15% discount: ${apply_discount(50, 15):.2f}")


# 5. Countdown
print("=== Countdown ===")
count = 5
while count >= 1:
    print(count)
    count -= 1