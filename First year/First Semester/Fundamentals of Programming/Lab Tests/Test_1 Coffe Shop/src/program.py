#
# Functions section
#


def create_coffe(name, country_of_origin, price):
    return {
        "name": name,
        "country_of_origin": country_of_origin,
        "price": price
    }


def add_coffe(coffees, name, country_of_origin, price):
    """
    A function that lets the user add a new coffee
    :param coffees: list of dict where we store all the data for the coffee
    :param name: the name of the coffee
    :param country_of_origin: the country of origin of the coffee
    :param price: the price of the coffee
    """
    coffe = create_coffe(name, country_of_origin, price)

    if coffe["price"] <= 0:
        print("Error: Invalid price!")

    coffees.append(coffe)

    return coffees


def display_coffe_sorted(coffees):
    """
    Function that sort the coffees by the country of origin and displays them
    :param coffees: list of dict where we store all the data for the coffee
    """
    sorted_coffees = sorted(coffees, key=lambda x: (x["country_of_origin"], x["price"]))
    print(sorted_coffees)


def valid_country_of_origin(country_of_origin):
    """
    function to check if the country of origin is valid
    """
    if country_of_origin == "":
        return False

    return True


def valid_price(price):
    """
    function to check if the price is valid
    """
    if price <= 0:
        return False

    return True


def filter_coffee(coffees, country_of_origin, price):
    """
    :param coffees: list of dict where we store all the data for the coffee
    :param country_of_origin: the country of origin of the coffee
    :param price: the price of the coffee
    """
    if valid_price(price) and valid_country_of_origin(country_of_origin):
        for coffee in coffees:
            if coffee["country_of_origin"] == country_of_origin:
                if coffee["price"] <= price:
                    print(coffee, " ")

    if valid_price(price) and not valid_country_of_origin(country_of_origin):
        for coffee in coffees:
            if coffee["price"] <= price:
                print(coffee, " ")

    if not valid_price(price) and valid_country_of_origin(country_of_origin):
        for coffee in coffees:
            if coffee["country_of_origin"] == country_of_origin:
                print(coffee, " ")

    if not valid_price(price) and not valid_country_of_origin(country_of_origin):
        print("No such coffees")

#
# User interface section
#


def display_ui():
    print("1. Add new coffe")
    print("2. Sort the coffees by country of origin")
    print("3. Filter the coffees base on country of origin and price")
    print("4. Exit")


def main():
    coffees = [
        create_coffe("Caffe miel", "France", 5.5),
        create_coffe("Starbucks", "UK", 12),
        create_coffe("Coffe nest", "Romania", 8),
        create_coffe("Zireto", "Romania", 13.5),
        create_coffe("GoodCoffee", "Spain", 7.5),
    ]

    display_ui()
    option_add_coffee = 1
    option_sort_coffee = 2
    option_fileter_coffee = 3
    option_end = 4

    while True:
        try:
            option = int(input("Chose an option from: "))
            if option == option_add_coffee:
                coffee = input("Write coffee name: ")
                country_of_origin = input("Write country of origin: ")
                try:
                    price = float(input("Write price of coffee: "))
                    coffees = add_coffe(coffees, coffee, country_of_origin, price)
                except ValueError:
                    print("Invalid value")
            if option == option_sort_coffee:
                display_coffe_sorted(coffees)
            if option == option_fileter_coffee:
                try:
                    country_of_origin = input("Write country of origin: ")
                    price = float(input("Write price of coffee: "))
                    filter_coffee(coffees, country_of_origin, price)
                except ValueError:
                    print("Invalid value")
            if option == option_end:
                print("End")
        except ValueError:
            print("Invalid Input")


main()
