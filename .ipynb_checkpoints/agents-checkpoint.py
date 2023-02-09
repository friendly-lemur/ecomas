#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:25:46 2022

@author: potruso
"""

import mesa
import random

class Agent_Saver(mesa.Agent):
    def __init__(self, unique_id, model,
                 position, wealth, order,
                 wait_invest, invested):
        super().__init__(unique_id, model)
        
        # DOF Agent
        self.position = position # initial position, buy or sell
        self.wealth = wealth * ( 1. + 0.01 * random.uniform(-1, 1) ) # cash
        self.order = order # quantities ordered
        
        # DOF Agent Saver
        self.wait_invest = wait_invest # timesteps of waiting before buying
        self.waiting = random.randint(1, 30) # not all investors invest at the sime timestap
        self.invested = invested
        
    # Saver Functions
    # the savers keep the position since the beginning of simulation
    # and keep buying or selling during the simulation
    def invest(self, model):
        if self.position == 'buy':
            self.order = 1 # choose a quantity to buy
            # set self.waiting = qualcosa prima di comprare di nuovo
        elif self.position == 'sell':
            self.order = 1 # choose a quantity to sell
        
        # update remaining wealth
        self.wealth = self.wealth - self.order * model.Price
    
    
    # Step Function for saver agent
    # if they have no more wealth they're out of money to invest
    # assume savers have a constant outside income they invest periodically
    def step(self, model):
        if self.wealth <= 0:
            self.position = 'null'
        
        if self.invested == True:
            self.order = 0 # do not buy anymore but wait
            self.waiting -= 1
            if self.waiting == 0:
                self.invested = False
        else:
            self.wealth += 100 # income of a saver from a portion of its salary
            self.invest(model)
            self.invested = True
            self.waiting = self.wait_invest # reset counter for next investing
            