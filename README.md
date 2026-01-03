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
### The Maxwell-Boltzmann Distribution
To statistically validate that a molecular dynamic simulation is accurate, the distribution of particle speeds from the simulation is compared against the theoretical *Maxwell-Boltzmann Distribution*. For an ideal gas at thermodynamic equilibrium, the speeds of particles are not uniform. Instead, they follow a specific probability distribution known as **Maxwell-Boltzmann PDF**.

The probability density function $f(v)$ for a particle of mass $m$ at temperature $T$ is given by:

$$
f(v)=4\pi \left( \frac{m}{2\pi k_B T} \right)^{3/2} v^2 \exp\left(-\frac{mv^2}{2k_B T}\right)
$$

### The Hard-Sphere Model
The Hard-Sphere model describes a system of particles that interact only through perfect collisions. As demonstrated in my [previous work](https://github.com/youMetTem/NumericalMBPDFreconSimulation). The interaction potential $V(r)$ is discontinous:

$$
V_{Hard-Sphere}(r) =
\begin{cases}
\infty, & r < 2R \\
0, & r \ge 2R
\end{cases}
$$

Where $2R$ is the diameter of the particle and $r$ is the distance between particle centers. Due to the discontinuity in interaction potential, particles simulated from this model will move with constant velocity in straight lines between collisions.

This model only accounts for repulsive forces, lacking the intermolecular attractive component which could be observed in real-world particles. Consequently, it cannot simulate nano cluster or droplet formation upon decreases in temperature.


### The Lennard-Jones Potential
In order to simulate realistic thermal properties and phase behavior, including the formation of nano cluster and droplets, this project utilize the Lennard-Jones (LJ) Potential. The LJ model introduces soft, continous interaction that accounts for both repulsion and attraction.

$$
V_{LJ}(r) = 4\epsilon \left[ \left( \frac{\sigma}{r} \right)^{12} - \left( \frac{\sigma}{r} \right)^6 \right]
$$

This potential is characterized by two terms:
1. Repulsion ($(\sigma/r)^{12}$): Modeling the Pauli exclusion principle.
2. Attraction ($(\sigma/r)^{6}$): Modeling long-range Van der Waals interaction.

With Modeling of Van der Waals interaction included in this project, it allow particles to bind together when their kinetic energy drops below the potential energy barrier. The enables 3D simulation of particle clustering and phases transitions.

Furthermore, this study aims to compare the the accuracy of speeds distribution data obtain from both *Hard-Sphere* and *Lennard-Jones Potential* model. By reconstruct the speeds distribution of both model with *Cubic Spline interpolation* and compare them with the the Maxwell-Boltzmann theoretical distribution.

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
