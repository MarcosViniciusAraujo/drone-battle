from platform import node
from Map.Position import Position
from random import shuffle
width = 34
heigth = 59
class Gamemap():   
    width = 34
    heigth = 59
    goldPos = []
    voidPos = []
    powerupPos = []
    blockedPos = []
    safePos = []
    unsafePos = []
    notVisit = []
    auxGoldPos = []
    
    def addPosition(self,type, x,y):
        if type == "gold":
            self.goldPos.append((x,y))
        elif type == "unsafe":
            self.unsafePos.append((x,y))
            if ((x,y) in self.notVisit):
                self.notVisit.remove((x,y))
        elif type == "safe":
            self.safePos.append((x,y))
        elif type == "block":
            self.blockedPos.append((x,y))
            if ((x,y) in self.notVisit):
                self.notVisit.remove((x,y))
        elif type == "powerup":
            self.powerupPos.append((x,y))
    def __init__(self):
        for i in range(self.heigth):
            for j in range(self.width):
                self.notVisit.append((i,j))
        shuffle(self.notVisit)
        

    def getGoldPos(self):
        return self.goldPos

    def getVoidPos(self):
        return self.voidPos
    
    def getSafePos(self):
        return self.safePos

    def getBlockedPos(self):
        return self.blockedPos
    
    def getPowerupPos(self):
        return self.powerupPos
    
    def getUnsafePos(self):
        return self.unsafePos
    
    def getNotVisit(self):
        return self.notVisit
    
    def getAuxGold(self):
        return self.auxGoldPos
    
    def populateAuxGoldPos(self,xi,yi):
        goldcopy = self.goldPos.copy()
        goldcopy = sorted(goldcopy, key=lambda x: self.manhattan(x[0],x[1],xi,yi))
        first = goldcopy.pop(0)
        self.auxGoldPos = goldcopy.copy()
        self.auxGoldPos.append(first)

    def getNearNode(self,x,y,type):
        if type == "notVisit":
            lista = self.notVisit
        elif type == "powerup":
            lista = self.powerupPos
        elif type == "gold":
            if ((x,y) in self.goldPos):
                lista = self.goldPos.copy()
                lista.remove((x,y))
                if lista == []:
                    return (10,10)
            else:
                lista = self.goldPos
        nearest = lista[0]
        menorValor = self.manhattan(nearest[0],nearest[1],x,y)
        if menorValor == 0 and type == "notVisit":
            self.notVisit.remove(nearest)
        if menorValor == 1:
            return nearest
        for i in lista[1:]:
            if (not self.isBadPos(i[0],i[1])):
                valor=self.manhattan(i[0],i[1],x,y)
                if valor<menorValor:
                    menorValor = valor
                    nearest = i
                    if menorValor == 0 and type == "notVisit":
                        self.notVisit.remove(nearest)
                    if menorValor == 1:
                        return nearest
        return nearest
#Seria bom ajustar essa função futuramente
    def nodeCost(self,x,y):
        if(self.isBadPos(x,y)):
            return 5000
        return 1

    def isBadPos(self,x,y):
        return ((x,y) in self.getBlockedPos() or (x,y) in self.getUnsafePos())

    def manhattan(self,x1,y1,x2,y2):
        return abs(x1-x2)+abs(y1-y2)
    
    #A* funciona dando como parametro as coordenadas iniciais, e depois as coordenadas finais, os pesos e custos estão na funçao nodeCost(não deu tempo de fazer direito).

    def aStar(self,xi,yi,xf,yf):
        open_set=[]
        close_set=[]
        initialNode = Node(xi,yi,0,xf,yf)
        open_set.append(initialNode)
        current = initialNode
        while open_set:
            current = min_gcost(open_set)
            if (current.x == xf and current.y == yf):
                return current.getPath()
            open_set.remove(current)
            close_set.append(current)
            vizinhos = current.getVizinhos(self.blockedPos,self.unsafePos)
            for nextNode in vizinhos:

                inFechada = False
                inAberta = False
                for i in close_set:
                    if(nextNode.x == i.x and nextNode.y == i.y):
                        inFechada = True
                if(not(inFechada)):
                    for i in open_set:
                        if(nextNode.x == i.x and nextNode.y == i.y):
                            inAberta = True
                            if(nextNode.f<i.f):
                                i.f=nextNode.f
                                nextNode.partner = current
                    if(inAberta==False):
                        open_set.append(nextNode)
                        nextNode.partner = current
        return None

def min_gcost(lista):
    menor = lista[0]
    for i in lista[1:]:
        if menor.f > i.f:
            menor = i
    return menor
class Node:
    def __init__(self,x,y,g,xf,yf):
        self.x=x
        self.y=y
        self.xf = xf
        self.yf = yf
        self.h=self.heuristic(xf,yf)
        self.g=g
        self.f = self.g + self.h
        self.partner = None
    
    def heuristic(self,xf,yf):
        return abs(self.x-xf)+abs(self.y-yf)
    
    def isValid(self,x,y):
        return(x>=0 and x<heigth and y>=0 and y<width) 

    def getVizinhos(self, blockedPos, unsafedPos):

        ret = []
        if (self.isValid(self.x-1,self.y)):
            if ((self.x-1,self.y) in blockedPos or (self.x-1,self.y) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x-1,self.y,self.g+cost,self.xf,self.yf))
        if (self.isValid(self.x+1,self.y)):
            if ((self.x+1,self.y) in blockedPos or (self.x+1,self.y) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x+1,self.y,self.g+cost,self.xf,self.yf))
        if (self.isValid(self.x,self.y+1)):
            if ((self.x,self.y+1) in blockedPos or (self.x,self.y+1) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x,self.y+1,self.g+cost,self.xf,self.yf))
        if (self.isValid(self.x,self.y-1)):
            if ((self.x,self.y-1) in blockedPos or (self.x,self.y-1) in unsafedPos):
                cost = 50
            else:
                cost = 1
            ret.append(Node(self.x,self.y-1,self.g+cost,self.xf,self.yf))
        return ret
    def getPath(self):
        temp=self
        pathList = list()
        while(temp.partner!=None):
            pathList.append(temp)
            temp=temp.partner
        return pathList[::-1]