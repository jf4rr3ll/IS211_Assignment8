#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module plays the game Pig"""

import random
import textwrap
import time


class Die:
    def __init__(self):
        self.value = 0
        seed = 0

    def roll(self):
        self.value = random.randint(1, 6)


class Player:
    def __init__(self):
        self.turn = False
        self.roll = True
        self.hold = False
        self.score = 0
        self.name = None

    def decide(self):
        decision = raw_input('Would you like to "Hold" or "Roll"? ')
        decision = decision.lower()
        if decision == 'hold':
            self.hold = True
            self.roll = False
        elif decision == 'roll':
            self.hold = False
            self.roll = True
        else:
            print('Invalid input, you must "Hold" or "Roll".')
            self.decide()


class ComputerPlayer(Player):

    def __init__(self):
        Player.__init__(self)
        self.name = "Computer"
        self.turn = False
        self.roll = True
        self.hold = False
        self.score = 0

    def decide(self):
        if 25 < 100 - self.score:
            hold_limit = 25
        else:
            hold_limit = 100 - self.score

        if self.score < hold_limit:
            return "roll"
        elif self.score >= hold_limit:
            return "hold"


class HumanPlayer(Player):

    def __init__(self):
        self.name = None
        Player.__init__(self)


class Game:
    def __init__(self, player1, player2, die):
        self.turn_score = 0
        self.die = Die()
        self.player1 = player1
        self.player2 = player2
        self.player1.score = 0
        self.player2.score = 0
        self.player1.name = "Player 1"
        self.player2.name = "Player 2"

        print raw_input("Press Enter to flip a coin to determine who will go first.")
        flip_result = random.randint(1, 2)
        if flip_result == 1:
            self.current_player = self.player1
            print "Player 1 will go first."
        elif flip_result == 2:
            self.current_player = self.player2
            print "Player 2 will go first."
        self.turn()

    def next_turn(self):
        self.turn_score = 0
        if self.player1.score >= 100:
            print "Player 1 wins!"
            print "Score:", self.player1.score
            self.endgame()
            newGame()
        elif self.player2.score >= 100:
            print "Player 2 wins!"
            print "Score:", self.player2.score
            self.endgame()
            newGame()
        else:
            if self.current_player == self.player1:
                self.current_player = self.player2
            elif self.current_player == self.player2:
                self.current_player = self.player1
            print "Next turn, it is ", self.current_player.name, "'s turn."
            self.turn()

    def turn(self):
        self.die.roll()
        if (self.die.value == 1):
            print "You Rolled a 1! No points added, your turn is over."
            print "Player 1 Score:", self.player1.score
            print "Player 2 Score:", self.player2.score
            self.turn_score = 0
            self.next_turn()
        else:
            self.turn_score = self.turn_score + self.die.value
            print "You rolled a:", self.die.value
            print "Current Value is:", self.turn_score
            print "Player 1 Score:", self.player1.score
            print "Player 2 Score:", self.player2.score
            self.current_player.decide()
            if (self.current_player.hold == True and self.current_player.roll == False):
                self.current_player.score = self.current_player.score + self.turn_score
                self.next_turn()
            elif (self.current_player.hold == False and self.current_player.roll == True):
                self.turn()

    def endgame(self):
        self.player1 = None
        self.player2 = None
        self.die = None
        self.turn_score = None


class Proxy(Game):
    def __init__(self):
        self.timestamp = time.time() + 60

    def timeCheck(self, timestamp):
        if (self.timestamp < time.time() ):
            print "Time is up! Game over!"


def newGame():
    new = raw_input('Welcome to Pig, would you like to read the rules, or just start the game? ("Read" / "Start")')
    if new.lower() == "read":
        instructions = "The rules of Pig are simple. The game features two players, whose goal is to reach " \
                       "100 points first. Each turn, a player repeatedly rolls a die until either a 1 is rolled " \
                       "or the player holds and scores the sum of the rolls (i.e. the turn total). At any time " \
                       "during a player's turn, the player is faced with two decisions: ROLL ­ If the player rolls " \
                       "a 1: the player scores nothing and it becomes the opponent's turn. If the player rolls 2 ­ 6:" \
                       " the number is added to the player's turn total and the player's turn continues. HOLD ­ The " \
                       "turn total is added to the player's score and it becomes the opponent's turn. You can also " \
                       "play a timed game: The player with the highest score at the end of one minute wins!"
        print textwrap.fill(instructions, 72)
        new = raw_input('Ready to start? Type "Start" to begin a normal game, or "Timed" to begin a timed game! ')
    if new.lower() == "start":
        player1 = raw_input("Player 1: Human or Computer? ").lower()
        player2 = raw_input("Player 2: Human or Computer? ").lower()
        die = Die()
        if player1 == "human":
            player1 = HumanPlayer()
        elif player1 == "computer":
            player1 = ComputerPlayer()
        if player2 == "human":
            player2 = HumanPlayer()
        elif player2  == "computer":
            player2 = ComputerPlayer()
        Game(player1, player2, die)
    if new.lower() == "timed":
        timestamp = time.time() + 60
    else:
        print 'You must type either "Start" or "Timed" to begin.'
        newGame()

if __name__ == '__main__':
    newGame()