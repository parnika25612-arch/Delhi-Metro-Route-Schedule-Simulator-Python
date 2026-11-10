======================================================
DELHI METRO ROUTE AND SCHEDULE SIMULATOR
======================================================
Date: 25th Novemeber, 2025

------------------------------------------------------
1. PROJECT OVERVIEW
------------------------------------------------------
This Python program simulates how the Delhi Metro network runs. 
It meets the main assignment - reading the station file, 
working out the time of the next train with separate peak and off-peak rules, 
and building a trip that changes once between the Blue line and the Magenta line.

------------------------------------------------------
2. FILE LIST
------------------------------------------------------
1. metro_simulator.py  : The main Python source code.
2. metro_data.txt      : The database file containing station connectivity.
3. README.txt          : This documentation file 

------------------------------------------------------
3. HOW TO RUN THE PROGRAM
------------------------------------------------------
Prerequisites:
- Python 3.x installed on your system.
- No external libraries (like pandas or numpy) are required.

Steps:
1. Ensure 'metro_simulator.py' and 'metro_data.txt' are in the same folder.
2. Open a terminal or command prompt in that folder.
3. Run the command:
   python metro_simulator.py
4. A menu will appear. Enter the number corresponding to your choice:
  - Option 1: Find next scheduled train.
  - Option 2: Plan a journey.
  - Option 5: Exit the program.

------------------------------------------------------
4. DATA SOURCES
------------------------------------------------------
- Station order and connectivity data were approximated using official 
  DMRC network maps.
- Travel times between stations are estimates based on average metro speeds 
  and typical travel durations found on Google Maps/DMRC app.
- Peak/Off-peak frequency windows are based on standard operational hours.

------------------------------------------------------
5. ASSUMPTIONS & LOGIC
------------------------------------------------------
To simplify the simulation for this assignment, the following assumptions 
were made:

A. TIMINGS & FREQUENCY
   - Service Hours: 06:00 AM to 11:00 PM.
   - Peak Hours: 08:00-10:00 AM and 05:00-07:00 PM.
   - Frequency: Trains run every 4 minutes during Peak Hours and every 
     8 minutes during Off-Peak hours.
   - Start Time: For simulation simplicity, the schedule assumes trains 
     start generating from 06:00 AM at all stations simultaneously.

B. ROUTING & INTERCHANGE
   - Interchange Buffer: A fixed 10-minute buffer is added to the travel 
     time whenever a user switches lines to account for walking between platforms.
   - Route Selection: The system prioritizes "Direct" routes first. If no 
     direct route exists, it searches for "1-Interchange" routes.

------------------------------------------------------
6. FEATURES IMPLEMENTED
------------------------------------------------------
Core Requirement: Blue & Magenta Line Data.
Core Requirement: Next Metro Calculation.
Core Requirement: Journey Planner (with Interchanges).
======================================================
