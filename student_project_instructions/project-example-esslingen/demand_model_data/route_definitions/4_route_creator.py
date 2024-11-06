# Define Parameters
FLOW_PER_HOUR = 10
FROM_TIME = 0
TO_TIME = 10000
VEHICLE_TYPE = "DEFAULT_TAXITYPE"



# Read duaroute file
fR = open("3_duarouter_trips.xml", "r")
lines = fR.read().split("\n")
fR.close()
lines = [l.strip() for l in lines]


# Print new File
print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
print("<routes xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://sumo.dlr.de/xsd/routes_file.xsd\">")
print("\t<!-- Routes -->")

ctr = 0
while ctr<len(lines):
    line = lines[ctr]
    if line.startswith("<vehicle id=\""):
        route_id = line.split("\"")[1]
        ctr+=1
        line = lines[ctr]
        route_edges = line.split("\"")[1]
        ctr+=1
        print("\t<route id=\""+route_id+"\" edges=\""+route_edges+"\"/>")
    else:
        ctr+=1
print("\n")
print("\t<!-- Define Vehicles or Flows in the following -->")


# Generate flows
ctr = 0
while ctr<len(lines):
    line = lines[ctr]
    if line.startswith("<vehicle id=\""):
        route_id = line.split("\"")[1]
        ctr+=1
        line = lines[ctr]
        route_edges = line.split("\"")[1]
        ctr+=1
        print("\t<flow id=\"flow_"+route_id+"\" type=\""+VEHICLE_TYPE+"\" begin=\""+str(FROM_TIME)+"\" end=\""+str(TO_TIME)+"\" probability=\""+str(FLOW_PER_HOUR/3600)+"\" route=\""+route_id+"\">	</flow>")
    else:
        ctr+=1
        
print("</routes>")