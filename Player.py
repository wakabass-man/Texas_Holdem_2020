class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.N = 0 #카드 갯수
        self.add = ""
    def addCard(self, c):
        self.cards.append(c)
        self.N += 1
    def inHand(self):
        return self.N
    def reset(self):
        self.N = 0
        self.cards.clear()
        self.add = ""
    def getCards(self):
        tmp = []
        for c in self.cards:
            tmp.append(c)
        return tmp
    def setAdd(self, n):
        self.add = n
    def getAdd(self):
        return self.add