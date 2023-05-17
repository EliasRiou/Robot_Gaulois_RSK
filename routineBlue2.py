import rsk

#from defense.defense_joueur import routine_defence
from defense.defense_joueur import routine_defence
from defense.defense_joueur import goal_volant

with rsk.Client(host='192.168.0.101', key='') as client:

    #setup
    equipe = 1 #ou -1 si on joue du coté gauche, le coté négatif du terrain
    if equipe > 0:
        direction_regard = 1 #robot fait face au coté négatif du terrain (angle = pi)
    if equipe < 0: 
        direction_regard = 0 #sinon robot fait face au coté positif du terrain (angle = 0)
    allier = 'blue'
    enemie = 'green'
    defenceur = client.robots[allier][2]
    attaquant = client.robots[allier][1]
    
    while True: #le match
        try:
            print(defenceur.position)
            routine_defence(client, equipe,direction_regard,defenceur,enemie,attaquant)      
        except:
            print("error Blue2")
