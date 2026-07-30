# URCap-2F-Python-Setup-and-Test
# UR5e and Robotiq Gripper Control with Python

## Project Overview

This project focused on establishing communication between a Universal Robots UR5e robotic arm and a Robotiq gripper using Python.

The main objectives were:

- Connect a PC to the UR5e robot.
- Control the Robotiq gripper through Python.
- Execute robot arm movements through programs running on the UR teach pendant.
- Investigate methods for detecting whether an object is being held by the gripper.
- Document installation challenges and their solutions.

---

## Hardware

- Universal Robots UR5e
- Robotiq Gripper
- Windows PC
- Ethernet connection

---

## Software

- Python 3.12.8
- Visual Studio Code
- ur_rtde
- Universal Robots PolyScope
- Windows PowerShell

---

## Project Structure

```text
project/
│
├── gripper_control.py
├── robotiq_preamble.py
├── README.md
└── Test.py
```

---

## Required Scripts

### gripper_control.py

Main script responsible for communicating with and controlling the Robotiq gripper.

Functions include:

- Connecting to the robot
- Activating the gripper
- Opening the gripper
- Closing the gripper
- Sending gripper movement commands

---

### robotiq_preamble.py

This file contains:

```python
ROBOTIQ_PREAMBLE
```

which provides the required URScript commands used to communicate with the Robotiq gripper.

The file must be available in the project directory.

Without it, Python produces an error similar to:

```python
ModuleNotFoundError: No module named 'robotiq_preamble'
```

---

## Installation

### Create a Virtual Environment

```powershell
py -3.12 -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\activate
```

Verify the Python version:

```powershell
python --version
```

Expected output:

```text
Python 3.12.8
```

---

### Install Dependencies

```powershell
pip install ur_rtde
```

---

## Robot Control Concept

### Robot Arm

The robot arm movement is executed through a program stored and run on the UR teach pendant.

Typical movement sequence:

```text
MoveJ
MoveL
MoveL
MoveJ
```

The robot follows its programmed trajectory independently of the Python application.

---

### Gripper Control

The Robotiq gripper is controlled through Python.

This allows:

- Robot motion to be managed by PolyScope.
- Gripper commands to be sent from a PC.
- Independent operation of arm and gripper.

Example workflow:

```text
UR Program
    ↓
Robot moves to waypoint

Python Program
    ↓
Gripper closes

UR Program
    ↓
Robot continues movement

Python Program
    ↓
Gripper opens
```

---

## Problems Encountered and Solutions

### Problem 1: CMake Error During ur_rtde Installation

#### Error

```text
Failed building wheel for ur_rtde
```

#### Initial Assumption

The error message suggested that CMake was missing.

#### Investigation

CMake was installed correctly, however the installation still failed.

#### Actual Cause

The package was attempting to build from source and required a complete C++ build environment.

#### Solution

Install:

- CMake
- Visual Studio Build Tools
- Desktop Development with C++
- MSVC Compiler
- Windows SDK

---

### Problem 2: Python 3.14 Was Still Being Used

#### Error

Build logs contained:

```text
pythoncore-3.14-64
```

and

```text
cpython-314
```

even after Python 3.12 had been installed.

#### Cause

VS Code was still using the previously installed Python 3.14 interpreter.

#### Solution

Create a new virtual environment explicitly using Python 3.12:

```powershell
py -3.12 -m venv .venv
```

Then select the correct interpreter in VS Code:

```text
Ctrl + Shift + P
Python: Select Interpreter
```

and choose:

```text
Python 3.12 (.venv)
```

---

### Problem 3: Missing C/C++ Compiler

#### Error

```text
CMAKE_C_COMPILER not set
CMAKE_CXX_COMPILER not set
```

#### Cause

No Microsoft C++ compiler was available on the system.

#### Solution

Install Visual Studio Build Tools with:

```text
Desktop Development with C++
```

including:

- MSVC Compiler
- Windows SDK
- CMake Tools

---

### Problem 4: Missing robotiq_preamble.py

#### Error

```python
from robotiq_preamble import ROBOTIQ_PREAMBLE
```

caused an import error.

#### Cause

The required file was not available within the project directory.

#### Solution

Add:

```text
robotiq_preamble.py
```

to the same folder as the main script.

---

## Investigation: Can Force Measurements Detect a Successful Grip?

### Objective

Determine whether the robot's force measurements can be used to identify if an object is being held by the Robotiq gripper.

---

### Approach

Several options were investigated:

- Reading TCP force values from the UR5e.
- Monitoring force data through RTDE.
- Comparing force values before and after grasping an object.

---

### Findings

The force information available through the UR controller represents forces measured at the robot's Tool Center Point (TCP).

These measurements are influenced by:

- Robot movement
- Acceleration and deceleration
- Tool orientation
- External disturbances
- Payload changes

During testing and analysis it became apparent that these force readings cannot reliably distinguish between:

```text
Object successfully grasped
```

and

```text
No object present
```

especially for small or lightweight objects.

---

### Conclusion

Using the UR5e force measurements alone is not a reliable method for determining whether the Robotiq gripper is holding an object.

The investigation concluded that grip detection through TCP force feedback is not feasible for this application.

More reliable alternatives would include:

- Gripper status information
- Built-in object detection features
- Additional sensors
- Vision systems

---

## Useful Commands

### Verify Python Version

```powershell
python --version
```

---

### Verify Pip

```powershell
pip --version
```

---

### Verify CMake

```powershell
cmake --version
```

---

### Verify C++ Compiler

```powershell
cl
```

Expected output:

```text
Microsoft (R) C/C++ Optimizing Compiler
```

---

## Program Termination

The following code was used for clean program shutdown:

```python
except KeyboardInterrupt:
    print("\nProgramm beendet.")
```

This catches the interrupt generated by:

```text
Ctrl + C
```

and prevents the program from terminating with a long exception traceback.

---

## Lessons Learned

- Always verify which Python interpreter is active in VS Code.
- Virtual environments simplify dependency management and troubleshooting.
- Installing `ur_rtde` on Windows may require additional C++ build tools.
- Arm movement and gripper control can be separated into independent systems.
- Import errors are often caused by missing local files rather than missing Python packages.
- TCP force measurements are not a reliable indicator of whether an object is currently being held by the gripper.

---

## Summary

The project successfully established a workflow in which the UR5e executes motion programs through the teach pendant while a Python application controls the Robotiq gripper independently. During development several installation and configuration issues were encountered, particularly concerning Python versions, CMake, and Visual Studio build tools. Additionally, an investigation into force-based grip detection showed that TCP force measurements cannot reliably determine whether an object is currently grasped, making alternative detection methods necessary.
