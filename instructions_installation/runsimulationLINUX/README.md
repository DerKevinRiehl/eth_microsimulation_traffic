

### Installation Instructions for Linux (Ubuntu)
(Tested for Ubuntu 22.04.5 LTS)


1. Launch your `Terminal`.
2. Type following command: `sudo apt-get update`
3. Type following command: `sudo apt-get install -y python3`
4. Type following command: `sudo apt-get install sumo sumo-tools sumo-doc`
5. Type following command: `sudo apt-get install python3-pip`
6. Install Anaconda by instructions on the website: https://docs.anaconda.com/anaconda/install/linux/ (I recommend downloading it and using the bash command. Note: Using venv should also work instead of conda.)
7. Type following command: `conda create -y --name sumo_env python==3.9`
8. Type following command: `conda activate sumo_env`
8. Type following command: `pip install --upgrade pip`
10. Type following command: `pip install eclipse-sumo traci`
11. Type following command: `pip install Pillow`
12. Type following command: `conda install spyder-kernels`
13. Type following command: `conda env list` and see where you python is stored
14. Launch your IDE (Integrated Development Environment). I use: `Spyder`.
15. In Spyder, Go to "Tools" -> "Preferences" -> "Python Interpreter" -> "Use the following Python Interpreter" and navigate to your installed environment, e.g. `/home/YOUR_USER/anaconda3/envs/spyder-env/bin/python`
16. Press `Apply` and `OK`.
17. Open a Python Script from the GitHub.
18. Change `sumoBinary = "sumo-gui"` to where your sumo is installed. (should be this path on Ubuntu machines)
19. Click Run to start the simulation.


If you decide to run the simulation from SUMO directly, then open the SUMO software (should be installed in your application overview) and open the simulation file from the GitHub (File > Open Simulation > _find document_). Click on the play button to start the simulation.