# Project Deliverables for "Microscopic Modelling and Simulation of Traffic operations HS2024"

During this course, you will apply what you have learned during the lessons in a "hands-on" project. In the project you should use microscopic traffic simulations to investigate how to solve a problem for a given case study of your choice. Think of two to three scenarios (solutions) to your problem, and use simulations to analyse the current state, and the state  in the scenarios.

By the end of this course, you will need to prepare a final presentation and project deliverables, these consist of the following, and are outlined into more detail in the following:

1. Project Documentation
    1. Interim Presentation (10 minutes long)
    2. Final Presentation (20 minutes long)
    3. Final Report (5-10 pages)
2. Project Work Result

On this page you will find detailed instructions what you need to prepare.
A template can be found in this folder as well `project-template-empty.zip` and an example folder of a study of mine and a master thesis student `project-example-esslingen`.

# 1. Project Documentation
## i) Iterim Presentations

The interim presentation should include a 10 minutes long presentation, with answers to the following questions:

- What case study map did you choose and why? (e.g. personal connection to your home town)
- What problems are there in this case study map (e.g. always congestion at a specific time)
- What possible solutions / suggested changes / scenarios would you like to assess during your student project? 
- What aspects do you want to analyze for each scenario? (e.g. environmental impact, experienced delays, traffic congestion, etc.)


## ii) Final Presentation

The final presentation should be a summary of your final report, feel free to choose a structure you prefer and fits your presentation style. Make sure to converse on following points:

- Quick summary of the case study & problem you selected (summary of interim presentation)
- Overview of your model and different scenarios that you analysed during the project
- Presentation of the results & final recommendation what you would do to solve the problem (which scenario helps most)
- Conclusion (limitations of the models, future work)

Highly appreciated: create some appealing visualizations (e.g., GIF animations, or videos) ;-)

## iii) Final Report

The final report should be between 5 to 10 pages (including text, tables and / or illustrations).
The report should follow following format requirements:
- LaTex / Microsoft Word / PDF (you can use either tool, be creative)
- Page Size: DIN A4
- Page Margins: Top 2.5cm, Bottom 2cm, Left 2.5cm, Right 2.5cm
- Font Size: 12pt, Arial (headings / titles / subtitles can be 15pt)

The report should follow this structure:
- Introduction
  - Case study, problem, motivation of this project, exact goal of the simulation study
- Model & Scenarios
  - Simulation model
    - what discrete simulation time step you choose
    - whether you simulate a specific situation (e.g., one hour peak-time, or a simulation over the whole day with varying demand)
    - whether your simulation is based on sumo itself or also includes TRACI
    - what output log files are generated from your simulation
    - how you process these log files to analyse the results (e.g., delay distribution, emission heatmap, MFD, space-time-diagram, space-time-heatmap, your own code)
  - Network model
    - illustration of the network map used
    - explanations where you got it from (e.g., self designed, open-street-map, or others)
    - defined inputs and outputs to the networks
    - table with numbers about possible routes through the network (for each input, how many routes start there, for each output, how many routes end there)
  - Demand model
    - outline how you researched data about the demand model, what sources you found, what assumptions you made
    - explanations / numbers about which vehicle types you simulate (what types, and how much percent of the vehicle population, how many vehicles)
    - outline how you estimated the O-D-Matrix
  - Scenario model
    - what specific, distinct scenarios do you explore  
- Results
  - Discuss your results based on your simulation outcomes, specific to your research questions, goals, and scenarios
  - Can you give a final recommendation / conclusion what scenario probably best solves your problem?
- Conclusions 
  - Does the model give sufficient guidance to make a decision for your case study problem?
  - What are the limitations of your simulation?
  - What could be done in future work to improve / extend the simulation further (given more time, data, etc.)?
- Appendix: Self-Reflection (not graded, can also be submitted anonymously, honest feedback appreciated)
  - What have you learned from the course that you use for your future?
  - What you found most and least useful about the course?
  - What you missed in the course but would like to have learned?
  - Any other feedback and suggestions to improve the course?

# 2. Project Work Result

The project work result should be a GitHub repository or ZIP file, that includes following files

*Notes: Each item ending with "/" should be a folder with more information. Depending on how many scenarios you have you need to create less or more scenario folders. scenario_1 should be the current situation (without any changes to the problem).*

```
project-root/
├── README.md
├── demand_model_data/
│   ├── researched_data/
│   │   ├── vehicle_type_distribution/
│   │   └── demand_data/
│   ├── entrance_and_exit_definitions/
│   ├── route_definitions/
│   └── od_matrix_estimation/
├── simulation_models/
│   ├── scenario_1_model/
│   │   ├── Configuration.sumocfg
│   │   ├── Network.net.xml
│   │   ├── Demand.xml
│   │   ├── RunSimulation.py (if you work wiht TRACI)
│   │   └── AdditionalFiles.xml (if any)
│   ├── scenario_2_model/
│   │   ├── Configuration.sumocfg
│   │   ├── Network.net.xml
│   │   ├── Demand.xml
│   │   ├── RunSimulation.py (if you work wiht TRACI)
│   │   └── AdditionalFiles.xml (if any)
│   └── scenario_3_model/
│       ├── Configuration.sumocfg
│       ├── Network.net.xml
│       ├── Demand.xml
│       ├── RunSimulation.py (if you work wiht TRACI)
│       └── AdditionalFiles.xml (if any)
├── simulation_output/
└── simulation_analysis/
```

The **README.md** should include explanations on how to run your simulatons, and how your parsed the outputs of the simulation.

In the folder **demand_model_data/**, you can provide data that you found / used when researching for numbers on vehicle types and demand in the subfolder **researched_data/**. Don't forget to provide links where you found these informations (usually in tabular form such as XML, Excel-XLSX, or CSV).
In subfolder **entrance_and_exit_definitions/** please provide a list of all entrances and exits to your network, that you want to use during your simulation.
In subfolder **route_definitions/** please provide a list of all routes that are possible between the defined entrances and exits.
In subfolder **od_matrix_estimation/** please provide code and data to calculate your final OD-Matrix estimation. In case you did not calculate, but just defined it, please provide data and explanations about this here.

For each scenario in **simulation_models/**, you need to provide at least a `Configuration.sumocfg`, `Network.net.xml`, `Demand.xml`. In addition to that, you can provide `RunSimulation.py` and `AdditionalFiles.xml` depending on whether you used it. Make sure that your simulations provide some form of log files, that you can then use to analyse in your **simulation_analysis/**.

The outcome of your simulation (log files) can be stored in **simulation_output/** folder. The log files might be too large to share, try to compress them, otherwise do not include them into your final submission, and rather provide a short version of them to outline the file structure of these logfiles.

The folder **simulation_analysis/** shall contain code, data, or further explanations on how you analysed the outcomes of your simulation (log files).
