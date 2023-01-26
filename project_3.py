from pathlib import Path
import csv

def main():
    while True:
        main_menu_display()
        selection = get_int("\nSelection: ")
        if selection == 3:
            break
        elif selection == 1:
            sales_return_menu()
        elif selection == 2:
            inventory_management()

def main_menu_display():
    print("Welcome to Wilson Parts!")
    print("\nSelect from menu below")
    print("*" * 25)
    print("1. Sales and Returns")
    print("2. Inventory Management")
    print("3. Exit")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except:
            print("Invalid input try again")

def read_csv():
    with open(Path(__file__).with_name("database.txt"), 'r') as database:
        items = [row for row in csv.reader(database)]
        return items

def sales_return_menu():
    while True:
        print("\nSales and Returns")
        print("*" * 25)
        print("1. Process Sale")
        print("2. Process Return")
        print("3. Return to previous menu")
        selection = get_int("\nSelection: ")
        if selection == 3:
            break
        elif selection == 1:
            sale_return_menu(1)
        elif selection == 2:
            sale_return_menu(2)

def sale_return_menu(num):
    while True:
        if num == 1:
            print("\nProcess Sale")
            print("Select one of the items below")
            print("*" * 25)
        elif num == 2:
            print("\nProcess Return")
            print("Select one of the items below")
            print("*" * 25)
        items = dynamic_inventory_menu()
        selection = get_int("\nSelection: ")
        if selection == len(items) + 1:
            break
        elif selection > len(items) + 1:
            print("Invalid Option. Try again...")
        elif num == 1:
             for index, value in enumerate(items):
                if selection == index + 1:
                    available_stock = int(value[2])
                    item_name = value[0]
                    item_price = float(value[1])
                    sale_calc(index, item_name, item_price, available_stock, items)
        else:
            for index, value in enumerate(items):
                if selection == index + 1:
                    available_stock = int(value[2])
                    item_name = value[0]
                    item_price = float(value[1])
                    return_calc(index, item_price, available_stock, items)

def dynamic_inventory_menu():
    items = read_csv()
    for index, value in enumerate(items):
        print(index + 1, value[0].capitalize())
    print(f"{len(items) + 1} Return to previous menu")
    return items

def sale_calc(indx, name, price, stock, data):
    while True:
        qty = get_int("Quantity of items your purchasing: ")
        if qty > stock:
            print(f"There are only currently: {stock} {name}s in stock.")
            print("Not enough items in inventory. Please try again")
        else:
            new_inventory = stock - qty
            modify_database(indx, 2, new_inventory, data)
            total = qty * price
            print(f"\nYou purchased {qty} for {price} each for total of ${round(total, 2)}")
            break

def return_calc(indx, price, stock, data):
    while True:
        qty = get_int("Quantity of items you're returning: ")
        returned_inventory = stock + qty
        modify_database(indx, 2, returned_inventory, data)
        total = qty * price
        print(f"\nYou returned {qty} for {price} each for total of ${round(total, 2)}")
        break

def modify_database(indx, item, inventory, data):
    with open(Path(__file__).with_name("database.txt"), 'w', newline='') as database:
        r = csv.writer(database, delimiter=',')
        data[indx][item] = str(inventory)
        for row in data:
            r.writerow(row)

def inventory_management():
    while True:
        print("\nInventory Management")
        print("*" * 25)
        print("1. Add item")
        print("2. Remove Item")
        print("3. Display All Items")
        print("4. Return to previous menu")
        print("3. Exit")
        selection = get_int("\nSelection: ")
        items = read_csv()
        if selection == 4:
            break
        elif selection == 1:
            add_item()
        elif selection == 2:
            remove_item(items)
        elif selection == 3:
            display_inventory()

def display_inventory():
    items = read_csv()
    print("\nCurrent Inventory")
    print("*" * 25)
    for value in items:
        print(*value, sep=' ')
    print("*" * 25)

def add_item():
    item_name = input("What is the item name: ")
    item_price = input("What is the item price: ")
    item_qty = input("What is the item quantity: ")
    item_list = [item_name, item_price, item_qty]
    with open(Path(__file__).with_name("database.txt"), 'a') as database:
        writer_object = csv.writer(database)
        writer_object.writerow(item_list)
    print(f"\n{item_name} was added sucessfully!")

def remove_item(data):
    item_name = input("What item item do you want to remove?: ")
    found_item = []
    for row in data:
        found_item.append(row)
        for field in row:
            if field == item_name:
                found_item.remove(row)
                print(f"\nRemoving: {item_name} from database")
    with open(Path(__file__).with_name("database.txt"), 'w', newline='') as database:
        writer = csv.writer(database)
        writer.writerows(found_item)

main()