class Agent_Rnd_Trader(mesa.Agent):
    def __init__(self, unique_id, model,
                 wealth, position, order):
        super().__init__(unique_id, model)

        #random.seed(42)

        # DOF Agent
        self.wealth = round(wealth * ( 1. + 0.1 * random.uniform(-1, 1) ), 2) # cash
        self.position = position # initial position, buy or sell
        self.order = order # quantities ordered
        
        #printing init stats
        print(f'{self.unique_id}: \t $ {round(self.wealth, 2)}')
        
    # Random Trader Functions
    def rnd_trade(self):
        if random.uniform(0,1) < 0.5:
            self.position = 'buy'
            self.order = 1 #randomize also this later
        else:
            self.position = 'sell'
            self.order = 1
        
        self.wealth = self.wealth - self.order * model.Price
        
    # Step Function for random trader agent
    def step(self):
        self.wealth += 1 
        
        if self.wealth <= 0:
            self.position = 'null'
            #self.order = 0
        
        self.rnd_trade()