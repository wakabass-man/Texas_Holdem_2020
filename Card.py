class Card:
    def __init__(self, temp):
        self.value = temp % 13 + 1 #카드넘버
        self.x = temp//13 #카드무늬
    def getValue(self):
        return self.value
    def getX(self):
        return self.x
    def getsuit(self):
        if self.x == 0:
            self.suit = "Spades"
        elif self.x == 1:
            self.suit = "Diamonds"
        elif self.x == 2:
            self.suit = "Hearts"
        else:
            self.suit = "Clubs"
        return self.suit
    def filename(self):
        return self.getsuit()+str(self.value)+".png"