# Import des bibliothèques time et random (time pas utilisée)

import time,random

# définition types blocks 
blocks=["f","o","X","1","2","3","4"]
# définition des items qui popent sur la map
items_list=["ifb","ex","rmv","nk"]

# fonction qui vérifie places disponibles (inutilisée)
def getavailableplaces(carte,joueur):
    posJ=getPos(joueur,carte)
    places=[]
    cas=[]
    try:
        if (carte[posJ[0]][posJ[1]+1] == " "):
            places.append([0,1])
            cas.append(1)
    except:
        None
    
    
    try:
        if (carte[posJ[0]][posJ[1]-1] == " " and posJ[1]-1 >= 0):
            places.append([0,-1])
            cas.append(2)
    except:
        None

    
    try: 
        if (carte[posJ[0]+1][posJ[1]] == " "):
            places.append([1,0])
            cas.append(4)
    except:
        None
    try:
        if (carte[posJ[0]-1][posJ[1]]== " " and posJ[0]-1 >= 0):

            places.append([-1,0])
            cas.append(3)
    except:
        None
    return [places, cas]


# récupération de la position du joueur

def getPos(joueur,carte):
    for i in range(0,len(carte)):
        for j in range(0,len(carte[i])):
            if carte[i][j]==joueur:
                return [i,j]
    return [-1,-1]


