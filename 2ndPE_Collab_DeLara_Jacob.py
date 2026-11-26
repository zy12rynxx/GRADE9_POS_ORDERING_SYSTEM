from abc import ABC, abstractmethod


class MenuItem(ABC):
    """Base class with encapsulated attributes, getters/setters, and polymorphic subtotal."""

    def __init__(self, item_id: int, name: str, price: float):
        self.__item_id = item_id
        self.set_name(name)
        self.set_price(price)

    # Getters
    def get_item_id(self) -> int:
        return self.__item_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    # Setters with validation
    def set_name(self, name: str) -> None:
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("Product name cannot be empty.")
        self.__name = cleaned

    def set_price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Product price cannot be negative.")
        self.__price = float(price)

    @abstractmethod
    def calculate_subtotal(self, quantity: int) -> float:
        """Overridden by subclasses for polymorphic subtotal calculation."""
        pass

    def format_line(self) -> str:
        return f"{self.get_item_id():<5} {self.get_name():<18} ₱{self.get_price():>8.2f}"


class FoodItem(MenuItem):
    """Subclass inheriting from MenuItem for food products."""

    def calculate_subtotal(self, quantity: int) -> float:
        return self.get_price() * quantity


class DrinkItem(MenuItem):
    """Subclass inheriting from MenuItem for drink products."""

    def calculate_subtotal(self, quantity: int) -> float:
        return self.get_price() * quantity


class OrderLine:
    """Encapsulates an ordered item and its quantity with getters and setters."""

    def __init__(self, item: MenuItem, quantity: int):
        self.set_item(item)
        self.set_quantity(quantity)

    # Getters
    def get_item(self) -> MenuItem:
        return self.__item

    def get_quantity(self) -> int:
        return self.__quantity

    # Setters with validation
    def set_item(self, item: MenuItem) -> None:
        if not isinstance(item, MenuItem):
            raise TypeError("Ordered item must be a MenuItem instance.")
        self.__item = item

    def set_quantity(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__quantity = int(quantity)

    def get_subtotal(self) -> float:
        return self.__item.calculate_subtotal(self.__quantity)


def display_menu(menu: dict[int, MenuItem]) -> None:
    """Display available food and drink products grouped by category."""
    print("\n=== PRODUCT MENU ===")
    print(f"{'No.':<5} {'Product':<18} {'Price':>10}")
    print("-" * 35)

    print("--- FOOD ---")
    for item in menu.values():
        if isinstance(item, FoodItem):
            print(item.format_line())

    print("\n--- DRINKS ---")
    for item in menu.values():
        if isinstance(item, DrinkItem):
            print(item.format_line())

    print("-" * 35)


def take_orders(menu: dict[int, MenuItem]) -> list[OrderLine]:
    """Allow the user to select multiple products, enter quantities, and compute subtotals."""
    orders: list[OrderLine] = []
    max_num = len(menu)

    while True:
        display_menu(menu)

        while True:
            choice = input(f"Enter product number (1-{max_num}): ").strip()
            if choice.isdigit() and int(choice) in menu:
                selected_item = menu[int(choice)]
                break
            print(f"Invalid selection. Please enter a number from 1 to {max_num}.")

        while True:
            qty_input = input("Enter quantity: ").strip()
            if qty_input.isdigit() and int(qty_input) > 0:
                quantity = int(qty_input)
                break
            print("Please enter a valid positive whole number for quantity.")

        order_line = OrderLine(selected_item, quantity)
        orders.append(order_line)
        print(f"Added: {selected_item.get_name()} x {order_line.get_quantity()}")

        while True:
            more = input("Order another product? (yes/no): ").strip().lower()
            if more in ("yes", "no"):
                break
            print("Please enter 'yes' or 'no'.")

        if more == "no":
            break

    return orders


def show_order_subtotals(orders: list[OrderLine]) -> None:
    """Display each ordered item along with its calculated subtotal."""
    print("\n=== ORDERED ITEMS & SUBTOTALS ===")
    if not orders:
        print("No items were ordered.")
        return

    for line in orders:
        item = line.get_item()
        print(
            f"{item.get_name()} | Price: ₱{item.get_price():.2f} | "
            f"Qty: {line.get_quantity()} | Subtotal: ₱{line.get_subtotal():.2f}"
        )


def main() -> None:
    menu: dict[int, MenuItem] = {
        # Food Items
        1: FoodItem(1, "Burger", 50.00),
        2: FoodItem(2, "Cheeseburger", 65.00),
        3: FoodItem(3, "Fries", 35.00),
        4: FoodItem(4, "Chicken Nuggets", 75.00),
        5: FoodItem(5, "Hotdog Sandwich", 45.00),
        6: FoodItem(6, "Spaghetti", 60.00),
        # Drink Items
        7: DrinkItem(7, "Soft Drink", 25.00),
        8: DrinkItem(8, "Iced Tea", 30.00),
        9: DrinkItem(9, "Bottled Water", 20.00),
        10: DrinkItem(10, "Lemonade", 35.00),
        11: DrinkItem(11, "Iced Coffee", 55.00),
    }

    orders = take_orders(menu)
    show_order_subtotals(orders)


if __name__ == "__main__":
    main()


# Reciept and total calculation
class OrderItem:

  def __init__(self, name: str, quantity: int, unit_price: float):
    self.name = name
    self.quantity = quantity
    self.unit_price = unit_price

  @property
  def subtotal(self) -> float:
    return self.quantity * self.unit_price


class Receipt:

  def __init__(self, items: list[OrderItem]):
    self.items = items

  def calculate_total(self) -> float:
    return sum(item.subtotal for item in self.items)

  def format_receipt(self) -> str:
    lines = ["=" * 36, "             RECEIPT", "=" * 36]
    for item in self.items:
      lines.append(
          f"{item.name:<16} x{item.quantity:<3}"
          f" @{item.unit_price:>6.2f}  {item.subtotal:>6.2f}"
      )
    lines.append("-" * 36)
    lines.append(f"{'TOTAL':<28} {self.calculate_total():>7.2f}")
    lines.append("=" * 36)
    return "\n".join(lines)

  def display(self) -> None:
    print(self.format_receipt())
    
