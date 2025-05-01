import random

class Deck:
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']


    def __init__(self):
        self.cards = []
        for suit in self.suits:
            for value in self.values:
                self.cards.append(f'{value}_of_{suit}')

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def get_value(self, card):
        return (card.split('_')[0])

    def get_suit(self, card):
        return card.split('of_')[1]




