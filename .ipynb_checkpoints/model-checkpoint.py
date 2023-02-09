#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:32:46 2022

@author: potruso
"""

import mesa
import random

from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from agents import Agent_Saver

# N_agents = 10,100,..., 1000 and so on
# p_savers = percentage of savers among the N_agents
# p_savers = percentage of random traders among the N_agents
# p_followers = percentage of followers among the N_agents
# savers_sentiment = {0,1}, e.g. 0.60 => 60% savers are buyers and 40% sellers
# Price = starting price of the asset, e.g. 12

class Market_Model(mesa.Model):
    """Market Model"""

    def __init__(self, N_agents, Price,
                 p_savers, p_rnd_traders, p_followers, savers_sentiment):
        
        # DOF model
        self.N_agents = N_agents
        self.Price = Price
        
        
        # Init dynamic variables model
        self.Last_Price = self.Price
        self.Step_Gain = 0
        self.Net_Result = 0
        
        # Environment Settings
        self.schedule = RandomActivation(self)
        self.savers_sentiment = savers_sentiment
        
        # seed for random initialization of agents wealth and other parameters
        random.seed(42)
        
        # Create Savers
        N_savers = int(N_agents * p_savers)
        wealth = 1000 
        order = 0
        wait_invest = random.randint(15, 30) # not all investors invest with the same frequency
        invested = True
        
        for i in range(N_savers):
            print('saver_{}'.format(i))
            if i <= N_savers * savers_sentiment:
                position = 'buy'
            else:
                position = 'sell'
            
            a = Agent_Saver('saver_{}'.format(i), self, position, wealth, order, wait_invest, invested)
            self.schedule.add(a)
        
        # DATACOLLECTING
        self.datacollector = DataCollector(
            model_reporters = {'Price': change_Prices}, # here put methods for datacollecting
            agent_reporters = {
                'Wealth': 'wealth',
                'Position': 'position',
                'Order': 'order'
            }
        )
    
    # we assume that each step is 1 day
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        
        # Collect the data at that timestep
        self.datacollector.collect(self)
        



def change_Prices(model):
    agent_wealth = [agent.wealth for agent in model.schedule.agents]
    agent_positions = [agent.position for agent in model.schedule.agents]
    agent_orders = [agent.order for agent in model.schedule.agents]
    
    sbo = 0 # sum buy orders
    sso = 0 # sum sell orders
    alfa = 0.1 # coefficient for price updating
    
    for i in range(len(agent_positions)):
        if agent_positions[i] == 'buy':
            sbo += agent_orders[i]
        elif agent_positions[i] == 'sell':
            sso += agent_orders[i]
    
    delta = alfa * (sbo - sso)
    
    model.Last_Price = model.Price
    model.Price = model.Price + delta
    model.Step_Gain = (model.Price - model.Last_Price)/model.Last_Price
    
    return model.Price