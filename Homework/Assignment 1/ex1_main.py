# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 20:16:13 2014

@author: jonathankroening
"""
import pylab as pl
import numpy as np
import cost_function as cf

filename = 'auto-mpg.data'

#Load and prepare data
X = np.loadtxt(filename, usecols=(4,))
Y = np.loadtxt(filename, usecols=(0,))

# Added feature scaling to keep learning rate and number of iterations reasonable.
X_norm = (X - np.mean(X))/np.std(X)

Theta = np.zeros((2,1))

print "Cost before gradient descent: " , cf.calculate_cost(X_norm, Y, Theta)
Theta, J_array = cf.gradient_descent(X_norm, Y, Theta, .01, 1000)
print "Thetas: " , Theta
print "Cost after gradient descent: ", cf.calculate_cost(X_norm, Y, Theta)

b = Theta[0]
m = Theta[1]

# main figure for plotting
fig = pl.figure(1, figsize=(7, 10))

# only plot regression line if m and b are not zero, that is, if the functions in cost_function are implemented
if (b != 0 and m != 0):

    #b and m are calculated for a scaled X, need to reconvert to graph and predict
    b -= np.mean(X)/np.std(X) * m
    m = m/np.std(X)

    # make a line to plot
    yp = pl.polyval([m,b],X)

    # plot line and scatter diagram
    #plot data
    ax1 = fig.add_subplot(2,1,1)
    ax1.plot(X, yp)
    ax1.set_title('MPG ~ Weight of Car')
    ax1.set_xlabel("Weight of Car")
    ax1.set_ylabel("MPG")

# make the scatter plot no matter if there's a regression line or not
ax1.scatter(X, Y)

# create space between subplots
fig.subplots_adjust(bottom=0.09, top=0.92,hspace=0.3)

# if the J_array (cost function) is not empty, plot it
if (sum(J_array) != 0):

    ax2 = fig.add_subplot(2,1,2)
    ax2.scatter([i for i in xrange(1000)], J_array)
    ax2.set_title('Cost Function -- J(Theta)')
    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('Cost')

pl.show()

### Note:
# a linear model is probably not the most realistic fit for this data because
# at some point, if the car is heavy enough you're going to get an MPG of 0.
# so long as we're still talking about cars here, and not boulders, every car
# has an MPG, it will never be 0.  And conversely, a really light car will likely
# achieve better MPG than just slightly worse than the y-intercept, which a
# linear model would suggest.  It's probable that the better fit is some sort of
# inverse function where it's forever in the first quadrant, never touching non-
# positive values.

