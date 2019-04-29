#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import pandas as pd
import random
import scipy.io
import scipy.signal
import seaborn as sns
from scipy import ndimage
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d


# ## Bumblebee (Bombus impatiens) colony development
# 
# #### This species of bumblebee is common across the eastern half of the United States and parts of Canada. They are essential and highly adaptable pollinators, but may currently at risk of decline due to climate change and widespread pesticide use.
# 
# #### Bumblebee queens are the only bees to survive the winter. They emerge from hibernation in early spring and found new colonies with their already fertilized eggs. The first larvae to hatch are  female worker bees, followed by drone males. Finally, a small number of new queens are produced; their eggs will be fertilized by the drones. I will assume that the bee larvae emerge and die at a linear rate, as the rate is not dependent on the population of bees already present.
# 
# #### This colony growth is modeled as follows.

# In[123]:


#Worker bees:
def wline(x):
    m=1.2
    c=1
    return m*x+c
x=np.arange(0,70,0.1)
y=[]

for number in x:
    y.append(wline(number))

plt.plot(x,y,color='b',label="workers")

def wflatline(x):
    m=0
    c=85
    return m*x+c
x=np.arange(70,180,0.1)
y=[]

for number in x:
    y.append(wflatline(number))

plt.axhline(0, color="black")
plt.axvline(0, color="black")

plt.xlim(-1,300)
plt.ylim(0,200)

plt.xlabel("days after colony is founded")
plt.ylabel("number of bees")
plt.plot(x,y,color='b')

def wdecline(x):
    m=-3
    c=625
    return m*x+c
x=np.arange(180,240,0.1)
y=[]

for number in x:
    y.append(wdecline(number))

plt.axhline(0, color="black")
plt.axvline(0, color="black")

plt.xlim(-1,300)
plt.ylim(0,200)

plt.xlabel("days after founding of colony")
plt.ylabel("number of bees")
plt.plot(x,y,color='b')

#Drones
def dline(x):
    m=1
    c=-90
    return m*x+c
x=np.arange(90,120,0.1)
y=[]

for number in x:
    y.append(dline(number))

plt.plot(x,y,color='r',label='drones')

def dflatline(x):
    m=0
    c=30
    return m*x+c
x=np.arange(120,180,0.1)
y=[]

for number in x:
    y.append(dflatline(number))
plt.plot(x,y,color='r')

def ddecline(x):
    m=-2
    c=390
    return m*x+c
x=np.arange(180,210,0.1)
y=[]

for number in x:
    y.append(ddecline(number))
plt.plot(x,y,color='r')

#BABY QUEENS. They'll mate with drones before drones die, then survive the winter and establish new colonies in the spring.

def queenline(x):
    m=2
    c=-320
    return m*x+c
x=np.arange(160,165,0.1)
y=[]

for number in x:
    y.append(queenline(number))
plt.plot(x,y,color='m',label="queens")
def queenflatline(x):
    m=0
    c=10
    return m*x+c
x=np.arange(165,300,0.1)
y=[]

for number in x:
    y.append(queenflatline(number))
plt.plot(x,y,color='m')
plt.legend()
plt.show()


# # Nectar/honey stores during colony growth & decline (normal conditions)
# 
# Can be modeled by the differential equation
# $\frac {\delta N} {\delta t}=N_{0}+k_{p}W-k_{c}B$
# 
# where: N=nectar/honey quantity, W= number of worker bees, B= number of total bees (includes those that don't produce nectar, ie queens, larvae, and drones), $k_{p}$ =production constant per worker bee, $k_{c}$= consumption constant for the average bee in the colony.
# 
# Here are two graphs of this, both during early colony development (spring) and when colony decline begins (fall).

# In[99]:


#During early colony development, say, the month of May.
N=6
W=5
B=10
kc=0.005
kp=0.01
Ncon=[6]
Wcon=[5]
Bcon=[0]
t=np.linspace(0,10,1001)
for i in range (1000):
    dN=-kc*B+kp*W
    dW=0.4
    dB=0.5
    N=N+dN
    W=W+dW
    B=B+dB
    Ncon.append(N)
    Wcon.append(W)
    Bcon.append(B)
plt.plot(t,Ncon,'-c', label='Nectar amount(mL)')
plt.plot(t,Wcon,'-r', label='Workers (# individuals)')
plt.plot(t,Bcon,'-b', label='Total bees (# individuals)')
plt.legend()
plt.xlabel("Time (days)")
plt.title("Nectar stores and bee populations(early colony growth)")


# In[98]:


# During colony decline
N=1200
W=200
B=250
kc=0.008
kp=0.01
Ncon=[1200]
Wcon=[200]
Bcon=[250]
t=np.linspace(0,10,1001)
for i in range (1000):
    dN=-kc*B+kp*W
    dW=-0.2
    dB=-0.1
    N=N+dN
    W=W+dW
    B=B+dB
    Ncon.append(N)
    Wcon.append(W)
    Bcon.append(B)
