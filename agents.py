import random
import time

import config


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_column(self, state, max_depth):
        pass


class Human(Agent):
    pass


class ExampleAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        time.sleep(random.random())
        columns = state.get_possible_columns()
        return columns[random.randint(0, len(columns) - 1)]

class Negascout(Agent):

    possible_wins =[]
    def check_score(self, win, Amarks, Bmarks):
        checked = 0
        for index in range(4):
            if Bmarks & (1 << win[index]) != 0: return 0
            if Amarks & (1 << win[index]) != 0: checked +=1
        if checked == 3:
            return 1
        else:
            return 0
    def node_evaluation(self,state,player):
        evaal = 0
        Amarks = state.get_checkers(0)
        Bmarks = state.get_checkers(1)
        if len(self.possible_wins)==0:
            for i in range(config.M):
                for j in range(config.N):
                    # 1 po visini
                    if i+4 <= config.M:
                        newln=[]
                        for cnt in range(4):
                            newln.append((j * config.M)+(i+cnt))
                        self.possible_wins.append(newln)
                    # 2 po sirini
                    if j+4 <= config.N:
                        newln =[]
                        for cnt in range(4):
                            newln.append(i+(j+cnt) * config.M);
                        self.possible_wins.append(newln)
                    # po dijagonali prvoj
                    if i+4 <= config.M and j+4 <= config.N:
                        newln =[]
                        for cnt in range(4):
                            newln.append((i+cnt)+(j+cnt) * config.M)
                        self.possible_wins.append(newln)
                    # po dijagonali drugoj
                    if i-3 >= 0 and j-3 >= 0:
                        newln =[]
                        for cnt in range(4):
                            newln.append((i-cnt)+(j-cnt) * config.M)
                        self.possible_wins.append(newln)
        for win in self.possible_wins:
            evaal += self.check_score(win,Amarks,Bmarks)
        return evaal
    def negascout(self, alpha, beta, max_depth, state, player):
        mul = 1
        RED = 0
        YEL = 1
        DRAW = 2
        if player == 1:
            mul = -1
        if max_depth == 0 and state.get_state_status() is None:
            return (self.node_evaluation(state, player)) * mul, 0
        elif state.get_state_status() == RED:
            return 1000*mul, 0
        elif state.get_state_status() == YEL:
            return -1000*mul, 0
        elif state.get_state_status() == DRAW:
            return 0, 0
        columns_order = [3, 2, 4, 1, 5, 0, 6]
        score = float('-inf')
        column_ret = None
        val = score
        i =0
        for column in state.get_possible_columns():
            succ = state.generate_successor_state(column)
            if i == 0:
                val, _ = self.negascout(-beta, -alpha, max_depth-1, succ, 1-player)
                val *= (-1)
                i += 1
            else:
                val, _ = self.negascout(-alpha - 1, -alpha, max_depth-1, succ, 1-player)
                val *= -1
                if alpha < val < beta:
                    val, _ = self.negascout(-beta, -alpha, max_depth-1, succ, 1-player)
                    val *= (-1)
            if val > score:
                score = val
                column_ret = column
            alpha = max(score, val)
            if val == score and column_ret is not None:
                if columns_order.index(column_ret) > columns_order.index(column):
                    score = val
                    column_ret = column
            if alpha >= beta:
                break
        return score, column_ret

    def get_chosen_column(self, state, max_depth):
        if max_depth == 0:
            max_depth = -1
        _, column = self.negascout(float('-inf'), float('inf'), max_depth, state, state.get_next_on_move())
        return column


class MinimaxABAgent(Agent):
    possible_wins = []

    def check_score(self,win,Amarks,Bmarks):
        checked = 0
        for index in range(4):
            if Bmarks & (1 << win[index])!=0: return 0
            if Amarks & (1 << win[index])!=0: checked += 1
        if checked==3:
            return 1
        else:
            return 0

    def node_evaluation(self,state,player):
        evaal = 0
        Amarks = state.get_checkers(0)
        Bmarks = state.get_checkers(1)
        if len(self.possible_wins)==0:
            for i in range(config.M):
                for j in range(config.N):
                    # 1 po visini
                    if i+4 <= config.M:
                        newln = []
                        for cnt in range(4):
                            newln.append((j * config.M)+(i+cnt))
                        self.possible_wins.append(newln)
                    # 2 po sirini
                    if j+4 <= config.N:
                        newln = []
                        for cnt in range(4):
                            newln.append(i+(j+cnt) * config.M);
                        self.possible_wins.append(newln)
                    # po dijagonali prvoj
                    if i+4 <= config.M and j+4 <= config.N:
                        newln = []
                        for cnt in range(4):
                            newln.append((i+cnt)+(j+cnt) * config.M)
                        self.possible_wins.append(newln)
                    # po dijagonali drugoj
                    if i-3 >= 0 and j-3 >= 0:
                        newln = []
                        for cnt in range(4):
                            newln.append((i-cnt)+(j-cnt) * config.M)
                        self.possible_wins.append(newln)
        for win in self.possible_wins:
            evaal += self.check_score(win,Amarks,Bmarks)
        return evaal

    def minimax(self, alpha, beta, max_depth, state, player):
        RED = 0
        YEL = 1
        DRAW = 2
        if max_depth == 0 and state.get_state_status() is None:
            return self.node_evaluation(state, player), 0
        elif state.get_state_status() == RED:
            return 1000, 0
        elif state.get_state_status() == YEL:
            return -1000, 0
        elif state.get_state_status() == DRAW:
            return 0, 0
        columns_order = [3, 2, 4, 1, 5, 0, 6]
        if player == 0:
            score = float('-inf')
            column_ret = None
            for column in state.get_possible_columns():
                succ = state.generate_successor_state(column)
                tmp, _ = self.minimax(alpha, beta, max_depth-1, succ, 1)
                if tmp == score and column_ret is not None:
                    if columns_order.index(column_ret) > columns_order.index(column):
                        score = tmp
                        column_ret = column
                if tmp > score:
                    score = tmp
                    column_ret = column
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    break
            return score, column_ret
        else:
            score = float('inf')
            column_ret = None
            for column in state.get_possible_columns():
                succ = state.generate_successor_state(column)
                tmp, _ = self.minimax(alpha, beta, max_depth-1, succ, 0)
                if tmp == score:
                    if columns_order.index(column_ret) > columns_order.index(column):
                        score = tmp
                        column_ret = column
                if tmp < score:
                    score = tmp
                    column_ret = column
                if score < beta:
                    beta = score
                if alpha >= beta:
                    break
            return score, column_ret

    def get_chosen_column(self, state, max_depth):
        if max_depth == 0:
            max_depth = -1
        _, column = self.minimax(float('-inf'), float('inf'), max_depth, state, state.get_next_on_move())
        return column

