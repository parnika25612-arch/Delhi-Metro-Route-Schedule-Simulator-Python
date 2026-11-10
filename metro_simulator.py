
minutes = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"]
hours = ["06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]


def calculate_fare(total_minutes):
    if total_minutes <= 5: 
        return 10
    elif total_minutes <= 12: 
        return 20
    elif total_minutes <= 25: 
        return 30
    elif total_minutes <= 45: 
        return 40
    elif total_minutes <= 60: 
        return 50
    else: 
        return 60

def trip_duration(line_data, start_st, end_st):
    st_names = []
    for row in line_data:
        if len(row) > 1:
            st_names.append(row[1].strip())
    
    if len(line_data) > 0:
        last_val = line_data[-1][2].strip()
        st_names.append(last_val)

    if start_st not in st_names or end_st not in st_names:
        return 0 

    idxA = st_names.index(start_st)
    idxB = st_names.index(end_st)

    if idxA < idxB:
        lower = idxA
        upper = idxB
    else:
        lower = idxB
        upper = idxA

    total_mins = 0

    for i in range(lower, upper):
        try:
            total_mins += int(line_data[i][3])
        except (ValueError, IndexError):
            pass

    return total_mins

def metro_time(Line, Station, Time):
    try:
        with open("metro_data.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "Error: metro_data.txt file not found."

    found = False
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) > 2:
            if parts[0].strip() == Line:
                if parts[1].strip() == Station or parts[2].strip() == Station:
                    found = True
                    break
    if not found:
        return f"Station '{Station}' on Line '{Line}' not found."

    try:
        time_parts = Time.split(':')
        user_h = int(time_parts[0])
        user_m = int(time_parts[1])
        user_total_minutes = (user_h * 60) + user_m
    except ValueError:
        return "Invalid time format. Please use HH:MM"

    stops = []
    last_dep = 360 # 6:00 AM
    stops.append(last_dep)

    for hour in hours:
        for minute in minutes:
            h2 = int(hour)
            m2 = int(minute)
            curT = h2 * 60 + m2

            if (480 <= curT < 600) or (1020 <= curT < 1140):
                freq = 4
            else:
                freq = 8

            if curT >= last_dep + freq:
                stops.append(curT)
                last_dep = curT

    next_stops = []
    for stop_min in stops:
        if stop_min >= user_total_minutes:
            hh2 = stop_min // 60
            mm2 = stop_min % 60
            next_stops.append(f"{hh2:02}:{mm2:02}")

    if not next_stops:
        return "No service available."
    return next_stops


def find_all_routes(Source, Destination):
    try:
        with open("metro_data.txt", "r") as f:
            lines = f.readlines()
    except: 
        return []

    lines_db = {} 
    station_lines = {} 

    for l in lines:
        parts = l.strip().split(',')
        if len(parts) > 3:
            lname = parts[0].strip()
            s1 = parts[1].strip()
            s2 = parts[2].strip()
            
            if lname not in lines_db: 
                lines_db[lname] = []
            lines_db[lname].append(parts)

            if s1 not in station_lines: 
                station_lines[s1] = []
            if s2 not in station_lines: 
                station_lines[s2] = []

            if lname not in station_lines[s1]:
                station_lines[s1].append(lname)
            if lname not in station_lines[s2]:
                station_lines[s2].append(lname)

    found_routes = []

    for l_name in lines_db:
        data = lines_db[l_name]

        stations = []
        for x in data:
            stations.append(x[1].strip())
            stations.append(x[2].strip())

        if Source in stations and Destination in stations:
            dur = trip_duration(data, Source, Destination)
            found_routes.append({ 
                "type": "Direct", 
                "line1": l_name, 
                "duration": dur })

    if Source in station_lines:
        src_lines = station_lines[Source]
    else:
        src_lines = []

    if Destination in station_lines:
        dest_lines = station_lines[Destination]
    else:
        dest_lines = []

    for s_line in src_lines:
        for d_line in dest_lines:
            if s_line == d_line: 
                continue 

            s_data = lines_db[s_line]
            d_data = lines_db[d_line]
            
            s_stations = []
            for x in s_data:
                s_stations.append(x[1].strip())
                s_stations.append(x[2].strip()) 
            d_stations = []
            for x in d_data:
                d_stations.append(x[1].strip())
                d_stations.append(x[2].strip()) 
            common = []
            for s_st in s_stations:
                for d_st in d_stations:
                    if s_st == d_st:
                        if s_st not in common:
                            common.append(s_st)

            for interchange in common:
                leg1 = trip_duration(s_data, Source, interchange)
                leg2 = trip_duration(d_data, interchange, Destination)
                total = leg1 + 10 + leg2

                found_routes.append({
                    "type": "Interchange",
                    "interchange": interchange,
                    "line1": s_line,
                    "line2": d_line,
                    "duration": total,
                    "leg1_dur": leg1,
                    "leg2_dur": leg2
                })

    n = len(found_routes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if found_routes[j]['duration'] > found_routes[j+1]['duration']:
                found_routes[j], found_routes[j+1] = found_routes[j+1], found_routes[j]
    
    return found_routes



def journey_planner(Source, Destination, Time):
    routes = find_all_routes(Source, Destination)
    
    if not routes:
        print("No valid route found. Please check station names.")
        return

    print(f"\nI found {len(routes)} route(s) for you:")
    idx = 1
    for r in routes:
        if r['type'] == "Direct":
            print(f"{idx}. Direct Metro via {r['line1']} Line ({r['duration']} mins)")
        else:
            print(f"{idx}. Switch Metros at {r['interchange']} ({r['duration']} mins)")
        idx += 1

    if len(routes) == 1:
        choice = 1
    else:
        c = input("\nWhich option do you prefer? (1-" + str(len(routes)) + "): ")
        if c.isdigit() and 1 <= int(c) <= len(routes):
            choice = int(c)
        else:
            print("Invalid selection. Showing best route.")
            choice = 1
    
    selected = routes[choice-1]
    
    print("\n" + "========================================")
    print(f"       YOUR TRAVEL PLAN       ")
    print("========================================")

    if selected['type'] == "Direct":
        trains = metro_time(selected['line1'], Source, Time)

        if type(trains) == str: 
            print(trains) 
            return

        dept = trains[0]
        d_parts = dept.split(':')
        dh = int(d_parts[0])
        dm = int(d_parts[1])
        arr_m = (dh*60 + dm) + selected['duration']
        
        print(f"Start at {Source} ({selected['line1']} Line)")
        print(f"Next metro at {dept}")
        print(f"Arrive at {Destination} at {arr_m//60:02}:{arr_m%60:02}")
        print(f"Total travel time: {selected['duration']} minutes")
        
    else: 
        trains1 = metro_time(selected['line1'], Source, Time)

        if type(trains1) == str: 
            print(trains1)
            return
        
        dept1 = trains1[0]
        d1_parts = dept1.split(':')
        d1h = int(d1_parts[0])
        d1m = int(d1_parts[1])
        arr1_m = (d1h*60 + d1m) + selected['leg1_dur']
        
        
        ready_m = arr1_m + 10
        ready_str = f"{ready_m//60:02}:{ready_m%60:02}"
        
        trains2 = metro_time(selected['line2'], selected['interchange'], ready_str)

        if type(trains2) == str: 
            print("Connection missed.")
            return
        
        dept2 = trains2[0]
        d2_parts = dept2.split(':')
        d2h = int(d2_parts[0])
        d2m = int(d2_parts[1])
        arr2_m = (d2h*60 + d2m) + selected['leg2_dur']
        
        time_split = Time.split(':')
        start_min = int(time_split[0])*60 + int(time_split[1])
        total_trip_time = arr2_m - start_min

        print(f"Start at {Source} ({selected['line1']} Line)")
        print(f"Next metro at {dept1}")
        print(f"Arrive at {selected['interchange']} at {arr1_m//60:02}:{arr1_m%60:02}")
        print(f"Transfer to {selected['line2']} Line")
        print(f"Next {selected['line2']} metro departs at {dept2}")
        print(f"Arrive at {Destination} at {arr2_m//60:02}:{arr2_m%60:02}")
        print(f"Total travel time: {total_trip_time} minutes")

    fare = calculate_fare(selected['duration'])
    print("----------------------------------------")
    print(f"ESTIMATED FARE: ₹{fare}")
    print("========================================")

#Main Program

while True:
    print("\n=== DELHI METRO SIMULATOR ===")
    print("1. Get Metro Timings")
    print("2. Journey Planner")
    print("3. Fare Calculation")
    print("4. View Line Info")
    print("5. Exit")
    choice = input("\nPlease select an option (1-5): ").strip()

    if choice == '1':
        l = input("\nWhich Line? (e.g., Yellow): ").strip()
        s = input("Station Name: ").strip()
        t = input("Time (HH:MM): ").strip()

        results = metro_time(l, s, t)

        if type(results) == str: 
            print(results)
        elif len(results) > 0:
            print(f"\nNext metro at {results[0]}")
            next = results[1:3]
            if next:
                print(f"Subsequent metros at {next[0]}, {next[1]}, ...")
        else:
            print("\nSorry!,no more metros for today.")

    elif choice == '2':
        s = input("\nSource Station: ").strip()
        d = input("Destination Station: ").strip()
        t = input("Start Time (HH:MM): ").strip()

        journey_planner(s, d, t)

    elif choice == '3':
        try:
            m = int(input("\nTravel Duration (minutes): "))
            f = calculate_fare(m)
            print(f"Estimated Fare: Rs {f}")
        except ValueError:
            print("Error: Please enter a valid number for minutes!")
            continue
    
    elif choice == '4':
        t = input("\nLine Color (e.g. Blue, Yellow): ").strip()

        try:
            with open("metro_data.txt", "r") as f:
                data = f.readlines()
            
            st = []
            for r in data:
                parts = r.strip().split(',')
                if len(parts) > 2 and parts[0].strip().lower() == t.lower():
                    s1 = parts[1].strip()
                    s2 = parts[2].strip()

                    if s1 not in st:
                        st.append(s1)
                    if s2 not in st:
                        st.append(s2)

            if len(st) > 0:
                print(f"\nSTATIONS ON {t.upper()} LINE: ")
                st.sort()
                print(", ".join(st))
                print(f"\nTotal Stations: {len(st)}")
            else:
                print("Line not found.")
        except:
            print("Error reading file.")
            
    elif choice == '5':
        print("\nThank you for using Delhi Metro Sim!")
        print("Shutting down...")
        break
    else:
        print("Invalid choice, please try again.")