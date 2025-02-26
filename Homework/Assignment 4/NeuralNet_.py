import numpy as np
import scipy.io as so
import scipy.optimize as opt


##### Function Definitions #################################################################
def costFunction(nn_params, *args):
    input_layer_size, hidden_layer_size, num_labels, X, Y, lambd = args[0], args[1], args[2], args[3], args[4], args[5]

    length1 = (input_layer_size+1)*(hidden_layer_size)

    nn1 = nn_params[:length1]
    T1 = nn1.reshape((hidden_layer_size, input_layer_size+1))
    nn2 = nn_params[length1:]
    T2 = nn2.reshape((num_labels, 1+ hidden_layer_size))
    m = X.shape[0] # number of training examples, useful for calculations

    ## You need to return the following variables correctly
    J = 0
    Theta1_grad = np.zeros(T1.shape)
    Theta2_grad = np.zeros(T2.shape)


####################### YOUR CODE HERE!!!! ###################################################
    '''
    Instructions (15pts): implement forward and backward propogation, set J, Theta1_grad and
    Theta2_grad to the cost, first matrix of thetas and second matrix of thetas. You don't need
    to use regularization, though there will be a 3 point b0nus if you do.

    For the y values, convert them to arrays, with a '1' in the zero index corresponding to a digit
    value of 1 and a '1' in 9th index corresponding to a digit value of 10, with zeros in all
    other indices.

    Note: you need to do an outer product when generating the capital Delta matrices in the PDF
    '''

    D1 = np.zeros(T1.shape)
    D2 = np.zeros(T2.shape)
    cost = 0

    # for each training example
    train_ex = -1 # training example number we're on (ie. which row of input matrix)
    for x in X:
        train_ex += 1

        # forward propagation
        a1 = x
        a1 = np.insert(a1, 0, 1, axis=0)
        z2 = np.dot(T1, a1)
        a2 = sigmoid(z2)
        a2 = np.insert(a2, 0 , 1, axis=0)
        z3 = np.dot(T2, a2)
        a3 = sigmoid(z3)

        # convert Y values to arrays to match 10 output units
        y = np.zeros([num_labels,])
        for i in range(num_labels):
            if Y[train_ex - 1] <= len(y):
                y[Y[train_ex] - 1] = 1

        # cost function at each layer
        for k in range(num_labels):
            cost += y[k] * np.log(a3[k]) + (1.0 - y[k]) * np.log(1.0 - a3[k])

        # back propagation
        d3 = a3 - y
        z2 = np.insert(z2, 0, 1, axis=0)
        d2 = np.dot(np.transpose(T2), d3) * sigmoidGradient(z2)
        d2 = d2[1:]
        D2 += np.outer(d3, np.transpose(a2))
        D1 += np.outer(d2, np.transpose(a1))

    Theta1_grad[0] = (1.0 / m) * D1[0]
    Theta1_grad[1:] = (1.0 / m) * D1[1:] + ((lambd / m) * T1[1:])
    Theta2_grad[0] = (1.0 / m) * D2[0]
    Theta2_grad[1:] = (1.0 / m) * D2[1:] + ((lambd / m) * T2[1:])

    regularization = (lambd / (2.0 * m)) * (np.sum(T1**2) + np.sum(T2**2))

    J = (-1.0 / m) * cost + regularization

###############################################################################################
    # unroll gradients and concatenate
    grad = np.concatenate([Theta1_grad.flatten(), Theta2_grad.flatten()])
    # return variables
    return J, grad

def gradApprox(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd):
    epsilon = 0.0001

    gradientApprox = np.zeros(nn_params.size)
    for i in range(nn_params.shape[0]):

        nn_params1 = np.copy(nn_params)
        nn_params2 = np.copy(nn_params)

        nn_params1[i] += epsilon
        nn_params2[i] -= epsilon
        cost_plus = costFunction(nn_params1, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)[0]
        cost_minus = costFunction(nn_params2, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)[0]
        cost_diff = (cost_plus - cost_minus)/(2.0*.0001)

        gradientApprox[i] = cost_diff

    return gradientApprox


def sigmoid(h):
    sigmoid = 0
###################### YOUR CODE HERE!!!! #####################################################
    sigmoid = 1.0 / (1.0 + np.exp(-h))
##############################################################################################
    return sigmoid




def sigmoidGradient(z):
    sigmoidGrad = 0
