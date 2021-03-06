# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 16:05:25 2021

@author: grace.arnup
"""

#TO DO
#advantage
    #how to smoothly make 2d20kh1 into a polynomial?
    #bring advantage into the interp
    #figure out how to have +z at different levels eg 
    #(2d6+1)(1d20)kh1+5 should return the highest result between 2d6+1 and 1d20, increased by 5
#comparing two dice pools
#negative values on die faces
    #numpy does not tolerate negative powers in polynomials
    #check out sympy?
#graphing
    #plot two dice pools on one chart
    #mark the expected value of a dice pool on the plot
#subtract one dice pool from annother
#something is wrong with how oddsPlot is plotting odds
    #check out the graphing elements

import numpy
from numpy.polynomial import Polynomial
import numpy as np
from random import randrange
import matplotlib.pyplot as plt
from math import floor

#interpreter
#accepts a list of dice in the form xdy or [i, j, k]
#outputs a list of polynomials for the input dice

def interp(diceList):   
    polynomials = []
    dieCount = 0
    
    for value in diceList:        
        if type(value) == numpy.polynomial.polynomial.Polynomial:
            polynomials.append(value)
        #this takes a list of faces and builds a polynomial for that die
        elif type(value) == list:
            diePoly = 0
           
            for face in value:
                if type(face) != int:
                    print ("die value error")                              
                
                else:                    
                    diePoly += Polynomial.basis(face)
            
            polynomials.append(diePoly)                                        
            
        elif type(value) == str:
            dice = value.split(",")
            # print("dice: {}".format(dice))
            modifier = 1
            
            for i in dice:
                die = []
                # print("i in dice: {}".format(i))
                
                if "+" in i: 
                    die = i.split("+")
                    # print("positive modifer, die = {}".format(die))
                
                elif "-" in i:
                    die = i.split("-")
                    modifier = -1
                    # print("negative modifer, die = {}".format(die))
               
                else:
                    die.append(i)
                    die.append(0)
                    # print("no modifer, die = {}".format(die))
                
                # print("die: {}".format(die))           
                    
                
                data = die[0].split("d")
                # print("data: {}".format(data))
                
                data[0] = int(data[0])
                dieCount += data[0]
                
                if data[0] == 1:                                            
                    poly = 0
                                     
                    count = int(data[1])
                    while count > 0:
                        poly += Polynomial.basis(count)
                        count -= 1
                    
                    # print("poly: {}".format(poly))
                    # print("die[1]: {}".format(die[1]))
                    # print("modifier: {}".format(modifier))
                    
                    poly = applyModifier(poly, int(die[1]) * modifier)
                                                     
                    polynomials.append(poly)
                
                elif data[0] > 1:
                    pool = []
                    
                    count = int(data[0])                               
                    while count > 0:                                                
                        pool.append("1d{}".format(data[1]))
                        count -= 1
                    
                    print("pool: {}".format(pool))
                    pool = getPool(pool)
                    print("getPool: {}".format(pool))
                    poly = applyModifier(pool, int(die[1]) * modifier)
                                    
                    polynomials.append(poly)
                               
    return polynomials                

#accepts a polynomial and a modifier
#returns the result of the polynomial, plus or minus the modifier
#results cannot go below 0
def applyModifier(poly, mod):
    # print("poly: {}, modifier: {}".format(poly, mod))
    
    if mod > 0:
        poly *= Polynomial.basis(mod)    
   
    elif mod < 0:
        result = 0
        for i in range(0, len(poly)):
            if i <= abs(mod):
                result += poly.coef[i]
            else:
                result += Polynomial.basis(i + mod) * poly.coef[i]
        poly = result    
   
    return poly  


#multiplies polynomials from a list
#returns a single polynomial, representing their combined possible rolls
def getPool(diceList):
    if type(diceList) == numpy.polynomial.polynomial.Polynomial:
        return diceList
    else:
        dice = interp(diceList)    
        pool = 1
        
        for die in dice:       
            pool = die * pool
        
        return pool


#gives the odds of a given dice pool in rolling equal or high that a target number
def odds(diceList, target):
    if type(target) == int:
        pool = getPool(diceList)       
        results = 0
        successes = 0
        
        count = 0
        while count < len(pool):
            results += pool.coef[count]
            if count >= target:
                successes += pool.coef[count]    
            count += 1
        
    return (successes/results)


#takes two dice lists, returns % chance that one will be higher than the other
def comparePools(diceList1, diceList2):
    pool1 = getPool(diceList1)
    pool2 = getPool(diceList2)
      
    score1 = 0
    score2 = 0    
    total = 0
       
    for i in range(1, len(pool1)):   
    
        for j in range(1, len(pool2)):  
              total += pool1.coef[i] + pool2.coef[j]
              
              # print ("{}: {}, {}: {}".format(diceList1, i, diceList2, j))
              
              if i > j:
                  score1 += pool1.coef[i] + pool2.coef[j]                                                    
                  # print(""""{} is higher, add {}""".format(diceList1,  pool1.coef[i] + pool2.coef[j]))
              elif j > i:
                  score2 += pool1.coef[i] + pool2.coef[j]
                  # print("{} is higher, add {}".format(diceList2, pool1.coef[i] + pool2.coef[j]))           
            
    chance1 = floor(score1/total * 100)
    chance2 = floor(score2/total * 100)
    chanceDraw = floor((1 - (score1 + score2)/total) * 100)

    print (text.format(diceList1, 
                       chance1, 
                       diceList2, 
                       chance2, 
                       chanceDraw))
    
    
