# Microscopic Modelling and Simulation of Traffic Operations 
## [ETH-Course-ID 101-0492-00L]
## Kevin Riehl [ETH Zürich, Institute for Transportation Planning and Systems IVT, Traffic Engineering Group SVT]

## Lecture 01: Introduction, General Information, Installing SUMO

Please follow the instructions based on your level of confidence in programming.

### Recommended Installation Instructions (For Beginners As Well)

1. **Step: Install Anaconda**

- Go to [https://www.anaconda.com/download](https://www.anaconda.com/download ) and download Anaconda Navigator.
- Follow the installation instructions.
- This is a full IDE (integrated development environment) that helps you to get started quickly with programming.
- Now install some further Python packages that we need for the software development in the following:
    - Search on your computer for the application `Anaconda-Prompt` and open it.
    - A terminal window / console opens, where you can write commands and execute them pressing enter.
    - Write following command to install the necessary python packages.

```
pip install --upgrade pip
pip install eclipse-sumo traci
pip install Pillow==9.4.0
```

- Validate the installation of the packages by typing:
```
pip list
```
- This should return a large list of all packages installed (in alphabetic order). Make sure that the packages "eclipse-sumo" and "traci" appear on your package list.

<br />
<br />

2. **Step: Install SUMO**

- Go to [https://eclipse.dev/sumo/](https://eclipse.dev/sumo/) and download the latest distribution of SUMO.
- Follow the installation instructions.
- This is the microsimulation software coming with further tools such as netedit.

<br />
<br />

3. **Step: Try to Test your Python Installation**

- Open your Anaconda Navigator Software.
- Search on your computer for the application `Spyder` and open it.
- In Spyder, you can run Python code, you could for example run this simple programme in your command line terminal (bottom right):

```
print("Hello and welcome to your very first Python programme...")
print("Please enter your name: ", end="")
name = input()
print("")
print("Nice to meet you "+name+" and wish you lots of success with programming...")
```

- This programme will print some statements on the console / terminal and ask you for your name.

<br />
<br />

4. **Step: Try to Test your SUMO Installation**

- Download [this repository from GitHub](https://github.com/DerKevinRiehl/eth_microsimulation_traffic/).
- Search on your computer for the application `SUMO-GUI` and open it.
- Open the simulation that you can find under: `eth_microsimulation_traffic/Lecture01/sumo_example_hello_world/Configuration.sumocfg`
- Click the "run" button and enjoy the simulation of traffic.
- Search on your computer for the application `Netedit` and open it.
- Draw some nice networks.
