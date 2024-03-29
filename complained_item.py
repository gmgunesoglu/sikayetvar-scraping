class ComplainedItem:
    id: int

    def __init__(self, href: str, name: str, rating: int, rating_count: int, upper_item_id: int, brand_id: int):
        self.href = href
        self.name = name
        self.rating = rating
        self.rating_count = rating_count
        self.upper_item_id = upper_item_id
        self.brand_id = brand_id
        self.is_leaf = True