from argparse import ArgumentParser
from json import dumps
from random import randint

import requests

# parse flignt_no and flight_date args
parser = ArgumentParser()
parser.add_argument('--flight_no', help='Flight number', required=True)
parser.add_argument('--flight_date', help='Flight date', required=True)
args = parser.parse_args()

FLIGHT_DATA = {
    'flightNo': args.flight_no,
    'flightDate': args.flight_date
}
API_BASE_URL = 'https://apigw.singaporeair.com'
HEADERS = {
    'Content-Type': 'application/json',
    'apikey': 'aghk73f4x5haxeby7z24d2rc'
}


def post(url, data=FLIGHT_DATA, headers=HEADERS):
    r = requests.post(url, data=dumps(data), headers=headers)
    return r


def get_min(a, b):
    return a if a <= b else b


api_meal_plan = '{}/appchallenge/api/meal/upliftplan'.format(API_BASE_URL)  # meal plan api url
api_passengers = '{}/appchallenge/api/flight/passenger'.format(API_BASE_URL)  # pax info api url
try:
    meal_plan = post(api_meal_plan)
    pax_load = post(api_passengers)
    if meal_plan.status_code == 200 and pax_load.status_code == 200:
        meal_plan = meal_plan.json()['response']['mealUpliftPlan']
        pax_load = pax_load.json()['response']['loadSummary']
    else:
        print 'Incorrect flight details.'
        exit()
except requests.exceptions.ConnectionError:
    print 'Connection error.'
    exit()

bus_pax_cnt = get_min(int(pax_load['businessClassCapacity:']),
                      int(pax_load['businessClassBookedLoad']))  # business class pax cnt
eco_pax_cnt = get_min(int(pax_load['economyClassCapacity:']),
                      int(pax_load['economyClassBookedLoad']))  # economy class pax cnt

print 'Flight details:\nFlight no.  = {}\nFlight date = {}'.format(FLIGHT_DATA['flightNo'], FLIGHT_DATA['flightDate'])

print '\nMeals summary:'
for i in meal_plan:  # for class in meal plan
    cls = i['bookingClass']
    container_info = i['containerUpliftInformation']
    if cls == 'Business':
        bus_meal_cnt = 0
        bus_meal_wgt = 0
        for j in container_info:
            quantity = int(j['quantity'])
            wgt = int(j['perPackWeight'][:-1])
            bus_meal_cnt += quantity
            bus_meal_wgt += wgt * quantity
            print '{} - {} ({}g) x {} ({}Kg)'.format(cls, j['meal'], wgt, quantity, round(quantity * wgt / 100) / 10.0)
    elif cls == 'Economy':
        eco_meal_cnt = 0
        eco_meal_wgt = 0
        for j in container_info:
            quantity = int(j['quantity'])
            wgt = int(j['perPackWeight'][:-1])
            eco_meal_cnt += quantity
            eco_meal_wgt += wgt * quantity
            print '{}  - {} ({}g) x {} ({}Kg)'.format(cls, j['meal'], wgt, quantity, round(quantity * wgt / 100) / 10.0)

PER_PAX_MEAL_CONS = 1500.0  # g

bus_cons = PER_PAX_MEAL_CONS * bus_pax_cnt
eco_cons = PER_PAX_MEAL_CONS * eco_pax_cnt
bus_wasted = bus_meal_wgt - bus_cons
eco_wasted = eco_meal_wgt - eco_cons

cur_bus_waste = 0
cur_eco_waste = 0
wasted = []
for i in meal_plan:  # for class in meal plan
    cls = i['bookingClass']
    container_info = i['containerUpliftInformation']
    if cls == 'Business' and cur_bus_waste < bus_wasted:
        for j in container_info:
            quantity = int(j['quantity'])
            wgt = int(j['perPackWeight'][:-1])
            wst_amt = randint(0, quantity)
            cur_bus_waste += wst_amt * wgt
            if wst_amt > 0:
                wasted.append({'class': cls, 'meal': j['meal'], 'amount': wst_amt, 'weight': wgt * wst_amt})
    elif cls == 'Economy' and cur_eco_waste < eco_wasted:
        for j in container_info:
            quantity = int(j['quantity'])
            wgt = int(j['perPackWeight'][:-1])
            wst_amt = randint(0, quantity)
            cur_eco_waste += wst_amt * wgt
            if wst_amt > 0:
                wasted.append({'class': cls, 'meal': j['meal'], 'amount': wst_amt, 'weight': wgt * wst_amt})

print '\nLeft-over food measured by device:'
for i in wasted:
    cls = i['class']
    meal = i['meal']
    amt = i['amount']
    wgt = i['weight']
    if cls == 'Business':
        print '{} - {} x {} ({}Kg)'.format(cls, meal, amt, round(wgt / 100) / 10.0)
    elif cls == 'Economy':
        print '{}  - {} x {} ({}Kg)'.format(cls, meal, amt, round(wgt / 100) / 10.0)

print '\nWastage Calculation:'
print '\nBusiness:\nPax Cnt         = {}\nMeals Cnt       = {}\nMeals Wgt       = {} Kg' \
      '\nAvg Meal Wgt    = {} g/meal\nConsumption     = {} Kg\nWastage         = {} Kg' \
      '\nWastage per Pax = {} g/Pax'.format(bus_pax_cnt, bus_meal_cnt, round(bus_meal_wgt / 100) / 10.0,
                                            round((bus_meal_wgt - cur_bus_waste) / 100) / 10.0,
                                            bus_meal_wgt / bus_meal_cnt, round(cur_bus_waste / 100) / 10.0,
                                            cur_bus_waste / bus_pax_cnt)
print '\nEconomy :\nPax Cnt         = {}\nMeals Cnt       = {}\nMeals Wgt       = {} Kg' \
      '\nAvg Meal Wgt    = {} g/meal\nConsumption     = {} Kg\nWastage         = {} Kg' \
      '\nWastage per Pax = {} g/Pax'.format(eco_pax_cnt, eco_meal_cnt, round(eco_meal_wgt / 100) / 10.0,
                                            round((eco_meal_wgt - cur_eco_waste) / 100) / 10.0,
                                            eco_meal_wgt / eco_meal_cnt, round(cur_eco_waste / 100) / 10.0,
                                            cur_eco_waste / eco_pax_cnt)
