class ComplainedItem:
    def __init__(self, href: str, name: str, rating: int, rating_count: int, upper_item: str, brand: str):
        self.href = href
        self.name = name
        self.rating = rating
        self.rating_count = rating_count
        self.upper_item = upper_item
        self.brand = brand
        self.is_leaf = True