plt.plot(t,Ncon,'-c', label='Nectar amount(mL)')
plt.plot(t,Wcon,'-r', label='Workers (# individuals)')
plt.plot(t,Bcon,'-b', label='Total bees (# individuals)')
plt.legend()
plt.xlabel("Time (days)")
plt.title("Nectar stores and bee populations(During colony decline!)")


# ## Bumblebee colony development is impacted by neonicotinoid pesticide exposure
# 
# #### Neonicotinoid pesticides are commonly used in commercial farming. These compounds disrupt cholinergic signaling in the insect central nervous system. On a larger scale, exposure to these pesticides has been shown to reduce overall colony size: it impairs foraging behavior, thermoregulation, and social networks.
# 
# #### Below, I model colony growth under different pesticide exposures:

# ## Colony heat distribution in experimental cage under normal conditions
# 
# #### We'll be using a modified rectangular food container as a cage. The colony will start off as only one queen, so there will be a single spike at her location.

# In[34]:


t=1 # On day 1, there's only one queen.
D=0.005
def u(x,y,t):
    return (1/(270*np.pi*D*t)*np.exp(-(x**2+y**2)/(4*D*t)))
x=np.linspace(-7, 7, 100)
y=np.linspace(-5, 5, 100)
X, Y = np.meshgrid (x, y)
Z=u(X,Y,t)
figu=plt.figure()
ax=plt.axes(projection='3d')
ax.plot_surface(X,Y,Z, color='m')


# #### After 25 days there are dozens more bees present, and they tend to cluster around the queen and the newly born workers. Social behaviors are normal.

# In[30]:


t=25 #25 days, more bees!
D=0.1
def u(x,y,t):
    return (1/(4*np.pi*D*t)*np.exp(-(x**2+y**2)/(4*D*t)))
x=np.linspace(-7, 7, 100)
y=np.linspace(-5, 5, 100)
X, Y = np.meshgrid (x, y)
Z=u(X,Y,t)
figu=plt.figure()
ax=plt.axes(projection='3d')
ax.set_title("Concentration of thermal energy")
ax.plot_surface(X,Y,Z,color='m')


# # Thermal energy distribution in a mature colony under neonicotinoid exposure 
# 
# #### We're going to see a sparser distribution of bees in the center; there will be more individuals clustered at the edges of the space due to neonicotinoids' impact on bees' social behavior. The difference from normal colonies is even more pronounced in the evening.

# In[49]:


t=25 #days
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = np.linspace(-7, 7, 30)
y = np.linspace(-5, 5, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');


# ## Models of bumblebee population growth over many seasons
# 
# ### Infinite resources (exponential growth)
# Assuming infinite resources in the environment (probably never the case in nature for bees) and nothing systematically killing populations, bumblebee populations will increase at $\frac{dx}{dt}= kx$, which solves to $x(t)= Ce^{kt}$. k is just some growth constant.
# 
# ### Finite resources (logistic growth)
# With finite resources, bee populations will grow according to $\frac {dx}{dt}=kx(1-\frac{x}{C})$, where k is a growth constant and C is the carrying capacity of the environment. An analytic solution is $x=\frac{C}{1+Ae^{-kt}}$ where $A=\frac{C-X_{0}}{X_{0}}$.
# 
# ### Finite resources + big bad pesticides.
# Now let's introduce neonicotinoid into the equation once the bees have reached carrying capacity. These pesticides both kill bees directly and decrease their reproductive capacity, so here I'll have a lower k as well as some constant d representing a proportion of bee deaths.
# This scenario is represented by the differential equation $\frac{dx}{dt}= (k-d)x$, which solves to $x(t)= Ce^{(k-d)t}$

# In[3]:


#Model for population growth with infinite resources:
B=50 #initial population
k=.04
Bpop=[50]
t=np.linspace(0,12,1201)
for i in range (1200):
    dB=k*B
    B=B+dB
    Bpop.append(B)
plt.plot(t, Bpop, '-c', label='Infinite resources')

#Model for population growth with finite resources
B=50 #initial population
k=.04
C=10**12
Bpop=[50]
t=np.linspace(0,12,1201)
for i in range (1200):
    dB=k*B*(1-B/C)
    B=B+dB
    Bpop.append(B)
plt.plot(t, Bpop, '-g', label='Finite resources')

#With finite resources + massive neocorticoid exposure after bees have reached carrying capacity

B=50 #initial population
k=.0394
C=10**12
Bpop=[50]
t=np.linspace(0,8,801)
for i in range (800):
    dB=k*B*(1-B/C)
    B=B+dB
    Bpop.append(B)
plt.plot(t, Bpop, '-m')
B=1000000000000#initial population
k=.03
d=0.05
C=1000000000000
Bpop=[1000000000000]
t=np.linspace(8,12,401)
for i in range (400):
    dB=(k-d)*B
    B=B+dB
    Bpop.append(B)
plt.plot(t, Bpop, '-m', label='Neonicotinoid exposure')

plt.title("Bee Population Growth and Decline")
plt.xlabel("Time (years)")
plt.ylabel("Bee population")
plt.xlim(0,12)
plt.ylim(0,1.2*10**12)
plt.legend()
plt.show()


# In[ ]:




