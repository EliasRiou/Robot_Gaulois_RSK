import rsk

from defense.defense_joueur import routine_defence
from attaque.attaque_joueur import routine_attaque

#wz5xcs
with rsk.Client(host='192.168.0.101', key='') as client:

    #setup
    equipe = 1 #ou -1 si on joue du coté gauche, le coté négatif du terrain
    if equipe > 0:
        direction_regard = 1 #robot fait face au coté négatif du terrain (angle = pi)
    if equipe < 0: 
        direction_regard = 0 #sinon robot fait face au coté positif du terrain (angle = 0)
    allier = 'blue'
    enemie = 'green'
    attaquant = client.robots[allier][1]
        
    while True: #le match
        try:
            routine_attaque(client,equipe, direction_regard, attaquant,enemie)
        except:
            print("error Blue1 : Préemption")
        # try:
        #     go_to_ball_droit_kick_cadre(client,equipe, direction_regard, attaquant,enemie)
            #     go_to_ball_droit_kick_cadre(client,-1,0, client.blue1, 'green')
            #     routine_defence(client,-1,0, client.blue2,"green")
            #     routine_defence(client,equipe,direction_regard,defenceur,enemie)
                

            # except :
            #     print ("error : no matching actions found") 