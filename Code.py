class MenuItem:
    # Base class for all menu items 
    def __init__(self, name: str, price: float) -> None:
        self.__name = name    
        self.__price = price   

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def __str__(self):
        return f"{self.__name} - ${self.__price}"


class Beverage(MenuItem):
    # Subclass representing beverages with temperature and sugar preference
    def __init__(self, name: str, price: float, temperature: float = 0, is_sugared: bool = False) -> None:
        super().__init__(name, price)
        self.__temperature = temperature  
        self.__is_sugared = is_sugared  

    def get_temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def get_is_sugared(self):
        return self.__is_sugared

    def set_is_sugared(self, is_sugared):
        self.__is_sugared = is_sugared


class Appetizer(MenuItem):
    # Subclass representing appetizers 
    def __init__(self, name: str, price: float, calories: float = 0) -> None:
        super().__init__(name, price)
        self.__calories = calories  

    def get_calories(self):
        return self.__calories

    def set_calories(self, calories):
        self.__calories = calories


class MainCourse(MenuItem):
    # Subclass representing main courses with vegetarian preference and preparation time
    def __init__(self, name: str, price: float, is_vegetarian: bool = False, prep_time: float = 0) -> None:
        super().__init__(name, price)
        self.__is_vegetarian = is_vegetarian  
        self.__prep_time = prep_time         

    # Getter and Setter for vegetarian preference
    def get_is_vegetarian(self):
        return self.__is_vegetarian

    def set_is_vegetarian(self, is_vegetarian):
        self.__is_vegetarian = is_vegetarian

    # Getter and Setter for preparation time
    def get_prep_time(self):
        return self.__prep_time

    def set_prep_time(self, prep_time):
        self.__prep_time = prep_time


class Menu:
    # Menu contains all available menu items
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

    # Search for an item in the menu by name
    def get_item(self, name: str) -> "MenuItem":
        for item in self.items:
            if item.get_name().lower() == name.lower():
                return item
        return None


class Order:
    # Represents an order containing menu items and discount logic
    def __init__(self, menu: Menu) -> None:
        self.menu = menu
        self.__menu_items = []  # Private list of ordered items

    # Add an item to the order
    def add_item(self, name: str) -> None:
        item = self.menu.get_item(name)
        if item:
            self.__menu_items.append(item)
        else:
            print(f"Item '{name}' is not in the menu.")

    # Apply discount based on order composition and total cost
    def apply_discount(self) -> float:
        total_price = sum(item.get_price() for item in self.__menu_items)
        discount = 0

        if total_price >= 50:
            discount = 0.2
        elif total_price >= 30:
            discount = 0.1

        # Count beverages, appetizers, and main courses
        beverage_count = sum(1 for item in self.__menu_items if type(item) == Beverage)
        appetizer_count = sum(1 for item in self.__menu_items if type(item) == Appetizer)
        main_course_count = sum(1 for item in self.__menu_items if type(item) == MainCourse)

        if beverage_count >= 2:
            discount += 0.05
        if appetizer_count >= 2:
            discount += 0.1
        if main_course_count >= 1 and appetizer_count >= 1:
            discount += 0.1

        return discount

    # Calculate total order price with discount applied
    def calculate_total_price(self) -> float:
        total_price = sum(item.get_price() for item in self.__menu_items)
        discount = self.apply_discount()
        return total_price * (1 - discount)


class Payment:
    # Base class for payment methods
    def pay(self, total_price: float) -> bool:
        raise NotImplementedError("Subclasses must implement the pay method")


class CreditCard(Payment):
    def __init__(self, number: str, cvv: str, balance: float) -> None:
        self.__number = number
        self.__cvv = cvv
        self.__balance = balance

    def pay(self, total_price: float) -> bool:
        if self.__balance >= total_price:
            self.__balance -= total_price
            print(f"Payment of ${total_price} successful with card {self.__number[-4:]}")
            return True
        else:
            print("Insufficient balance on the credit card.")
            return False


class Cash(Payment):
    def __init__(self, amount: float) -> None:
        self.__amount = amount

    def pay(self, total_price: float) -> bool:
        if self.__amount >= total_price:
            self.__amount -= total_price
            print(f"Payment of ${total_price} successful with cash.")
            return True
        else:
            print(f"Insufficient cash. Need ${total_price - self.__amount}.")
            return False


# Create menu and order instances
menu = Menu()
order = Order(menu)

my_cash = Cash(100)
my_credit_card = CreditCard("1234567890123456", "123", 500)

# Display the menu
print("\nMenu:")
for item in menu.items:
    print(f"{item.name} - ${item.price}")

# Allow the user to place an order
while True:
    item_name = input("\nEnter item name (or 'done' to finish): ").strip()
    if item_name.lower() == "done":
        break
    order.add_item(item_name)

total_price = order.calculate_total_price()
print(f"\nTotal price: ${total_price}")

choice = input("\nChoose your payment method (cash/credit): ").strip().lower()

# Use the selected payment method to make the payment
if choice == "cash":
    if my_cash.pay(total_price):
        print("Order confirmed and paid in cash.")
elif choice == "credit":
    if my_credit_card.pay(total_price):
        print("Order confirmed and paid with credit card.")
else:
    print("Invalid payment method.")
