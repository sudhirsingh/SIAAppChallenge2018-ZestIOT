# SIAAppChallenge2018-ZestIOT
POC Code by Zestiot team for Tracking F&amp;B consumption

1. main_video.py : This is poc code to capture the leftover food from camera and identify the type of food from color coding.
2. wastage_calculation.py : This is poc code to calculate the wastage from the information captured from camera and passenger list and uplift plan coming from SIA API. 

Follow these steps to run the code

1. clone or download the code
2. run the python code <br>
  py wastage_calculation.py
  
 
 The output of the program is For Flight SQ336 on date 2018-07-20. The Passenger detials and Upliftplan is fetch from API. The leftover meal is randomly decided and then wastage is calculated. 
 
 Sample output:

    Flight details:
Flight no.  = SQ336
Flight date = 2018-07-20

Meals summary:<br>
Business - Duck with rice (300g) x 10 (3.0Kg)<br>
Business - Chicken Pasta (300g) x 12 (3.6Kg)<br>
Business - Lamb Biryani (400g) x 5 (2.0Kg)<br>
Business - Grilled Salmon (250g) x 14 (3.5Kg)<br>
Business - Bread Basket (250g) x 7 (1.7Kg)<br>
Business - Fruit Basket (1000g) x 3 (3.0Kg)<br>
Business - Cheese platter (750g) x 1 (0.7Kg)<br>
Economy  - Fish with potatoes (270g) x 140 (37.8Kg)<br>
Economy  - Beef with egg noodles (250g) x 110 (27.5Kg)<br>
Economy  - E013 (50g) x 100 (5.0Kg)<br>

Left-over food measured by device:<br>
Business - Chicken Pasta x 4 (1.2Kg)<br>
Business - Grilled Salmon x 8 (2.0Kg)<br>
Business - Bread Basket x 6 (1.5Kg)<br>
Economy  - Fish with potatoes x 113 (30.5Kg)<br>
Economy  - Beef with egg noodles x 32 (8.0Kg)<br>
Economy  - E013 x 61 (3.0Kg)<br>

Wastage Calculation:

Business:<br>
Pax Cnt         = 5<br>
Meals Cnt       = 52<br>
Meals Wgt       = 17.6 Kg<br>
Avg Meal Wgt    = 12.9 g/meal<br>
Consumption     = 338 Kg<br>
Wastage         = 4.7 Kg<br>
Wastage per Pax = 940 g/Pax<br>

Economy :<br>
Pax Cnt         = 45<br>
Meals Cnt       = 350<br>
Meals Wgt       = 70.3 Kg<br>
Avg Meal Wgt    = 28.7 g/meal<br>
Consumption     = 200 Kg<br>
Wastage         = 41.5 Kg<br>
Wastage per Pax = 923 g/Pax<br>