#text for comparePools()
text = """Odds:
{} will be higher {}% of the time
{} will be higher {}% of the time 
They will be equal {}%of the time"""    


#prints the information from odds()
def printOdds(diceList, target):
    value = int(odds(diceList, target) * 100)
    dice = ""
    for die in diceList:
        if dice =="":
            dice += str(die)
            
        else:
            dice += " + {}".format(str(die)) 
    print("""Dice pool: {}
There is a {}% chance of rolling equal to or higher than {}""".format(dice, value, target))
    oddsPlot(diceList, target)
    
    
def oddsPlot(diceList, target):
    pool = getPool(diceList)
    total = 0
    
    x = []
    y = []
    
    count = 1    
    while count < len(pool):
        total += pool.coef[count]
        x.append(count)
        y.append(total)
        count += 1
    
    fig = plt.figure()    
    ax = fig.add_axes([0,0,1,1])
    ax.axvline(target, color="red")
    ax.bar(x, y)
    
    plt.show() 
    
    #printOdds(diceList, target)


#accepts a dice list and target number
#ought to output a graph of x vs chance to score at least x, and a line to mark the target
#doesnt work - I think total is getting much to high
def oddsPlot2(diceList, target):
    pool = getPool(diceList)
    total = 0
    values = []
    percents = []
    
    for i in range(0, len(pool)):
        values.append(i)
        
        for j in range(0, len(pool)):
            total += pool.coef[j]
            if j >= i: 
                values[i] += j
    
    del values[0] 
    
    for i in values:        
        percents.append(floor(i/total * 100))
    
    fig = plt.figure()    
    ax = fig.add_axes([0,0,1,1])
    ax.axvline(target, color="red")
    ax.bar(range(1, len(pool)), percents)
    
    plt.show()  

    
#gives the expectation of the dice pool
def expect(diceList):   
    pool = getPool(diceList)    
    
    results = 0
    score = 0
    
    for i in range (0, len(pool)):
        results += pool.coef[i]
        score += pool.coef[i] * i
            
    return score/results      

    
#simulates rolling the offered dice pool
#test by checking arverge result to expectation for 1d6?    
def roll(diceList):
    pool = getPool(diceList)
    
    possibles = []
   
    count = 1
    while count < len(pool):
        coef = pool.coef[count]
        
        count2 = 0        
        while count2 < coef:
            possibles.append(count)
            count2 += 1  
            
        count += 1
     
    return possibles[randrange(len(possibles))]


#compares the average of several rolls to the expected result for the dice
#find out how to do a sigma test to determine scientific accuracy?
def rolltest(diceList, tests):
    total = 0
    
    count  = 0
    while count < tests:
        total += roll(diceList)
        count += 1
    
    return total/tests - expect(diceList)    


#takes a dice and returns a bar graph of the odds for each result
def barGraph(diceList):
    pool = getPool(diceList)
    
    x = []
    y = []
    
    count = 1
    while count < len(pool):
        x.append(count)
        y.append(pool.coef[count])
        count += 1
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])    

    ax.bar(x, y)
    plt.show()
    
#accepts two lists of dice  
#returns a polynomial for rolling both dice pools and taking the higher result  
def advantage(firstDice, secondDice):
    firstPool = getPool(firstDice)
    
    secondPool = getPool(secondDice)
   
    poly = 0
    
    for i in range(0, len(firstPool)):
        for j in range(0, len(secondPool)):
            poly += firstPool.coef[i] * secondPool.coef[j] * Polynomial.basis(np.maximum(i,j))
                 
    return poly   