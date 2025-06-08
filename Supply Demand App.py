import matplotlib.pyplot as plt
import numpy as np
import math

def main():
    print("To start, first input the points for the demand and supply curves.")

    print("")
    print("Please input the points for the demand curve.")
    print("")

    print("Please enter the points in the format 'x,y' (e.g., '1,2'). Type 'done' when finished.")
    pointsDemand = []
    while True:
        point = input("Enter point: ")
        if point.lower() == 'done':
            break
        try:
            x, y = map(float, point.split(','))
            pointsDemand.append((x, y))
        except ValueError:
            print("Invalid input. Please enter the point in the correct format.")
        print("You entered the following points for the demand curve:", pointsDemand)

    print("")
    print("Now, please input the points for the supply curve.")
    print("")

    print("Please enter the points in the format 'x,y' (e.g., '1,2'). Type 'done' when finished.")
    pointsSupply = []
    while True:
        point = input("Enter point: ")
        if point.lower() == 'done':
            break
        try:
            x, y = map(float, point.split(','))
            pointsSupply.append((x, y))
        except ValueError:
            print("Invalid input. Please enter the point in the correct format.")
        print("You entered the following points for the supply curve:", pointsSupply)
    
    print("")
    print("")
    
    supplyCurve, supply_y_intercept, supply_slop = make_supply_curve(pointsSupply)
    demandCurve, demand_intercept, demand_power_cofficient = make_demand_curve(pointsDemand)

    print(f"Supply Curve: Qs = {supply_y_intercept}+{supply_slop}P")
    print(f"Demand Curve: Qd = {demand_intercept} * P^{demand_power_cofficient}")   

    print("")
    equilibrium_price, equilibrium_quantity = find_equilibrium(supplyCurve, demandCurve, pointsSupply, pointsDemand)

    print(f"Equilibrium Price = {equilibrium_price}, Equilibrium Quantity = {equilibrium_quantity}")
    print("")
    print("Generating the supply and demand curves...")
    plot_market(supplyCurve, demandCurve, equilibrium_price, equilibrium_quantity)
    print("")

    print("Now, you can input a price to find the quantity supplied and demanded at that price.")
    while True:
        price_input = input("Enter a price (or type 'exit' to quit): ")
        if price_input.lower() == 'exit':
            break
        try:
            price = float(price_input)
            quantity_supplied = round(supplyCurve(price),2)
            quantity_demanded = round(demandCurve(price),2)
            print(f"At price {price}, Quantity Supplied: {quantity_supplied}, Quantity Demanded: {quantity_demanded}")
        except ValueError:
            print("Invalid input. Please enter a valid price.") 








def find_equilibrium(supply_curve, demand_curve, pointsSupply, pointsDemand):
    all_prices = [point[0] for point in pointsSupply + pointsDemand]
    min_price = max(min(all_prices), 0.01)
    max_price = max(all_prices)
    best_price = None          
    smallest_diff = float('inf') 
    best_quantity = None  
    price = min_price
    step = 0.0001
    while price <= max_price:
        try:
            supply_q = supply_curve(price)
            demand_q = demand_curve(price)

            diff = abs(supply_q - demand_q)

            if diff < smallest_diff:
                smallest_diff = diff
                best_price = price
                best_quantity = (supply_q + demand_q) / 2  

        except Exception:
            pass

        price += step  
    return round(best_price, 2), round(best_quantity, 2)



def make_supply_curve(pointsSupply):
    x_values = []
    y_values = []

    for point in pointsSupply:
        price = point[0]
        quantity = point[1]

        x_values.append(price)
        y_values.append(quantity)

    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xx = sum(x**2 for x in x_values)
    sum_xy = sum(x*y for x, y in zip(x_values, y_values))

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    y_intercept = (sum_y - slope * sum_x) / n

    def supply_curve(price):
        return y_intercept + slope * price

    return supply_curve, y_intercept, slope


def make_demand_curve(pointsDemand):
    log_x = [math.log(pt[0]) for pt in pointsDemand]
    log_y = [math.log(pt[1]) for pt in pointsDemand]
    
    coefficient, intercept= np.polyfit(log_x, log_y, 1) 
    
    intercept = math.exp(intercept)  
    power_cofficient = coefficient

    def demand_curve(price):
        return intercept * price**(power_cofficient)
        
    return demand_curve, intercept, power_cofficient  




def plot_market(supply_curve, demand_curve, equilibrium_price, equilibrium_quantity):
    prices = [p / 100 for p in range(10, 500)]
    supply_quantities = [supply_curve(p) for p in prices]
    demand_quantities = [demand_curve(p) for p in prices]
    plt.figure(figsize=(10, 6))
    plt.plot(supply_quantities, prices, label='Supply Curve', color='green')
    plt.plot(demand_quantities, prices, label='Demand Curve', color='red')
    plt.scatter(equilibrium_quantity, equilibrium_price, color='blue', zorder=5, label='Equilibrium')

    plt.axhline(y=equilibrium_price, color='blue', linestyle='dotted')  
    plt.axvline(x=equilibrium_quantity, color='blue', linestyle='dotted')  

    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.title('Supply and Demand Curves with Equilibrium')
    plt.legend()
    plt.grid(True)

    plt.show()

    

if __name__ == '__main__':
    main()