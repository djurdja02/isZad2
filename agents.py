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
    def node_evaluation(self,state,player):
        Acheck = state.get_checkers(0)
        Bcheck = state.get_checkers(1)
        Awin = sum(1 for i in state.win_masks if (Acheck & i)==i)
        Bwin = sum(1 for i in state.win_masks if (Bcheck & i)==i)

        # vecim vrednostima je potrebno nagraditi pobede ostvarene manjim brojem zetona
        evaluation = Awin-Bwin
        if evaluation > 0:
            evaluation = evaluation+evaluation * 5.6 / bin(Acheck).count('1')
        else:
            evaluation = evaluation-evaluation * 5.6 / bin(Acheck).count('1')
        return evaluation

    def negascout(self, alpha, beta, max_depth, state, player):
        if max_depth == 0 or state.get_state_status() is not None:
            mul = 1
            if player == 1:
                mul = -1
            return (self.node_evaluation(state, player)) * mul, 0
        columns_order = [3, 2, 4, 1, 5, 0, 6]
        score = float('-inf')
        column_ret = None
        val = score
        i =0
        for column in state.get_possible_columns():
            succ = state.generate_successor_state(column)
            if i == 0:
                val, _ = self.negascout(-beta, -alpha, max_depth-1, succ, 1-player)
                val *= -1
                i += 1
            else:
                val, _ = self.negascout(-alpha - 1, -alpha, max_depth-1, succ, 1-player)
                val *= -1
                if alpha < val < beta:
                    val, _ = self.negascout(-beta, -alpha, max_depth-1, succ, 1-player)
                    val *= -1
            if val > score:
                score = val
                column_ret = column
            alpha = max(score, val)
            if val == score:
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

    def node_evaluation(self, state, player):
        Acheck = state.get_checkers(0)
        Bcheck = state.get_checkers(1)
        Awin= sum(1 for i in state.win_masks if (Acheck & i) == i)
        Bwin= sum(1 for i in state.win_masks if (Bcheck & i) == i)


        #vecim vrednostima je potrebno nagraditi pobede ostvarene manjim brojem zetona
        evaluation = Awin - Bwin
        if evaluation > 0:
            evaluation = evaluation + evaluation*5.6/bin(Acheck).count('1')
        else:
            evaluation = evaluation - evaluation*5.6/bin(Acheck).count('1')
        return evaluation

    def minimax(self, alpha, beta, max_depth, state, player):
        if max_depth == 0 or state.get_state_status() is not None:
            return self.node_evaluation(state, player), 0
        columns_order = [3, 2, 4, 1, 5, 0, 6]
        if player == 0:
            score = float('-inf')
            column_ret = None
            for column in state.get_possible_columns():
                succ = state.generate_successor_state(column)
                tmp, _ = self.minimax(alpha, beta, max_depth-1, succ, 1)
                if tmp == score:
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

