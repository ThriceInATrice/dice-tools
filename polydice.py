# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 16:05:25 2021

@author: grace.arnup
"""

#TO DO
#advantage?
    #a function to combine the dice and make a single custom die/polynomial?
    #how to smoothly make 2d20kh1 into a polynomial?
#comparing two dice pools
#graph of possible results
#die roller
#negative dice
    #numpy does not tolerate negative powers in polynomials
    #check out sympy?


from numpy.polynomial import Polynomial
from random import randint, randrange

#interpreter
#accepts a list of dice in the form xdy or [i, j, k]
#outputs a list of polynomials for the incut dice
#does not accept negatives
def interp(diceList):   
    polynomials = []
    dieCount = 0
    
    for die in diceList:        
        #this takes a list of faces and builds a polynomial for that die
        if type(die) == list:
            diePoly = 0
           
            for face in die:
                if type(face) != int:
                    print ("die value error")                              
                
                else:                    
                    diePoly += Polynomial.basis(face)
            
            polynomials.append(diePoly)                                        
            
        else:
            data = die.split("d")
            dieCount += int(data[0])
            
            if int(data[0]) == 1:                                            
                poly = 0
                
                count = int(data[1])
                while count > 0:
                    poly += Polynomial.basis(count)
                    count -= 1
                
                polynomials.append(poly)
            
            elif int(data[0])>1:
                pool = []
                
                count = int(data[0])                                
                while count > 0:
                    pool.append("1d{}".format(data[1]))
                    count -= 1

                for poly in interp(pool):                  
                    polynomials.append(poly)
                               
    return polynomials
                


#multiplies polynomials from a list
#returns a single polynomial, representing their combined possible rolls
def getPool(diceList):
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
    #make a clause that can compare two dice pools, give odds on which is higher?
        
    return (successes/results)

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
 
   
#gives the expectation of the dice pool
def expect(diceList):
    
    pool = getPool(diceList)    
    
    results = 0
    score = 0
    
    count = 1
    while count < len(pool):
        results += pool.coef[count]
        score += pool.coef[count] * (count)
        count += 1
    
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
    while count< tests:
        total += roll(diceList)
        count += 1
    
    return total/tests - expect(diceList)    
    
    