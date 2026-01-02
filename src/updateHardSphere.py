import numpy as np
from scipy.spatial.distance import pdist, squareform

# setting up parameters
mlcName = "Helium"
mlcMW = 6.646 * 10**-27 # kg
mlcRadius = 3.1 * 10**(-11) # m
N = 1500 # number of particles
boundaryLength = 10**(-9) # m
boltzmannConstant = 1.38 * 10**-23 # J/K

# initialize random position, velocity matrix, v_rms, and dt
def initSys(N, temperature, mlcMW, boundaryLength):

    # setting up initial positions in a grid layout
    # preventing overlapping placed particle
    particlePerSide = int(np.ceil(N**(1/3)))
    particleDistance = boundaryLength / particlePerSide

    if particleDistance < 2 * mlcRadius: # checking whether the box is large enough
        print("Overcrowded, box is too small.")
        return

    posMat = np.zeros((N, 3))
    placingCount = 0

    # placing particle
    for x in range(particlePerSide):
        for y in range(particlePerSide):
            for z in range(particlePerSide):
                if placingCount >= N: break

                posMat[placingCount] = np.array([
                    x*particleDistance + particleDistance/2,
                    y*particleDistance + particleDistance/2,
                    z*particleDistance + particleDistance/2
                    ])
                
                # adding tiny randomness
                posMat[placingCount] += np.random.uniform(-particleDistance/10, -particleDistance/10, 3)
                placingCount += 1
            if placingCount >= N: break
        if placingCount >= N: break

    # setting up initial velocities
    velocityMat = np.random.uniform(-1, 1, (N, 3))

    # scaling velocities to temperature parameter
    Vsqaure = np.sum(velocityMat**2, axis = 1)
    totKE = mlcMW * np.sum(Vsqaure) / 2
    avgKE = totKE/N
    currentTemp = (2/3) * (avgKE/boltzmannConstant)
    scalingFactor = np.sqrt(temperature/currentTemp)

    velocityMat = velocityMat * scalingFactor

    # setting up v_rms
    vRMS = np.sqrt(3 * boltzmannConstant * temperature / mlcMW)

    # setting up safe dt for calculation, avoiding tunneling
    maxV = np.max(np.linalg.norm(velocityMat, axis=1))
    dt = (mlcRadius / maxV) * 0.2

    return posMat, velocityMat, vRMS, dt

# theoretical maxwell-boltzmann PDF
def maxwellBoltzmannPDF(v, m, T,):
    A = (m / (2 * np.pi * boltzmannConstant * T))**(3/2)
    exponent = - (m * v**2) / (2 * boltzmannConstant * T)
    return 4 * np.pi * A * (v**2) * np.exp(exponent)

# update function, output the new positions and velocities matrix
def update(pos, velocity, dt, boundaryLength, mlcRadius):

    #update positions
    pos += velocity * dt

    # handle wall collisions
    leftCollide = pos[:, 0] < mlcRadius
    rightCollide = pos[:, 0] > (boundaryLength - mlcRadius)
    velocity[leftCollide | rightCollide, 0] *= -1

    bottomCollide = pos[:, 1] < mlcRadius
    topCollide = pos[:, 1] > (boundaryLength - mlcRadius)
    velocity[bottomCollide | topCollide, 1] *= -1

    frontCollide = pos[:, 2] < mlcRadius
    backCollide = pos[:, 2] > (boundaryLength - mlcRadius)
    velocity[frontCollide | backCollide, 2] *= -1

    # handle particle collisions
    distanceMat = squareform(pdist(pos))
    collidePair1, collidePair2 = np.where((distanceMat < 2 * mlcRadius))
    uniqueFilter = collidePair1 < collidePair2

    for i, j in zip(collidePair1[uniqueFilter], collidePair2[uniqueFilter]):
        relativePos = pos[i] - pos[j]
        relativeVelocity = velocity[i] - velocity[j]
        distanceSquare = np.sum(np.square(relativePos))

        # checking if particle is moving toward each other or not
        if np.dot(relativePos, relativeVelocity) < 0:
            deltaVelocity = relativePos * (np.dot(relativePos, relativeVelocity)/distanceSquare)

            velocity[i] -= deltaVelocity
            velocity[j] += deltaVelocity

    # prevent wall clipping (double check)
    pos[pos < mlcRadius] = mlcRadius
    pos[pos > boundaryLength - mlcRadius] = boundaryLength - mlcRadius
    
    return pos, velocity
