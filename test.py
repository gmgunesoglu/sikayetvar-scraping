from complained_item import ComplainedItem

def get_next_generation(item_list = []):
    next_items = []
    item: ComplainedItem
    for item in item_list:
        new_item = ComplainedItem(item.href + "/child", item.name + " child", item.rating, item.rating_count, item.href, item.brand)
        new_item.is_leaf = True
        next_items.append(new_item)
        item.brand = item.name
    return next_items

def print_item(item: ComplainedItem):
    print(f"href: {item.href}\nname: {item.name}\nrating: {item.rating}\nrating count: {item.rating_count}\nupper item: {item.upper_item}\nbrand: {item.brand}\nis leafe: {item.is_leaf}\n")


item = ComplainedItem("/tes","test",5,222,None,"/test")

item_list = []
item_list.append(item)
print_item(item_list[0])
next_item_list = get_next_generation(item_list)
print_item(item_list[0])
print_item(next_item_list[0])