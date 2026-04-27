# Tennis Ball Tracker ESD : Capstone Project
FPGA-oriented tennis ball tracker using stereo vision and MATLAB–Blender simulation to estimate 3D ball position, evaluate accuracy under motion, compute coefficient of restitution, and perform in/out detection with visualization.

**NOTE** : This directory is *technically* not a comprehensive directory of everything developed for the project. There are some branches of the repository that were left stale as a means to go back to certain testing or development steps. This was done as a precaution in case we needed to fix data from previous runs, but had lost the ability to for some reason during development.  This directory is the **main** branch but there are three others that were left stale...
- python_editing
- snickerdoodle-integration
- wind-sim-commit
These three branches each served a purpose in our development cycle, but as changes were made and code was refactored, they were left stale and to be used as backups
## Group Members
---
Kaishaun Nicholas (kan6526@rit.edu)

Befekir Belayneh (bdb4290@rit.edu)

Gerald Lynch (gal9036@rit.edu)

Talitha Sutton (tks8012@rit.edu)

Areeb Majid (atm8256@rit.edu)

Jeff Taylor (jet2898@rit.edu)

## Whats in this folder
---
Within this project directory there are a number of miscellaneous files, primary sub directories are...

Documentation
Includes documentation files, including how to use Git, the assignment pdf, and CDR PDR presentation and associated documentation

Example Files
Files pulled from the ESD : Capstone myCourses page as examples to use for stereo imaging, image filtering, and assisting with FPGA development

misc
Miscellaneous files fall into a few subdirectories...
	Labs
	The preliminary labs done in the first quarter of the course, used as a baseline for stereo imaging and tennis ball tracking. 
	Captures
	The captures folder is a temp folder designed to hold the images captured from the Labs, and subsequent development of the tennis ball tracker
	Class Notes
	Notes taken in class during the first half of the semester up to week 6

# "Final" folder
The final folder is where the true project sits. Inside there are several sub directories and a number of data collection files. Different python files, different testing matlab files, and different user interfaces depending on the use case.

To go over some of these files...
## snickerdoodleIntegration
This is where all the snickerdoodle integration code provided by Kaishaun Nicholas (kan6526@rit.edu) and Befekir Belayneh (bdb4290@rit.edu) sits, this code integrates the snickerdoodle board with python and the MatLab blender link developed. 

### Triangulation_results_{data}
The triangulation results files are the test results generated from analyzing the .dat files provided. Each .dat file was simulated, and results including actual ball location, calculated ball location, error value, and percent error were saved to these excel sheets.

## captures
Here is where the thousands of images saved per run were left after each simulation or run of the snickerdoodle. The captures folder was NOT for use in the code, and was used primarily for identifying key issues and point of failure. No code should have ever looked into the captures folder except to save an image to it.

## image analysis capture
Here are some of the images captured and saved for either later analysis or temporary current analysis. Including analysis on images from the captures folder to identify error causes. 2 Dimensional error cloud images can be seen here, as well as preliminary graphs that were not used in the final product presentation, as the data scope is too small. 

### GUI.mlapp
The GUI.mlapp is the final project GUI used, which holds the run blender function, and connect to snickerdoodle function. This GUI calculates the ball location, updates live, and includes an LED "Lamp" visualization, note that the physical LED will likely be more accurate as the "Lamp" LED was a later addition. 

### simulation_gui.mlapp
This GUI is an older GUI used exclusively to simulate the Snickerdoodle board via matlab functions. The outcome is the same, or largely same as when the system is run with the snickerdoodle board. This GUI is leftover so that Jeff Taylor (jet2898@rit.edu) can run system accuracy tests even when the snickerdoodle board is in use.