# si possible, bouger à gauche
def moveleft(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[1]-1>=0 and carte[position[0]][position[1]-1] not in blocks:
        if carte[position[0]][position[1]-1] in items_list and carte[position[0]][position[1]-1] not in items:
            items.append(carte[position[0]][position[1]-1])
        carte[position[0]][position[1]]=" "
        carte[position[0]][position[1]-1]=player
    return carte, items

# si possible, bouger à droite

def moveright(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[1]<len(carte[0])-1:
        if carte[position[0]][position[1]+1] not in blocks:
            if carte[position[0]][position[1]+1] in items_list and carte[position[0]][position[1]+1] not in items:
                items.append(carte[position[0]][position[1]+1])
            carte[position[0]][position[1]]=" "
            carte[position[0]][position[1]+1]=player
    return carte,items

def moveup(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[0]-1>=0 and carte[position[0]-1][position[1]] not in blocks:
        if carte[position[0]-1][position[1]] in items_list and carte[position[0]-1][position[1]] not in items:
            items.append(carte[position[0]-1][position[1]])
        carte[position[0]][position[1]]=" "
        carte[position[0]-1][position[1]]=player
    return carte,items

def movedown(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[0]<len(carte)-1:
        if carte[position[0]+1][position[1]] not in blocks:
            if carte[position[0]+1][position[1]] in items_list and carte[position[0]+1][position[1]] not in items:
                items.append(carte[position[0]+1][position[1]])
            carte[position[0]][position[1]]=" "
            carte[position[0]+1][position[1]]=player
    return carte,items


def positionblock(player, carte):
    position = getPos(player,carte)
    if position[1]-1>=0 and carte[position[0]][position[1]-1] == "o":
        return True
    if position[1]<len(carte[0])-1:
        if carte[position[0]][position[1]+1] == "o":
            return True
    if position[0]-1>=0 and carte[position[0]-1][position[1]] == "o":
        return True
    if position[0]<len(carte)-1:
        if carte[position[0]+1][position[1]] == "o":
            return True
    else:
        return False



def removeoldexplosions(carte,bombelist):
    if len(bombelist) == 0:
        for i in range(0,len(carte)):
            for j in range(0,len(carte[i])):
                if carte[i][j] == "ex":
                    carte[i][j] = " "
        return [True, carte]
    else:
        return [False]

# une bonne fonction !

def nuke(carte,plyr):


    for i in range(0,len(carte)):
        for j in range(0,len(carte[i])):
            if carte[i][j] != plyr and carte[i][j] != "X":
                carte[i][j]=" "
    return carte    

passe=0

# fonction fabien

def elevage_de_moi(carte,player,passe):
    #print("fabien")
    global fabienslocation
    try:
        fabienslocation
    except NameError:
        fabienslocation=[]
    
    if passe==0:
        nbfabiens=random.randint(0,10)
        for i in range(0,nbfabiens):
            
            y=random.randint(0,10)
            x=random.randint(0,12)
            #print(str(x)+" "+str(y))
            fabienslocation.append([y,x])
            if carte[y][x] != "X":
                carte[y][x]="f"
        passe+=1
    elif passe>0:
        #print(fabienslocation)
        vl=0
        for i in fabienslocation:
            #print(fabienslocation)
            #print(i)
                    
            try:
                if carte[i[1]][i[0]+1] != "X":
                    carte[i[1]][i[0]+1]="f"
                    carte[i[1]][i[0]]=" "
                    fabienslocation[vl]=[i[1],i[0]+1]
                    #print([i[1],i[0]+1])
                    
                else:
                    carte[i[1]][i[0]]=" "
                    fabienslocation.remove(i)
            except:
                try:
                    carte[i[1]][i[0]]=" "
                except:
                    print("Attention, une erreur est survenue avec un des fabien !!!!")
                fabienslocation.remove(i)

            
            
            vl+=1
    if len(fabienslocation) == 0:
        passe=0
        for i in range(0,len(carte)):
            for j in range(0,len(carte[i])):
                if carte[i][j]=="f":
                    carte[i][j]=" "
    return [carte,passe,fabienslocation]

def posebombe(player,carte):
    posplayer=getPos(player,carte)
    possible=True
    cas=0
    mabombe=[0,0]
    # if posplayer[0] < len(carte) and posplayer[1]+1 < len(carte[0]):
    #     if(carte[posplayer[0]][posplayer[1]+1] != "X" and carte[posplayer[0]][posplayer[1]+1] != "o"):
    #         cas=1
    #         possible=True
    #     elif posplayer[1]-1 > 0 and posplayer[0]-1 >0:
    #         if(carte[posplayer[0]][posplayer[1]-1] != "X" and carte[posplayer[0]][posplayer[1]-1] != "o"):
    #             cas=2
    #             possible=True
    #         elif carte[posplayer[0]-1][posplayer[1]] != "X" and carte[posplayer[0]-1][posplayer[1]]!="o":
    #             cas=3
    #             possible=True
    #         elif carte[posplayer[0]+1][posplayer[1]] != "X" and carte[posplayer[0]+1][posplayer[1]] != "o":
    #             cas=4
    #             possible=True
    possibilites=getavailableplaces(carte,player)
    if len(possibilites[0]) != 0 and len(possibilites[1]) != 0:
        possible=True
        cases=possibilites[1]
        if len(cases) > 1:
            cas=cases[random.randint(0,len(cases)-1)]
        else:
            cas=cases[0]
            

    if possible:
        #carte[posplayer[0]][posplayer[1]] = "b"
        mabombe=[posplayer[0],posplayer[1]]
        
    return [carte,mabombe]


def laluck():
    nombre=random.randint(0,1000)
    if nombre in range(0,50):
        rendu="ifb"
        itm=True
    elif nombre in range(51,200):
        rendu="rmv"
        itm=True
    elif nombre in range(201,202):
        rendu="nk"
        itm=True
    else:
        rendu="ex"
        itm=False
    return rendu,itm



def explosionbombe(carte,posebombe):
    exp=[]
    # for i in range(0,len(carte)):
    #     for j in range(0,len(carte[i])):
    carte[posebombe[0]][posebombe[1]],i=laluck()
    if not i:
        exp.append([posebombe[0],posebombe[1]])
    
    try:
        e=carte[posebombe[0]+1][posebombe[1]]
        if(e != "X"):
            carte[posebombe[0]+1][posebombe[1]],i=laluck()
            if not i:
                exp.append([posebombe[0]+1,posebombe[1]])
    except:
        None


    try:
        e=carte[posebombe[0]-1][posebombe[1]]
        if(e != "X" and posebombe[0]-1>=0):
            carte[posebombe[0]-1][posebombe[1]],i=laluck()
            if not i:
                exp.append([posebombe[0]-1,posebombe[1]])
    except:
        None
    try:
        e=carte[posebombe[0]][posebombe[1]+1]
        if(e != "X"):
            carte[posebombe[0]][posebombe[1]+1],i=laluck()
            if not i:
                exp.append([posebombe[0],posebombe[1]+1])
    except:
        None

    try:
        e=carte[posebombe[0]][posebombe[1]-1]
        if(e != "X" and posebombe[1]-1>=0):
            carte[posebombe[0]][posebombe[1]-1],i=laluck()
            if not i:
                exp.append([posebombe[0],posebombe[1]-1])
    except:
        None
    
    return carte,exp