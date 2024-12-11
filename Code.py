class MenuItem:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

class Beverage(MenuItem):
    def __init__(self, name: str, price: float, temperature: float = 0, is_sugared: bool = False) -> None:
        super().__init__(name, price)
        self.temperature = temperature
        self.is_sugared = is_sugared

class Appetizer(MenuItem):
    def __init__(self, name: str, price: float, calories: float = 0) -> None:
        super().__init__(name, price)
        self.calories = calories

class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, is_vegetarian: bool = False, prep_time: float = 0) -> None:
        super().__init__(name, price)
        self.is_vegetarian = is_vegetarian
        self.prep_time = prep_time

class Menu:
    def __init__(self) -> None:
        self.items = [
            Beverage("Soda", 2),
            Beverage("Tea", 3),
            Beverage("Coffee", 5),
            Beverage("Juice", 4),
            Beverage("Water", 4),
            Appetizer("Fruit", 2),
            Appetizer("Cookies", 4),
            Appetizer("Popcorn", 4),
            MainCourse("Pizza", 10),
            MainCourse("Burger", 12),
            MainCourse("Spaghetti", 14),
            MainCourse("Salad", 8)
        ]

    def get_item(self, name: str) -> "MenuItem":
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

class Order:
    def __init__(self, menu: Menu) -> None:
        self.menu = menu
        self.menu_items = []
        
    # Add an item to the order
    def add_item(self, name: str) -> None:
        item = self.menu.get_item(name)  
        if item:
            self.menu_items.append(item)
        else:
            print(f"Item '{name}' is not in the menu")

    # Apply a discount
    def apply_discount(self) -> float:
        total_price = 0
        beverage_count = 0
        appetizer_count = 0
        main_course_count = 0

        for item in self.menu_items:
            total_price += item.price

            if type(item) == Beverage:
                beverage_count += 1
            elif type(item) == Appetizer:
                appetizer_count += 1
            elif type(item) == MainCourse:
                main_course_count += 1

        discount = 0
        if total_price >= 50:
            discount = 0.2  # 20% discount for orders above $50
        elif total_price >= 30:
            discount = 0.1  # 10% discount for orders above $30

        if beverage_count >= 2:
            discount += 0.05  # 5% extra discount for 2 or more beverages
        if appetizer_count >= 2:
            discount += 0.1  # 10% extra discount for 2 or more appetizers
        if main_course_count >= 1 and appetizer_count >= 1:
            discount += 0.1  # 10% combo discount for having a main course and appetizer

        return discount

    # Calculate total price
    def calculate_total_price(self) -> float:
        total_price = 0
        for item in self.menu_items:
            total_price += item.price

        discount = self.apply_discount()
        total_price -= total_price * discount  # Apply the discount
        return total_price
    
###################################################### # Can I improve this section and make it shorter?
class Payment:  ### This is obligatory, but how can i make it neccesary in the code?
    def pay(total_price: int) -> None:
        pass     
        
class CreditCard(Payment):
    def __init__(self, number: int, cvv: str) -> None:
        self.number = number
        self.cvv = cvv

    def pay(self, total_price: int) -> None:  # Here it comes de section where I pay the bill with my credit card
        if self.number < total_price: 
            print("The payment can not be done, there is not enough money in your credit card")
            return False
        print("Your bill has been succesfully paid")
        return True

class Cash(Payment):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def pay(self, total_price: int) -> None: # Here it comes de section where I pay de bill with cash
        if self.amount < total_price: 
            print("The payment can not be done, there is not enough money in cash")
            return False
        print("Your bill has been succesfully paid")
        return True
   

######################################################




menu = Menu()
order = Order(menu)

# Personal money 
my_cash = Cash(5)
my_credit_card = CreditCard(1, "123456789")


# Show the menu
print("Menu:")
for item in menu.items:
    print(f"{item.name} - ${item.price}")

print("\nType the name of the item you want to order. Type 'done' to finish your order\n")

# Allow the user to add more items
while True:
    item_name = input("Enter item name: ").strip()
    if item_name.lower() == "done":
        break
    order.add_item(item_name)


print("\nYour order:")
for item in order.menu_items:
    print(f"- {item.name}: ${item.price}")

# Calculate the total price
total_price = order.calculate_total_price()
print(f"\nThe total price is: ${total_price}")

### Here it comes the code where I pay for the bill if I have enough cash
### Improve logic
if order.menu_items and (my_cash.pay(total_price) or my_credit_card.pay(total_price)):  
    # Obtain more details about the order
    for item in order.menu_items:
        if type(item) == Beverage:
            item.temperature = float(input(f"Indicate the temperature of the {item.name.lower()}: "))
            item.is_sugared = input(f"Would you like your {item.name.lower()} with sugar? (y/n): ").strip().lower() == "y"
        elif type(item) == Appetizer:
            item.calories = float(input(f"Indicate the amount of calories for your {item.name.lower()}: "))
        elif type(item) == MainCourse:
            item.is_vegetarian = input(f"Would you like the {item.name.lower()} to be vegetarian? (y/n): ").strip().lower() == "y"
            item.prep_time = float(input(f"Indicate the preparation time for your {item.name.lower()} (in minutes): "))
        print("Your order will be soon prepared!")
else:
    print("\nNo items were ordered")
    

