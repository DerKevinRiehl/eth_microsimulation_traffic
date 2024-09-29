# Microscopic Modelling and Simulation of Traffic Operations 
## [ETH-Course-ID 101-0492-00L]
## Kevin Riehl [ETH Zürich, Institute for Transportation Planning and Systems IVT, Traffic Engineering Group SVT]

## Lecture 05: TRACI – Manipulate & Sense Simulation in Real-Time

### Four example projects
This folder contains four exemplary sumo simulations.

- sumo_example_traci_1_launch

- sumo_example_traci_1_onthego

- sumo_example_traci_2_retrieve

- sumo_example_traci_3_trafficlight

### Excercises

**First Task: Introduction** 
1. Launch your Python IDE `Spyder`.
2. Run each simulation by executing the Python script `RunSimulation.py` of every example.
3. Read the Python code and get familiar with how Python & TRACI can be used to control SUMO. 

**Second Task: Advanced Retrieval** 
1. Use the network from `sumo_example_traci_3_trafficlight`.
2. Modify the Python code, in order to create a list of all travel times of all vehicles that complete their route in simulation steps 600-700 seconds. (The first 600 seconds can be considered as warm-up time, to fill the network with vehicles.).
3. For the recorder travel times, calculate the distribution and statistical properties such as average, standard deviation, minimum and maximum. 

**Third Task: Custom Traffic Light Controller**

1. Use the network from `sumo_example_traci_3_trafficlight`.
2. Think of your own traffic light controller (it might include sensors, information about queue lengths, etc., or it could be a simple fixed cycle controller).
3. Implement your traffic light control.
4. Observe how your custom control performs over the preconfigured fixed-cycle controller.
5. Assess the travel time distribution before and after using your controller. Are you able to significantly improve the travel times?

**Have seen enough already?**
- Feel free to work on your project / case study.
- Feel free to read the documentation of SUMO, checkout some tutorials, or help your colleagues solve their issues.