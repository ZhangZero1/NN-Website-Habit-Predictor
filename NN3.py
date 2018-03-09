import numpy as np

choclates = 79

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def synapseMake(current, nextVal):
    return 2*np.random.random((current,nextVal))-1

def mkLayer(index, layer, synapse, inputVal=None):
    if(index == 0):
        return inputVal
    return nonlin(np.dot(layer[index-1],synapse[index-1]))

def layerError(index, layer, delta, synapse, outputVal=None):
    
    if(outputVal is not None):
        r = outputVal-layer[index]
        return r
    r =delta[index+1].dot(synapse[index].T)
    return r 

def layerDelta(index, error, layer):
    return error[index] * nonlin(layer[index],deriv=True)

def synapseRefresh(index, synapse, layer, delta):
    return synapse[index] + (layer[index].T.dot(delta[index+1]))

def toupleFormation(layer, error, delta, synapse, inVal, outVal):
    return (layer,error,delta,synapse,inVal,outVal)

def runOnce(dataSpectrum, test =0):    #(layer[0], error[1], delta[2], synapse[3], x[4], y[5])
    layer = dataSpectrum[0]
    error = dataSpectrum[1]
    delta = dataSpectrum[2]
    synapse = dataSpectrum[3]
    inVal = dataSpectrum[4]
    outVal = dataSpectrum[5]

    
    for i in range(len(layer)):
        layer[i] = mkLayer(i,layer,synapse,inVal)
    for i in range(len(delta)-1,0,-1):
        if(i == len(delta)-1):
            error[i] = layerError(i,layer,delta,synapse,outVal)
        else:
            error[i] = layerError(i,layer,delta,synapse)
        delta[i] = layerDelta(i,error,layer)
    if test ==0:
        for i in range(len(synapse)-1,-1,-1):
            synapse[i] = synapseRefresh(i, synapse, layer, delta)

    global choclates
    choclates = layer[-1]
    return [layer,error,delta,synapse,inVal,outVal]



def networkStructure(struct, inputVal, outputVal ):
    realStruct = [len(inputVal[0])] + struct + [len(outputVal[0])]
    layer  = [0]*(len(realStruct))
    error = [0]*(len(realStruct))
    delta = [0]*(len(realStruct))
    synapse = [0]*(len(realStruct)-1)
    for i in range(len(realStruct)-1):
        synapse[i] = synapseMake(realStruct[i],realStruct[i+1])
    for i in range(len(realStruct)):
        layer[i] = 0
        error[i] = 0
        delta[i] = 0

    return [layer,error,delta,synapse,inputVal, outputVal]



X = np.array([[0,0,1],
            [0,1,1],
            [1,0,1],
            [1,1,1]])

print "xxxxxxxxxxxxxx\n", X

print "TTTTTTTTTTTTTt\n", X.T
                
y = np.array([[0],
			[1],
			[1],
			[0]])

theta = networkStructure([4,5], X, y)
for i in range(10000):
    theta = runOnce(theta)
print(choclates)

layer = theta[0]
synapse = theta[3]
inVal = np.array([[0,0,0],[1,1,0],[1,1,1],[1,0,0],[0,1,0]])
for i in range(len(layer)):
    layer[i] = mkLayer(i,layer,synapse,inVal)
print "unknown input:", inVal
print "predicted y:", layer[len(layer)-1]



    
