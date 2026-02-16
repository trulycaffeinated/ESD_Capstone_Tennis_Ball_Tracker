# Tennis Ball Tracker ESD : Capstone Project
FPGA-oriented tennis ball tracker using stereo vision and MATLAB–Blender simulation to estimate 3D ball position, evaluate accuracy under motion, compute coefficient of restitution, and perform in/out detection with visualization.

We can do our demo in person or as a video or both. The in person demo will provide bonus points
## Preliminary Stuffs
---
Clone this repo using git. If  you don't have it, you can install it over the web or using WinGET
```powershell
winget install git.git
```

Then
```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

I would recommend creating a system environment variable for wherever you save this repository. So for me I made a system environment variable to "C:\Users\tjeff\blah\blah\ESD_Project" labelled ESD2
1. In powershell, cd to the place you want to place the git repo
   ``cd "C:\users\{your user}\documents\..."`` is an example
2. Download this repository / clone it via git 
   ``git clone {repo link}``
3. Windows -> "Edit the system environment variables" -> Environment variables
4. New -> Name your variable and copy the directory path as the value
5. Hit "OK"

Now with any edits you make, it should be pretty easy to commit and push up changes
## Project Description and Matlab Intro
---
Likely tasks...
- system architecture **(group) (PRD)**
- firmware (labs)
- software (labs)
- gui (labs) (LAB 2)
- algorithm development (labs)
- system integration (Everybody - everything coming together)
- system and subsystem testing **(Jeff preferably)**
- program management (cost & schedule) 
- risk assessment and mitigation 
- Documentation **(Jeff preferably)**

### 🎯 Core technical pieces
1. **Ball position accuracy (static camera)** – 15 pts  **(THIS IS *MOSTLY* LAB #1)**
    → How accurate is your 3D position estimate across X/Y/Z?
2. **Camera motion accuracy (static ball)** – 15 pts  
    → How bad does error get when the camera shifts (wind simulation)?
3. **Coefficient of restitution** – 10 pts  
    → Measure how “bouncy” the court is using physics + tracking.
4. **LED visualization** – 10 pts  
    → Green LED = in  
    → Red LED blinking at **10 Hz, 50% duty** = out
5. **Full tennis tracker demo** – 40 pts
    - Track **5 serves**
    - Track **5 volleys**
    - Show **instant replay**
    - GUI matters a LOT here
6. **Professionalism & documentation** – 10 pts
## Group Members
---
Jeff Taylor (jet2898@rit.edu)
