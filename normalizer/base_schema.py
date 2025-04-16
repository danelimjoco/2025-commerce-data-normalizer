# base_schema.py
class UnifiedProduct:
    def __init__(self, id, title, price, currency, quantity, created_at):
        self.id = id
        self.title = title
        self.price = price
        self.currency = currency
        self.quantity = quantity
        self.created_at = created_at

    def to_dict(self):
        return self.__dict__
