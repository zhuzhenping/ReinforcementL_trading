"""
Basic structure (c) 2016 Tucker Balch
Implemented by Eric Zhang since 07/2016
Q-learner class (part of reinforcement learning algorithm)
"""

import math
import random as rand
import numpy as np


class QLearner(object):

    def __init__(self,
                 num_states=100,
                 num_actions=3,
                 alpha=0.2,
                 gamma=0.9,
                 rar=0.98,
                 radr=0.95,
                 dyna=0,
                 verbose=False):

        self.verbose = verbose
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar # save for checking dyna
        self.newrar = rar # create a copy of rar to use in decay
        self.radr = radr
        self.s = 0  # state
        self.a = 0  # action
        self.Q_table = np.random.rand(num_states,num_actions)*2 - 1
        self.last_s = 0 # save the last state
        self.last_a = 0 # save the last action
        self.dyna = dyna
        self.visited = []
        if dyna: # initialize matrix for dyna implementation
            self.T_ct = {} # save counts of each action at each state in a dictionary
            self.R_table = np.zeros((num_states,num_actions)) # save reward matrix as part of model


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        # randomly select an action
        if rand.random > self.rar:
            action = self.Q_table[s].argmax()
        else:
            action = int(math.floor((rand.random() * self.num_actions)))
        # self.rar *= self.radr  # decaying random action

        if self.verbose: print "s =", s,"a =",action
        # save last move info
        self.last_s = s
        self.last_a = action
        # # normalize Q-table to prevent values to go huge
        # self.Q_table = self.Q_table/sum(sum(self.Q_table))
        return action

    def query(self, s_prime, r, iteration):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @iteration: helps to decide whether this run is the first iteration, if yes, no dyna
        @returns: The selected action
        """
        # epsilon greedy select an action
        if rand.random() > self.newrar:
            action = self.Q_table[s_prime].argmax()
        else:
            action = int(math.floor((rand.random()*self.num_actions)))
        self.newrar *= self.radr # decaying random action

        # now update Q table
        self.Q_table[self.last_s, self.last_a] += \
            self.alpha*(r + self.gamma*self.Q_table[s_prime].max() - self.Q_table[self.last_s, self.last_a])

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r

        # if self.dyna and (not is_first_iteration): # make sure we dont do dyna at the first query
        if self.dyna and iteration:
            if [self.last_s,self.last_a] not in self.visited:
                self.visited.append([self.last_s, self.last_a])
                self.T_ct[(self.last_s, self.last_a)] = []
            self.T_ct[(self.last_s, self.last_a)].append(s_prime)
            self.R_table[self.last_s, self.last_a] = (1-self.alpha)*self.R_table[self.last_s, self.last_a] + self.alpha*r

            for _ in range(self.dyna):
                d_state, d_action = self.visited[int(math.floor((rand.random()*len(self.visited))))]
                d_s_prime = self.T_ct[d_state,d_action][int(math.floor((rand.random()*len(self.T_ct[(d_state,d_action)]))))]
                d_r = self.R_table[d_state,d_action]
                self.Q_table[d_state, d_action] += \
                    self.alpha * (d_r + self.gamma * self.Q_table[d_s_prime].max() - self.Q_table[d_state, d_action])

        # if self.verbose: print self.T_ct[(self.last_s, self.last_a)]

        self.last_s = s_prime
        self.last_a = action

        return action

    def output_q(self):
        return self.Q_table

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
