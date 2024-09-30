# Microscopic Modelling and Simulation of Traffic Operations 
## [ETH-Course-ID 101-0492-00L]
## Kevin Riehl [ETH Zürich, Institute for Transportation Planning and Systems IVT, Traffic Engineering Group SVT]

## Lecture 06: Environmental Impact Assessment

### One example project
This folder contains one exemplary sumo simulation.

- sumo_example_emissions

### Excercises

**First Task: Introduction** 
1. Run the simulation `sumo_example_emissions` with `SUMO-GUI`.
2. Have a look on the generated file `Output_Emissions.xml`.
3. Visualize the CO2 emissions in a heatmap using the Python Script `Python_Parser.py` (you can run the script with your Python IDE `Spyder`).
4. Have a look on the steps of the Python Script. Try to understand the structure of the tables `emission_info` and `emission_info_agg`. What is their difference?

**Second Task: Your Own Impact** 
1. Use your own network.
2. Modify your Configuration file so that the simulation logs the emission relevant information.
3. Use the Python Script from `sumo_example_emissions` to visualize a heatmap of your emissions.
4. Can you display other emissions than just CO2? Are they similar to CO2 heatmap, or different?

**Third Task: Your Project**
1. Are environmental impact assessments such as emissions or noise relevant to your project?
2. Think of research questions related to environmental impact and include them into your project.

**Have seen enough already?**
- Feel free to work on your project / case study.
- Feel free to read the documentation of SUMO, checkout some tutorials, or help your colleagues solve their issues.