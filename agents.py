import random
import time


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
    def node_evaluation(self, state, player):
        if bin(state.get_checkers(0)).count('1') < 3:
            return 0
        Awins = 0
        Bwins = 0
        next_moves = state.get_possible_columns()
        for i in next_moves:
            curr = state.generate_successor_state(i)
            if curr.get_checkers(0) in curr.get_all_win_states():
                Awins +=1
            if curr.get_checkers(1) in curr.get_all_win_states():
                Bwins +=1
        cnt = bin(curr.get_checkers(0)).count('1')
        evaluation = (Awins - Bwins) * (1./cnt)
        return evaluation




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

    def node_evaluation(self,state,player):
        if bin(state.get_checkers(0)).count('1') < 3:
            return 0
        Awins = 0
        Bwins = 0
        next_moves = state.get_possible_columns()
        for i in next_moves:
            curr = state.generate_successor_state(i)
            if curr.get_checkers(0) in curr.get_all_win_states():
                Awins += 1
            if curr.get_checkers(1) in curr.get_all_win_states():
                Bwins += 1
        cnt = bin(curr.get_checkers(0)).count('1')
        evaluation = (Awins-Bwins) * (1. / cnt)
        return evaluation

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

