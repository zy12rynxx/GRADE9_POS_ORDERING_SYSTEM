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


# Example usage
if __name__ == "__main__":
  order_items = [
      OrderItem("Burger", 2, 120.00),
      OrderItem("Fries", 1, 75.50),
      OrderItem("Iced Tea", 2, 45.00),
  ]
  receipt = Receipt(order_items)
  receipt.display()
  