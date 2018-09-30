# SIAAppChallenge2018-ZestIOT
POC Code by Zestiot team for Tracking F&amp;B consumption

Follow these steps to run the code

1. clone or download the code
2. run the python code
  py 
  
 
 The output of the program is For Flight SQ336 on date 2018-07-20. The Passenger detials and Upliftplan is fetch from API. The leftover meal is randomly decided and then wastage is calculated. 
 
 Sample output:
 
Flight details:
Flight no.  = SQ336
Flight date = 2018-07-20

Meals summary:
Business - Duck with rice (300g) x 10 (3.0Kg)
Business - Chicken Pasta (300g) x 12 (3.6Kg)
Business - Lamb Biryani (400g) x 5 (2.0Kg)
Business - Grilled Salmon (250g) x 14 (3.5Kg)
Business - Bread Basket (250g) x 7 (1.7Kg)
Business - Fruit Basket (1000g) x 3 (3.0Kg)
Business - Cheese platter (750g) x 1 (0.7Kg)
Economy  - Fish with potatoes (270g) x 140 (37.8Kg)
Economy  - Beef with egg noodles (250g) x 110 (27.5Kg)
Economy  - E013 (50g) x 100 (5.0Kg)

Left-over food measured by device:
Business - Chicken Pasta x 4 (1.2Kg)
Business - Grilled Salmon x 8 (2.0Kg)
Business - Bread Basket x 6 (1.5Kg)
Economy  - Fish with potatoes x 113 (30.5Kg)
Economy  - Beef with egg noodles x 32 (8.0Kg)
Economy  - E013 x 61 (3.0Kg)

Wastage Calculation:

Business:
Pax Cnt         = 5
Meals Cnt       = 52
Meals Wgt       = 17.6 Kg
Avg Meal Wgt    = 12.9 g/meal
Consumption     = 338 Kg
Wastage         = 4.7 Kg
Wastage per Pax = 940 g/Pax

Economy :
Pax Cnt         = 45
Meals Cnt       = 350
Meals Wgt       = 70.3 Kg
Avg Meal Wgt    = 28.7 g/meal
Consumption     = 200 Kg
Wastage         = 41.5 Kg
Wastage per Pax = 923 g/Pax
