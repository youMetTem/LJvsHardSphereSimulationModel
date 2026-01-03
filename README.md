# Comparison of Lennard-Jones Potential and Hard-Sphere Models: Equilibrium Velocity Distributions and Thermal Properties
The project extends my previous work, [Numerical Reconstruction of the Maxwell-Boltzmann Distribution via a 3D Monatomic Hard-Sphere Simulation](https://github.com/youMetTem/NumericalMBPDFreconSimulation), by replacing the hard-sphere interaction with Lennard-Jones potential. Both model of hard-sphere and Lennard-Jones potential are compared by evaluating how well each reproduce the theoretical Maxwell-Boltzmann velocity distribution.

Furthermore, to highlight the strengths and limitations of each motion model, this project also explores their thermal response to rapid temperature reduction (quenching). By visualizing 3D particle dynamics and observe how each model react as the temperature decreases.

<table>
  <tr>
    <td width="60%" align="center" valign="middle">
      <img src="assets/forProjectOverview/02_fittedTemperature.png" width="100%" alt = "02_fittedTemperature.png"/>
    </td>
    <td width="40%" align="center" valign="middle">
      <img src="assets/forProjectOverview/visTempChangeLJ3DSpeed.gif" width="100%" alt = "GenericFunctionCurveFitted"/>
    </td>
  </tr>
</table>

## Table of Contents
1. [Project Overview](#comparison-of-lennard-jones-potential-and-hard-sphere-models-equilibrium-velocity-distributions-and-thermal-properties)
2. [Theoretical Background](#theoretical-background)
3. [Methodology](#methodology)
4. [Results](#results)
5. [Conclusion](#conclusion)
6. [Installation & Usage](#installation--usage)
7. [Acknowledgements & Resources](#acknowledgements--resources)
8. [AI Use Declaration](#ai-use-declaration)

## Theoretical Background
in process ...

## Methodology
in process ...

## Results
in process ...

## Conclusion
in process ...

## Installation & Usage
### 1. Prerequisites & Setup
First, ensure you have Python 3.x installed. For window OS replace `python3` with `python`.

Clone repository:
```bash
git clone https://github.com/youMetTem/LJvsHardSphereSimulationModel.git
cd LJvsHardSphereSimulationModel
```

Install requirements:
```bash
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

### 2. Running Simulation and Comparative Analysis (`main.py`)
By default, the simulation models 70 Argon molecules at initial temperature of 1073 K confined within a cubic box of side length $2.2 \times 10^{-9}$ m. There parameters can be modified in the `main.py`, `updateHardSphere.py`, `updateLJ.py` files.

Run the script:
```bash
python3 src/main.py
```

This will run the simulation with Lennard-Jones potential model with initial kinetic energy corresponding to 373 K for 700 iterations. After equilibration, 50 samples are collected every 50 iteration to compute a new equilibrium temperature. The simulation is then rerun at this temperature using the Hard-Sphere model. Distribution and residual plots compare both models to the theoretical curve, and the MSE for each model will be reported in the matplotlib window and terminal, respectively.

### 3. Running the 3D Simulation Visualizations
This project provides 3 simulation visualization models:
#### Visualization of the Lennard–Jones potential model without external interference.

```bash
python3 src/visLJ3DconstTemp.py
```

#### Visualization of the hard-sphere model’s response to rapid temperature decreases.

```bash
python3 src/visTempChangeHardSphere3D.py
```

#### Visualization of the Lennard–Jones model’s response to rapid temperature decreases.

```bash
python3 src/visTempChangeLJ3D.py
```
A local web server will start, and your default web browser will automatically open a new tab to display the 3D animation.


#### 3D Simulation Controls (MacOS/Trackpad)
Once the browser window opens, you can navigate the 3D space using these trackpad gestures:

| Action | Trackpad Gesture | Keyboard Alternative |
| :--- | :--- | :--- |
| **Rotate View** | **Two-finger Click** & Drag | Hold **Ctrl** + Click & Drag |
| **Zoom In/Out** | **Two-finger Swipe** (Up/Down) | Hold **Option (Alt)** + Click & Drag |
| **Pan (Move)** | Hold **Shift** + Click & Drag | -- |

Note: For more details on camera control, refer to the official [VPython Documentation](https://www.glowscript.org/docs/VPythonDocs/index.html#).



## Acknowledgements & Resources
This project was inspired by several excellent resources. Special thanks to the following creators, authors for their high quality educational content:
* **Physics for Scientists and Engineers (Serway & Jewett)** - Primary reference for the Kinetic Theory of Gases and Maxwell-Boltzmann derivation.
* **[Molecular interaction and the Lennard-Jones potential](https://youtu.be/Yqj5jHUE3wI?si=RdwNpKF5yMZtr6Yk)** by *Prof. John Holman* - Explanation on the working principle of "Lennard-Jones potential".
* **[Velocity Verlet Algorithm - Solving equations of motion | Molecular Dynamics](https://www.youtube.com/watch?v=qT8pxV53FA4&t=500s)** by *LearnWithVinay* - Providing theoretical flowchart of the *Velcolity Verlet Algorithm*
* **[Numerical Methods for Engineers](https://youtube.com/playlist?list=PLkZjai-2Jcxn35XnijUtqqEg0Wi5Sn8ab&si=NUFmcl7sFmRZM9Wr)** by *Prof. Jeffrey Chasnov* - Provided the concept of numerical matrix operation and cubic spline interpolation.
* **[EGME206 Numerical Methods for Engineers, Spring 2021](https://youtube.com/playlist?list=PLLM1AZpDbYI1HPhHWmA-_5YqF26Rnt9ZM&si=xaMQ15EgJC063XTu)** by *Prof. Ittichote Chuckpaiwong* - In-dept explanation in the topic of Regressions.
* **[VPython for Beginners](https://youtube.com/playlist?list=PLdCdV2GBGyXOnMaPS1BgO7IOU_00ApuMo&si=8MC25WVnnu3wRcem)** by *Let's Code Physics* - Introduce the usage of `VPython` for 3D simulation.



## AI Use Declaration
This project utilized AI tools to assits in the development process and text refinement.
* **GitHub Copilot:** Used for code autocompletion, debugging scripts, and snipped generation.
* **Google Gemini:** Used for mundane snipped code generation, drafting the initial structure of this README file, text refinement, and documentation formatting.

All scientific logics, mathematical derivations, and final code implementation were verified and reviewed by me.
