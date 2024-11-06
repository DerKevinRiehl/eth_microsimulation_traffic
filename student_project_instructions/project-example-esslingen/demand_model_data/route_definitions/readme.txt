# Step 1 - Prepare File For Duaroute Tool
- Open `1_TripGenerator.py`
- Define entrance_exit_map and possible_routes
- Run the script `1_TripGenerator.py`
- This will create a file `2_Routes.xml`

# Step 2 - Use Sumo's "duaroute" tool to render Demand model

```C:\Users\kriehl\AppData\Local\sumo-1.19.0\bin>duarouter.exe -n network.net.xml -t 2_Routes.xml -o 3_duarouter_trips.xml```

# Step 3 - Create Demand Model for your simulation

- Open `4_route_creator.py`
- Specify `FLOW_PER_HOUR` (veh/h), `FROM_TIME`, `TO_TIME`, and `VEHICLE_TYPE` at the beginning of the file.
- Run the script `4_route_creator.py`
- This script will print into console, a complete Demand Model.
- You can use this script to create flows for specific vehicle types, times, that should spawn during the simulation.
