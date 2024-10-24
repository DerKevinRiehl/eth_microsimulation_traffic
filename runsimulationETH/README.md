

### Installation Instructions

1. Launch your `Anaconda Prompt`.
2. Type following command: `conda create -y --name sumo_env python==3.9`
3. Type following command: `conda activate sumo_env`
4. Type following command: `pip install --upgrade pip`
5. Type following command: `pip install eclipse-sumo traci`
6. Type following command: `pip install Pillow==9.4.0`
7. Type following command: `conda env list` and see where you python is stored
7. Launch your IDE (Integrated Development Environment) `Spyder`.
8. In Spyder, Go to "Tools" -> "Preferences" -> "Python Interpreter" -> "Use the following Python Interpreter" and navigate to your installed environment, e.g. `C:/Users/kriehl/.conda/envs/sumo_env/python.exe
9. Press `Apply` and `OK`.
10. Open a Python Script from the GitHub.
11. Change `sumoBinary = "C:/APPS/Sumo/sumo-1.20.0/bin/sumo-gui.exe` to where your sumo is installed. (should be this path on ETH machines)
12. Click Run to start the simulation.
