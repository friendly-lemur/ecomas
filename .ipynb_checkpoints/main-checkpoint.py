#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:39:29 2022

@author: potruso
"""

from model import Market_Model

N_agents = 100
Price = 10
Last_Price = Price
p_savers = 1.
p_rnd_traders = 0.
p_followers = 0.
savers_sentiment = 0.70

model = Market_Model(N_agents, Price, p_savers, p_rnd_traders, p_followers, savers_sentiment)

for i in range(3000):
    model.step()
    print('hi')
    
agent_vars = model.datacollector.get_agent_vars_dataframe()
model_vars = model.datacollector.get_model_vars_dataframe()

print(agent_vars)

model_vars.plot()