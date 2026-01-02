from vpython import *
import numpy as np
import colorsys

import updateLJ as LJ

# Setting up configuration, Argon
N = 70
initT = 1073 # K
mlcMW = 6.63 * 10**(-26) # kg
boundaryLength = 2.2*10**(-9) # m
mlcRadius = 1.7 * 10**(-10) # m
dt = 5.5 * 10**(-15)
boltzmannConstant = 1.38 * 10**-23 # J/K

# LJ Potential parameters
epsilon = 120 * boltzmannConstant
sigma = 3.4 * 10**(-10)

# setting up dynamic coloring
def getSpectrumColor(speed, vRMS):
    normalized = speed/(2.5*vRMS)
    if normalized > 1: normalized = 1

    hue = 0.7 * (normalized)
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    return vector(r, g, b)

# simulation
def LJ3DSimul():
    pos, vel, vRMS, n = LJ.initSys(N, initT, mlcMW, boundaryLength)
    acc = LJ.LJ(pos)

    # setting up scene
    scene.width = 800
    scene.height = 600
    scene.title = "Lennard-Jones Simulation Over Decreasing Temperature"
    scene.center = vector(boundaryLength/2, boundaryLength/2, boundaryLength/2)
    scene.range = boundaryLength * 1.5
    scene.autoscale = False

    # setting up box frame
    curve(pos=[
        vector(0,0,0), vector(boundaryLength,0,0), vector(boundaryLength,boundaryLength,0), vector(0,boundaryLength,0), vector(0,0,0),
        vector(0,0,boundaryLength), vector(boundaryLength,0,boundaryLength), vector(boundaryLength,boundaryLength,boundaryLength), vector(0,boundaryLength,boundaryLength), vector(0,0,boundaryLength),
        vector(boundaryLength,0,boundaryLength), vector(boundaryLength,0,0), vector(boundaryLength,boundaryLength,0), vector(boundaryLength,boundaryLength,boundaryLength), vector(0,boundaryLength,boundaryLength), vector(0,boundaryLength,0)
    ], color = color.white, radius = boundaryLength*0.005)

    # setting up particles
    particles = []
    for i in range(N):
        particle = sphere(pos = vector(pos[i, 0], pos[i, 1], pos[i, 2]), radius = mlcRadius)
        particles.append(particle)

    temp_label = wtext(text = f"Temperature: {initT} K")

    running = True
    
    while running:
        rate(300)

        pos, vel, acc = LJ.velVerlet(pos, vel, acc, dt, boundaryLength)

        # double check to keep particles inside the box
        for i in range(3):
            under = pos[:, i] < sigma/2
            pos[under, i] = sigma/2
            vel[under, i] *= -1

            over = pos[:,i] > (boundaryLength - sigma/2)
            pos[over, i] = (boundaryLength - sigma/2)
            vel[over, i] *= -1.0

        speeds = np.linalg.norm(vel, axis = 1)
        curVrms = np.sqrt(np.mean(speeds**2))
        curT = (mlcMW * curVrms**2)/(3*boltzmannConstant)

        temp_label.text = f"Temperature: {curT} K"

        for i in range(N):
            particles[i].pos = vector(pos[i, 0], pos[i, 1], pos[i, 2])
            particles[i].color = getSpectrumColor(speeds[i], vRMS)
        
        vel = vel * 0.999
    
    return

LJ3DSimul()