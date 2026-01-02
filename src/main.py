import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from sklearn.metrics import mean_squared_error

import updateHardSphere as HS
import updateLJ as LJ

# setting up simulation configuration
transientStep = 700
sampleCount = 50
sampleStep = 50

def histCubicSplineFit(velocityMatHS, velocityMatLJ, stabilizedT):

    speedHS = np.linalg.norm(velocityMatHS, axis = 1)
    speedLJ = np.linalg.norm(velocityMatLJ, axis = 1)

    # setting up plotting domain
    maxV = max(np.max(speedHS), np.max(speedLJ))
    vAxis = np.linspace(0, maxV*1.2, 200)

    # Fitting Hard-Sphere Simulation
    countsHS, binEdgesHS = np.histogram(speedHS, bins = 50, density = True)
    binCentersHS = (binEdgesHS[:-1] + binEdgesHS[1:]) /2
    yObservedHS = countsHS

    cubicSplineFuncHS = CubicSpline(binCentersHS, yObservedHS)
    yhatHS = cubicSplineFuncHS(vAxis)

    # clipping out of bound
    yhatHS[vAxis < np.min(speedHS)] = 0
    yhatHS[vAxis > np.max(speedHS)] = 0
    yhatHS[yhatHS < 0] = 0


    # Fitting Lennard-Jones Simulation
    countsLJ, binEdgeLJ = np.histogram(speedLJ, bins = 50, density = True)
    binCentersLJ = (binEdgeLJ[:-1] + binEdgeLJ[1:]) /2
    yObservedLJ = countsLJ

    cubicSplineFuncLJ = CubicSpline(binCentersLJ, yObservedLJ)
    yhatLJ = cubicSplineFuncLJ(vAxis)

    # clipping out of bound
    yhatLJ[vAxis < np.min(speedLJ)] = 0
    yhatLJ[vAxis > np.max(speedLJ)] = 0
    yhatLJ[yhatLJ < 0] = 0

    # Theoretical PDF defined in updateHardSphere
    yTheory = HS.maxwellBoltzmannPDF(vAxis, HS.mlcMW, stabilizedT)

    # Calculating MSE for both simulation
    mseHS = mean_squared_error(yTheory, yhatHS)
    mseLJ = mean_squared_error(yTheory, yhatLJ)

    # Residual of both comparing to Theoretical PDF
    residualsHS = yhatHS - yTheory
    residualsLJ = yhatLJ - yTheory

    print(f"---------------------------\nHard-Sphere Simlation MSE = {mseHS}\nLennard-Jones Simulation MSE = {mseLJ}\n---------------------------\n")

    # plotting section

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]})

    ax1.hist(speedLJ, bins=50, density=True, alpha=0.3, color="gray", label="Raw Simulation Data (LJ)")
    ax1.plot(vAxis, yTheory, "b--", linewidth=2, alpha=0.8, label="Theoretical Distribution")
    ax1.plot(vAxis, yhatHS, "g-", linewidth=2.5, alpha=0.7, label="Hard Sphere Spline")
    ax1.plot(vAxis, yhatLJ, "r-", linewidth=2.5, alpha=0.7, label="Lennard-Jones Spline")
    ax1.scatter(binCentersLJ, yObservedLJ, color="black", s=10, marker="x", alpha=0.6, label="Histogram Bin Centers (LJ)")

    ax1.set_ylabel("Probability Density")
    ax1.set_title(f"Maxwell-Boltzmann: Hard Sphere vs LJ Spline Interpolation")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.scatter(vAxis, residualsHS, color="green", s=10, alpha=0.5, label="HS Residuals")
    ax2.scatter(vAxis, residualsLJ, color="crimson", s=10, alpha=0.5, label="LJ Residuals")
    ax2.axhline(0, color="black", linestyle="--", linewidth=1)
    
    maxResidAbs = max(np.max(np.abs(residualsHS)), np.max(np.abs(residualsLJ)))
    ax2.set_ylim(-maxResidAbs * 1.1, maxResidAbs * 1.1)

    # ax2.set_ylim(minRes * 1.5, maxRes * 1.5)
    ax2.set_ylabel("Residuals")
    ax2.set_xlabel("Speed [m/s]")
    ax2.set_title("Residual Plot (Spline and Theory)")
    ax2.legend(loc = "upper right", fontsize = "small")
    ax2.grid(True, alpha = 0.3)

    plt.tight_layout()
    plt.show()

def main():

    # Lennard-Jones simulation
    pos, vel, vRMSinit, dt = LJ.initSys(LJ.N, LJ.temperature, LJ.mlcMW, LJ.boundaryLength)
    acc = LJ.LJ(pos)
    sampleLJ = []

    for i in range(transientStep):
        pos, vel, acc = LJ.velVerlet(pos, vel, acc, dt, LJ.boundaryLength)

    for i in range(sampleCount):
        for j in range(sampleStep):
            pos, vel, acc = LJ.velVerlet(pos, vel, acc, dt, LJ.boundaryLength)
        sampleLJ.append(vel.copy())
    
    stackedLJ = np.vstack(sampleLJ)

    # Calculating temperature at new stabilized state of LJ simulation
    speedsLJ = np.linalg.norm(stackedLJ, axis=1)
    vRMSsquare = np.mean(speedsLJ**2)
    
    stabilizedT = LJ.temperature * (vRMSsquare/(vRMSinit**2))

    print(f"---------------------------\nSystem Shifted to New Stabilized T: {LJ.temperature} K -> {stabilizedT} K\n---------------------------\n")

    # Hard-Sphere simulation at new stabilizedT
    pos, vel, vRMS, dt = HS.initSys(HS.N, stabilizedT, HS.mlcMW, HS.boundaryLength)
    sampleHS = []

    for i in range(transientStep):
        pos, vel = HS.update(pos, vel, dt, HS.boundaryLength, HS.mlcRadius)
    
    for i in range(sampleCount):
        for j in range(sampleStep):
            pos, vel = HS.update(pos, vel, dt, HS.boundaryLength, HS.mlcRadius)
        sampleHS.append(vel.copy())
    
    stackedHS = np.vstack(sampleHS)

    # plotting graph at new stabilizedT
    histCubicSplineFit(stackedHS, stackedLJ, stabilizedT)

if __name__ == "__main__":
    main()