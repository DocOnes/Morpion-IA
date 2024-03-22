from random import choice,random

def fini(etat):
    '''Ça prend un état en entrée et ça sort un booléen pour savoir si le jeu est fini'''
    #verif ligne
    for j in range(2):
        for i in range(1,len(str(etat)),3):
            a= True
            for k in range(3):
                if j+1!=int(str(etat)[i+k]):
                    a=False
                    break
            if a:
                return a
    #verif colonne
    for j in range(2):
        for i in range(3):
            a=True
            for k in range(3):
                if j+1!=int(str(etat)[i+1+k*3]):
                    a=False
                    break
            if a:
                return a
    #verif diag
    a=True
    diag1=[1,5,9]
    diag2=[3,5,7]
    for j in range(2):
        for i in diag1:
            if j+1!=int(str(etat)[i]):
                a=False
                break
        if a:
            return a
        a=True
        for i in diag2:
            if j+1!=int(str(etat)[i]):
                a=False
                break
        if a:
            return a
            
def modif(action,etat,p):
    '''Ça prend une action, un etat et le joueur qui a fait l'action et ça sort un string avec l'état après l'action effectué'''
    c=""
    for i in range(len(str(etat))):
        if i==action:
            c+=str(p)
        else:
            c+=str(etat)[i]
    return c

def trouverpos(etat):
    '''Ça prend en entrée un état et ça ressort toutes les actions possibles'''
    pos=[]
    for i in range(len(str(etat))):
        if str(etat)[i]=="0":
            pos.append(i)
    return pos

def step(etat,pos,qval,p):
    '''Ça prend un etat, les actions possibles, la Q-table et le joueur qui doit jouer et ça ressort l'état qui a la 
    plus grande Q-value en int'''
    mini=int(modif(pos[0],etat,p))
    for i in pos:
        c=int(modif(i,etat,p))
        try:
            m=qval[mini]
        except:
            m=0
        try:
            e=qval[c]
        except:
            e=0
        if m>e:
            mini=c
    return mini

def e_step(etat,qval,epsilon,epsilon_min,decay,p):
    '''Ça prend en entrée un etat, la Q-table, l'epsilon, l'epsilon min, le decay et le joueur qui doit jouer.
    Ça ressort un True et l'etat après l'action effectué'''
    pos=trouverpos(etat)
    if len(pos)==0:
        return False,etat
    if random()>epsilon:
        etat=step(etat,pos,qval,p)
    else:
        etat=int(modif(choice(pos),etat,p))
    epsilon=max(epsilon*decay,epsilon_min)
    return True,etat

def play(etat,qvalue,epsilon,reward,lr,decay,epsilon_min,etat_base):
    '''Ça prend en entrée toute les variables et ça fait jouer l'ia contre elle même en changeant les Q-values'''
    etat=etat_base
    histo1=[]
    histo2=[]
    while True:
        histo1.append(etat)
        a,etat=e_step(etat,qvalue,epsilon,epsilon_min,decay,1)
        if fini(etat):
            r1=reward
            r2=-reward
            break
        histo2.append(etat)
        a,etat=e_step(etat,qvalue,epsilon,epsilon_min,decay,2)
        if fini(etat):
            r1=-reward
            r2=reward
            break
        if a==False:
            r1=0
            r2=0
            break
    for i in range(len(histo1)-1,-1,-1):
        try:
            qvalue[histo1[i]]+=(r1*lr)*(i+1)
        except:
            qvalue[histo1[i]]=(r1*lr)*(i+1)
    for i in range(len(histo2)-1,-1,-1):
        try:
            qvalue[histo2[i]]+=(r2*lr)*(i+1)
        except:
            qvalue[histo2[i]]=(r2*lr)*(i+1)
    return qvalue

#Les variables modifiables en fonction de la personne
etat_base=1000000000
etat=etat_base
qval={}
epsilon=1
epsilon_min=0.00001
reward=1
lr=0.01
decay=0.95

def affichage(etat):
    '''Ça prend en entrée un état et ça print l'état pour comme une grille de morpion'''
    for i in range(1,len(str(etat)),3):
        print(str(etat)[i:i+3])

def verif(etat):
    '''Ça vérifie si il y a encore des cases libres'''
    for i in range(1,len(str(etat))):
        if str(etat)[i]=="0":
            return True
    return False

#L'entrainnement de l'ia
for i in range(10):
    for j in range(100000):
        qval=play(etat,qval,epsilon,reward,lr,decay,epsilon_min,etat_base)
    print(i+1)

#C'est pour jouer contre l'ia après son entrainnement
r=int(input("1 pour rejouer "))
while r==1:
    a=input("1 pour commencer ")
    while a=="1" or a=="2":
        if a=="1":
            etat=etat_base
            while verif(etat) and not fini(etat):
                p=1
                affichage(etat)
                etat=modif(int(input()),etat,p)
                if not verif(etat) or fini(etat):
                    break
                p=21
                a,etat=e_step(etat,qval,0,0,decay,p)
                if not verif(etat) or fini(etat):
                    break
        if a=="2":
            etat=etat_base
            while verif(etat) and not fini(etat):
                p=1
                a,etat=e_step(etat,qval,0,0,decay,p)
                if not verif(etat) or fini(etat):
                    break
                p=2
                affichage(etat)
                etat=modif(int(input()),etat,p)
                if not verif(etat) or fini(etat):
                    break
    r=int(input("1 pour rejouer "))