###################### YOUR CODE HERE!!!! #####################################################
    sigmoidGrad = sigmoid(z) * (1.0 - sigmoid(z))
###############################################################################################
    return sigmoidGrad


def forwardPropAndAccuracy(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y):

    predictions = 0
    percentCorrect = 0
####################### YOUR CODE HERE !!!! ###################################################
#Extra Credit: 5 points

    length1 = (input_layer_size+1)*(hidden_layer_size)

    nn1 = nn_params[:length1]
    T1 = nn1.reshape((hidden_layer_size, input_layer_size+1))
    nn2 = nn_params[length1:]
    T2 = nn2.reshape((num_labels, 1+ hidden_layer_size))
    m = X.shape[0] # number of training examples, useful for calculations

    correct = 0
    total = 0
    predictions = np.empty(len(Y))
    # for each training example
    train_ex = -1 # training example number we're on (ie. which row of input matrix)
    for x in X:
        train_ex += 1

        # forward propagation
        a1 = x
        a1 = np.insert(a1, 0, 1, axis=0)
        z2 = np.dot(T1, a1)
        a2 = sigmoid(z2)
        a2 = np.insert(a2, 0 , 1, axis=0)
        z3 = np.dot(T2, a2)
        a3 = sigmoid(z3)

        # convert Y values to arrays to match 10 output units
        y = np.zeros([num_labels,])
        for i in range(num_labels):
            if Y[train_ex - 1] <= len(y):
                y[Y[train_ex] - 1] = 1

        a = np.argmax(a3)
        # print a, np.argmax(y)
        if a == np.argmax(y):
            correct += 1.0
        total += 1.0
        predictions[train_ex] = a

    predictions = predictions.flatten()
    percentCorrect = correct / total

###############################################################################################

   #make sure you return these correctly
    return predictions, percentCorrect


def randomInitializeWeights(weights, factor):
##### This is implemented for you. Think: Why do we do this? #################################

    W = np.random.random(weights.shape)
    #normalize so that it spans a range of twice epsilon
    W = W * 2.0 * factor # applied element wise
    #shift so that mean is at zero
    W = W - factor #L_in is the number of input units, L_out is the number of output
    #units in layer

    return W

###############################################################################################
# helper methods
def getCost(nn_params, *args):
    input_layer_size, hidden_layer_size, num_labels, X, Y, lambd = args[0], args[1], args[2], args[3], args[4], args[5]
    cost = costFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)[0]
    print cost
    return cost



def getGrad(nn_params, *args):
    input_layer_size, hidden_layer_size, num_labels, X, Y, lambd = args[0], args[1], args[2], args[3], args[4], args[5]
    return costFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd )[1]

###############################################################################################



###############################################################################################
##### Start Program! ##########################################################################
###############################################################################################


print "Loading Saved Neural Network Parameters..."

data = so.loadmat('ex4data1.mat')

X = data['X']
Y = data['y']

#previously determined weights to check
weights = so.loadmat('ex4weights.mat')

weights1 = weights['Theta1']
weights2 = weights['Theta2']

#weights1 = weights1.T

input_layer_size  = 400
hidden_layer_size = 25
num_labels = 10
lambd = 1.0
params = np.concatenate([weights1.flatten(), weights2.flatten()])

j, grad = costFunction(params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)

print "Cost at parameters loaded from ex4weights.mat. (This value should be about 0.383770 with regularization, 0.287629 without): ", j

print "signmoidGrad of 0 (should be 0.25): ", sigmoidGradient(0)

params_check = randomInitializeWeights(np.zeros(params.shape), .12)

grad_check = costFunction(params_check[:35], 4, 4, 3, X[:10, :4], Y[:10, :3], lambd)[1]

grad_approx =  gradApprox(params_check[:35], 4, 4, 3, X[:10, :4], Y[:10, :3], lambd)
checkGradient = np.column_stack((grad_check, grad_approx))

print "Gradient check: the two columns should be very close: ", checkGradient

nn_params = randomInitializeWeights(np.zeros(params.shape), .12)

args = (input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)

result = opt.fmin_cg(getCost, nn_params, fprime=getGrad, gtol=.002, args=args, maxiter=50)

#extra credit
print "Accuracy: ", forwardPropAndAccuracy(result, input_layer_size, hidden_layer_size, num_labels, X, Y)[1]
