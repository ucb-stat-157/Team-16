#!/usr/bin/env python

import sys
import numpy as np

pclick = 0
conditionalsclick = {}

#assume each line is feature value, feature(ad id), clicks, impressions.
#ex. 10040 \t ad_id \t 0 \t 6


def train(data):
    totalclicks = 0
    totalimps = 0
    global pclick
    k = 0
    simiclick = {}
    siminoclick = {}
    
    #compute total clicks and total impressions, for P(Y)
    for line in data:
        instance = line.strip().split('\t')
        value = instance[0]
        feature = instance[1]
        clicks = int(float(instance[2]))
        imps = int(float(instance[3]))
        totalclicks += int(float(clicks))
        totalimps += int(float(imps))
        if value == "-1":
            continue
        if feature not in conditionalsclick.keys():
            conditionalsclick[feature] = {}
        #if feature is a similarity index, add it to an array so that we can calculate the mean and var later.
        if 'simi' in feature:
            if feature not in simiclick.keys():
                simiclick[feature] = []
                siminoclick[feature] = []
            for i in xrange(clicks):
                simiclick[feature].append(float(value))
            for j in xrange(imps-clicks):
                siminoclick[feature].append(float(value))
        else:
            conditionalsclick[feature][value] = instance
        
##    print conditionalsclick
##    print totalclicks
##    print totalimps
##    print pclick

        
    #P(Y)
    pclick = float(totalclicks)/totalimps
    m = 1
    
    #compute conditional probabilities. P(X|Y), P(X|not Y)
    for feature in conditionalsclick:
        #If similarity ratio, 
        if 'simi' in feature:
            conditionalsclick[feature]['click'] = (np.mean(simiclick[feature]), np.var(simiclick[feature]))
            conditionalsclick[feature]['noclick'] = (np.mean(siminoclick[feature]), np.var(siminoclick[feature]))
            conditionalsclick[feature]['UNK'] = (0,0)
        else:
            k = len(conditionalsclick[feature].keys()) + 1
            for value in conditionalsclick[feature]:
                instance = conditionalsclick[feature][value]
                #print instance
                clicks = int(float(instance[2]))
                imps = int(float(instance[3]))
                conditionalsclick[feature][value] = (float(clicks + m)/(totalclicks + (k*m)), float((imps - clicks + m))/(totalimps - totalclicks + (k*m)))
            conditionalsclick[feature]["UNK"] = (float(m)/(totalclicks + (k*m)), float((m)/(totalimps - totalclicks + (k*m))))

"""
def predict(feature, plick):

    # max of P(X|Y)*P(Y)

    click = conditionalsclick[feature] * pclick
    noclick = conditionalsnoclick[feature] * (1-pclick)

    if click > noclick:
        return 1
    else:
        return 0
"""

train(sys.stdin)

for k,values in conditionalsclick.items():
    for value, tup in values.items():
        print '%s\t%s\t%s\t%s' % (k, value, tup[0], tup[1])
    
print 'Total\tTotal\t%s\t%s' % (pclick, 1-pclick)
# print 'Total\tTotal\t%s\t%s' % (totalclicks, totalimps)
