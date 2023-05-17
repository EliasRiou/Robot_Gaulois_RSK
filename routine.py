import rsk
from defense.defense_joueur import routine_defence
from attaque.attaque_joueur import routine_attaque


with rsk.Client(host='127.0.0.1', key='') as client:

    #setup
    equipe = 1 #ou -1 si on joue du coté gauche, le coté négatif du terrain
    if equipe > 0:
        direction_regard = 1 #robot fait face au coté négatif du terrain (angle = pi)
    if equipe < 0: 
        direction_regard = 0 #sinon robot fait face au coté positif du terrain (angle = 0)
    allier = 'green'
    enemie = 'blue'
    attaquant = client.robots[allier][1]
    defenceur = client.robots[allier][2]
    
    while True: #le match
        routine_attaque(client,equipe, direction_regard, attaquant,enemie)
        routine_attaque(client,-1,0, client.blue1, 'green')
        routine_defence(client,-1,0, client.blue2,"green")
        routine_defence(client,equipe,direction_regard,defenceur,enemie)

        # try:
        #     go_to_ball_droit_kick_cadre(client,equipe, direction_regard, attaquant,enemie)
        #     go_to_ball_droit_kick_cadre(client,-1,0, client.blue1, 'green')
        #     routine_defence(client,-1,0, client.blue2,"green")
        #     routine_defence(client,equipe,direction_regard,defenceur,enemie)
            

        # except :
        #     print ("error : no matching actions found") 
        