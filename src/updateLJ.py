import numpy as np

# setting up parameters
mlcName = "Helium"
mlcMW = 6.646 * 10**-27 # kg
mlcRadius = 3.1 * 10**(-11) # m
N = 1500 # number of particles
temperature = 373 # K (shifts overtime, defined here as source of initial kinetic energy)
boundaryLength = 10**(-9) # m
boltzmannConstant = 1.38 * 10**-23 # J/K

# LJ Potential parameters
epsilon = 10.2 * boltzmannConstant
sigma = 2 * mlcRadius

# initialize current random position, current velocity matrix, v_rms, and dt
def initSys(N, temperature, mlcMW, boundaryLength):

    # setting up initial positions in a grid layout
    # preventing overlapping placed particle
    particlePerSide = int(np.ceil(N**(1/3)))
    particleDistance = boundaryLength / particlePerSide

    if particleDistance < 2 * mlcRadius: # checking whether the box is large enough
        print("Overcrowded, box is too small.")
        return

    curPosMat = np.zeros((N, 3))
    placingCount = 0

    # placing particle
    for x in range(particlePerSide):
        for y in range(particlePerSide):
            for z in range(particlePerSide):
                if placingCount >= N: break

                curPosMat[placingCount] = np.array([
                    x*particleDistance + particleDistance/2,
                    y*particleDistance + particleDistance/2,
                    z*particleDistance + particleDistance/2
                    ])
                
                # adding tiny randomness
                curPosMat[placingCount] += np.random.uniform(-particleDistance/10, -particleDistance/10, 3)
                placingCount += 1
            if placingCount >= N: break
        if placingCount >= N: break

    # setting up initial velocities
    curVelMat = np.random.uniform(-1, 1, (N, 3))

    # scaling velocities to temperature parameter
    Vsqaure = np.sum(curVelMat**2, axis = 1)
    totKE = mlcMW * np.sum(Vsqaure) / 2
    avgKE = totKE/N
    currentTemp = (2/3) * (avgKE/boltzmannConstant)
    scalingFactor = np.sqrt(temperature/currentTemp)

    curVelMat = curVelMat * scalingFactor

    # setting up v_rms
    vRMS = np.sqrt(3 * boltzmannConstant * temperature / mlcMW)

    # setting up safe dt for calculation, avoiding tunneling
    maxV = np.max(np.linalg.norm(curVelMat, axis=1))
    dt = (mlcRadius / maxV) * 0.2

    return curPosMat, curVelMat, vRMS, dt

# Calculating F(t), a(t) from the LJ Potential
def LJ(curPosMat):
    # finding r, r vector
    collisionAxisVec = curPosMat[:, np.newaxis, :] - curPosMat[np.newaxis, :, :]
    r = np.linalg.norm(collisionAxisVec, axis = 2)

    # prevent self interaction
    np.fill_diagonal(r, np.inf)

    # prevent particles being to close and cause speed exceeding light
    r = np.clip(r, sigma * 0.8, None)

    # calculating force, acceleration
    curForceMagnitude = ((24*epsilon)/r**2) * (2*(sigma/r)**12 - (sigma/r)**6)
    curForceMat = curForceMagnitude[:, :, np.newaxis] * collisionAxisVec
    curAccMat = np.sum(curForceMat, axis = 1)/mlcMW

    return curAccMat

def velVerlet(curPosMat, curVelMat, curAccMat, dt, boundaryLength):
    
    # Velocity Verlet Algorithm 1
    nextPosMat = curPosMat + curVelMat*dt + (curAccMat * dt**2)/2

    # correcting wall collision before calculating next velocity
    lowerWall = nextPosMat < 0
    nextPosMat[lowerWall] = -nextPosMat[lowerWall]
    curVelMat[lowerWall] *= -1

    upperWall = nextPosMat > boundaryLength
    nextPosMat[upperWall] = 2*boundaryLength - nextPosMat[upperWall]
    curVelMat[upperWall] *= -1

    # Velocity Verlet Algorithm 2
    nextAccMat = LJ(nextPosMat)
    nextVelMat = curVelMat + (curAccMat + nextAccMat)*dt*(1/2)

    return nextPosMat, nextVelMat, nextAccMat