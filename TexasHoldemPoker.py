from tkinter import *
from tkinter import font
from winsound import *
from Card import *
from Player import *
import random

class TexasHoldemPoker:
    def __init__(self):
        self.window = Tk()
        self.window.title("Texas Holdem Poker")
        self.window.geometry("800x600")
        self.window.configure(bg="green")

        self.fontstyle = font.Font(self.window, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=16, weight='bold', family='Consolas')
        self.cardDeck = [i for i in range(52)]
        random.shuffle(self.cardDeck)
        self.player = Player("player")
        self.dealer = Player("dealer")
        self.betMoney = 10
        self.playerMoney = 1000
        self.LcardsPlayer = []
        self.LcardsDealer = []
        self.LfieldCard = []
        self.fieldCard = []
        self.deckN = 0
        self.turn = 0
        self.jokbo = {"로티플":0, "백스플":1, "스티플":2, "포카드":3, \
                      "풀하우스":4, "플러쉬":5, "마운틴":6, "백스트":7, \
                      "스트레이트":8, "트리플":9, "투페어":10, "원페어":11, \
                      "노페어":12}
        self.symbol = ["♠", "◇", "♡", "♣"]

        self.setupLabel()
        self.setupButton()

        self.window.mainloop()
    def setupButton(self):
        self.BCheck = Button(self.window, text="check", width=6, height=1, font=self.fontstyle2, \
                             command=lambda X=0: self.pressedB(X))
        self.BCheck.place(x=50, y=500)
        self.BOne = Button(self.window, text="Bet x1", width=6, height=1, font=self.fontstyle2, \
                           command=lambda X=1: self.pressedB(X))
        self.BOne.place(x=150, y=500)
        self.BDouble = Button(self.window, text="Bet x2", width=6, height=1, font=self.fontstyle2, \
                              command=lambda X=2: self.pressedB(X))
        self.BDouble.place(x=250, y=500)
        self.Deal = Button(self.window, text="Deal", width=6, height=1, font=self.fontstyle2, command=self.pressedDeal)
        self.Deal.place(x=600, y=500)
        self.Again = Button(self.window, text="Again", width=6, height=1, font=self.fontstyle2,
                            command=self.pressedAgain)
        self.Again.place(x=700, y=500)

        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'
    def setupLabel(self):
        self.LbetMoney = Label(text="$10", width=4, height=1, font=self.fontstyle, bg="green", fg="yellow")
        self.LbetMoney.place(x=200, y=450)
        self.LplayerMoney = Label(text="You have $"+str(self.playerMoney-self.betMoney), width=15, height=1, \
                                  font=self.fontstyle, bg="green", fg="yellow")
        self.LplayerMoney.place(x=500, y=450)
        self.LplayerStatus = Label(text="", width=10, height=1, font=self.fontstyle2, bg="green", fg="cyan")
        self.LplayerStatus.place(x=400, y=400)
        self.LdealerStatus = Label(text="", width=10, height=1, font=self.fontstyle2, bg="green", fg="cyan")
        self.LdealerStatus.place(x=400, y=100)
        self.Lstatus = Label(text="", width=15, height=1, font=self.fontstyle, bg="green", fg="red")
        self.Lstatus.place(x=500, y=300)
    def pressedB(self, X):
        if self.betMoney + self.betMoney * X-self.betMoney <= self.playerMoney-self.betMoney:
            self.betMoney += self.betMoney * X
            self.LbetMoney.configure(text="$" + str(self.betMoney))
            self.LplayerMoney.configure(text="You have $" + str(self.playerMoney-self.betMoney))

            if self.turn != 4:
                self.Deal["state"] = "active"
                self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME)
        else: PlaySound('sounds/wrong.wav', SND_FILENAME)

        self.BCheck["state"] = "disabled"
        self.BCheck["bg"] = "gray"
        self.BOne["state"] = "disabled"
        self.BOne["bg"] = "gray"
        self.BDouble["state"] = "disabled"
        self.BDouble["bg"] = "gray"
        if self.turn == 4: self.showResult()
    def straight(self, tmp):
        for i in range(13-5+1):
            if tmp[i+1] and tmp[i+2] and tmp[i+3] and tmp[i+4] and tmp[i+5]:
                return True
        return False
    def calcStatus(self, p):
        myStatus = ""
        tmp = []
        for c in self.fieldCard:
            tmp.append(c)
        tmp += p.getCards()
        suitTMP = [0 for _ in range(4)]
        valTMP = [0 for _ in range(14)]    #because of index
        for c in tmp:
            suitTMP[c.getX()] += 1
            valTMP[c.getValue()] += 1
        for i in range(len(suitTMP)):
            if suitTMP[i] >= 5:
                #p.setAdd(self.symbol[i])
                myStatus = "플러쉬"
                if valTMP[10] and valTMP[11] and valTMP[12] and valTMP[13] and valTMP[1]: return "로티플"
                elif valTMP[1] and valTMP[2] and valTMP[3] and valTMP[4] and valTMP[5]: return "백스플"
                elif self.straight(valTMP): return "스티플"
        triple, d1, d2 = False, False, False
        for v in valTMP:
            if v >= 4: return "포카드"
            elif v >= 3: triple = True
            elif v >= 2 and d1 == False: d1 = True
            elif v >= 2: d2 = True
            if triple and (d1 or d2): return "풀하우스"
        if myStatus != "": return myStatus
        if valTMP[10] and valTMP[11] and valTMP[12] and valTMP[13] and valTMP[1]: return "마운틴"
        if valTMP[1] and valTMP[2] and valTMP[3] and valTMP[4] and valTMP[5]: return "백스트"
        if self.straight(valTMP): return "스트레이트"
        if triple: return "트리플"
        if d1 and d2: return "투페어"
        if d1 or d2: return "원페어"
        return "노페어"
    def win(self):
        self.Lstatus.configure(text="You won!!")
        PlaySound('sounds/win.wav', SND_FILENAME)
        self.playerMoney = self.playerMoney - self.betMoney + self.betMoney * 2
    def lose(self):
        self.Lstatus.configure(text="Sorry you lost!")
        PlaySound('sounds/wrong.wav', SND_FILENAME)
        self.playerMoney = self.playerMoney - self.betMoney
    def draw(self):
        pass
    def showResult(self):
        for i in range(2):
            p = PhotoImage(file="cards/" + self.dealer.cards[i].filename())
            self.LcardsDealer[i].configure(image=p)
            self.LcardsDealer[i].image = p

        playerStatus = self.calcStatus(self.player)
        dealerStatus = self.calcStatus(self.dealer)
        self.LdealerStatus.configure(text=dealerStatus+self.dealer.getAdd())
        self.LplayerStatus.configure(text=playerStatus+self.player.getAdd())

        if self.jokbo.get(playerStatus) < self.jokbo.get(dealerStatus): self.win()
        elif self.jokbo.get(playerStatus) > self.jokbo.get(dealerStatus): self.lose()
        else:
            pass

        self.betMoney = 0
        self.LbetMoney.configure(text="$" + str(self.betMoney))
        self.LplayerMoney.configure(text="You have $" + str(self.playerMoney-self.betMoney))

        self.Again['state'] = 'active'
        self.Again['bg'] = 'white'
    def pressedDeal(self):
        self.BCheck["state"] = "active"
        self.BCheck["bg"] = "white"
        self.BOne["state"] = "active"
        self.BOne["bg"] = "white"
        self.BDouble["state"] = "active"
        self.BDouble["bg"] = "white"
        self.Deal["state"] = "disabled"
        self.Deal["bg"] = "gray"

        if self.turn == 0:
            self.hitPlayer(self.player.inHand())
            self.hitDealerDown(self.dealer.inHand())
            self.hitPlayer(self.player.inHand())
            self.hitDealerDown(self.dealer.inHand())
        elif self.turn == 1:
            for i in range(3):
                self.setFieldCard()
        elif self.turn == 2: self.setFieldCard()
        elif self.turn == 3: self.setFieldCard()

        self.turn += 1
    def hitPlayer(self, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.player.addCard(newCard)
        p = PhotoImage(file="cards/" + newCard.filename())
        self.LcardsPlayer.append(Label(self.window, image=p))
        self.LcardsPlayer[self.player.inHand() - 1].image = p
        self.LcardsPlayer[self.player.inHand() - 1].place(x=50 + n * 80, y=350)
        PlaySound('sounds/cardFlip1.wav', SND_FILENAME)
    def hitDealerDown(self, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.dealer.addCard(newCard)
        p = PhotoImage(file="cards/b2fv.png")
        self.LcardsDealer.append(Label(self.window, image=p))
        self.LcardsDealer[self.dealer.inHand() - 1].image = p
        self.LcardsDealer[self.dealer.inHand() - 1].place(x=50 + n * 80, y=50)
        PlaySound('sounds/cardFlip1.wav', SND_FILENAME)
    def setFieldCard(self):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        n = self.deckN-4
        self.fieldCard.append(newCard)
        p = PhotoImage(file="cards/" + newCard.filename())
        self.LfieldCard.append(Label(self.window, image=p))
        self.LfieldCard[n - 1].image = p
        self.LfieldCard[n - 1].place(x=130 + n * 80, y=200)
        PlaySound('sounds/cardFlip1.wav', SND_FILENAME)
    def pressedAgain(self):
        PlaySound('sounds/ding.wav', SND_FILENAME)

        self.player.reset()
        self.dealer.reset()
        self.fieldCard.clear()

        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'
        self.BCheck['state'] = 'active'
        self.BCheck['bg'] = 'white'
        self.BOne['state'] = 'active'
        self.BOne['bg'] = 'white'
        self.BDouble['state'] = 'active'
        self.BDouble['bg'] = 'white'

        for l in self.LcardsPlayer:
            l.destroy()
        for l in self.LcardsDealer:
            l.destroy()
        for l in self.LfieldCard:
            l.destroy()
        self.LcardsPlayer = []
        self.LcardsDealer = []
        self.LfieldCard = []

        self.LplayerStatus["text"] = ""
        self.LdealerStatus["text"] = ""
        self.Lstatus["text"] = ""

        self.turn = 0
        self.deckN = 0
        self.betMoney = 10
        self.cardDeck = [i for i in range(52)]
        random.shuffle(self.cardDeck)

        self.betMoney = 10
        self.LbetMoney.configure(text="$" + str(self.betMoney))
        self.LplayerMoney.configure(text="You have $" + str(self.playerMoney - self.betMoney))
TexasHoldemPoker()