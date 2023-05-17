
from utils.helpers import distance_ennemie, ennemie_le_plus_près, suivre_balle
from attaque.attaque_joueur import positionnement_kick
from attaque.attaque_joueur import goto_kick
import math
import time

def vitesse_balle(client):
    xball, yball = client.ball
    time.sleep(0.2)

    xball2, yball2 = client.ball

    hyp = math.sqrt((xball2-xball)**2+(yball2-yball)**2)
    print("hey2")
    vitesse_ball = hyp*5 #le *5 est l'inverse de /0.2

    return vitesse_ball

def balle_mouvement(client): #Retourne True si la balle est en mouvement ( > 0.2 m/s )
    if vitesse_balle(client) < 0.30:
        print("balle immobile")
        return False #Retourne False si la balle est immobile ( < 0.2 m/s )
    print ("balle en mouvement")
    return True 


def prediction_balle(client,equipe,defenceur):
    xball, yball = client.ball
    xrobot,yrobot = defenceur.position
    time.sleep(0.2)
    xball2, yball2 = client.ball
    theta = math.atan((yball2-yball)/(xball2-xball))
    return (yball2 + math.sin(theta)*(0.915*equipe-xball2)) # es-ce que la balle arrive dans les cages y = yball2 + sin (la composante en y) x R rayon = distance = +-0.915 - xball2

def go_to_ball_droit_kick_centre(client,equipe,direction_regard,robot): #on peut changer la direction de ce kick selon la stratégie
    xball, yball = client.ball
    robot.goto((xball+0.0823*equipe,yball,(direction_regard*math.pi)))
    robot.kick()
    return 

def degagement_zone_defence(client,equipe,direction_regard,defenceur,enemie):
    vitesse_ball = vitesse_balle(client)
    if vitesse_ball < 0.2: #on considère la balle immobile
        #positionnement_kick(client, equipe, defenceur, direction_regard, enemie) #si besoin après test
        goto_kick(client, equipe, defenceur, direction_regard, enemie)

#and distance_ennemie(client,enemie) > 0.30

def goal_volant(client,equipe,defenceur):
    xball,yball = client.ball
    xrobot,yrobot = defenceur.position
    if equipe == 1:
        if xball < 0.45 or xball>0.515 and xball<0.915: #marche pas chez l'aversaire
            distance_x = 0.45 - xball
            pourcentage = distance_x/1.365
            x = 0.915 - 0.465 * pourcentage
            y = yball * (1-pourcentage-0.2)
            theta = math.atan((yball-yrobot)/(xball-xrobot))
            arrive = False
            while not arrive == True:
                att_arrive = defenceur.goto((x,y,math.pi + theta))
                arrive = att_arrive
            return True
    if equipe == -1:
        if xball > -0.45 or xball<-0.515 and xball>-0.915: #marche pas chez l'aversaire
            distance_x = xball + 0.45
            pourcentage = distance_x/1.365
            x = -0.915 + 0.465 * pourcentage
            y = yball * (1-pourcentage-0.2)
            theta = math.atan((yball-yrobot)/(xball-xrobot))
            arrive = False
            while not arrive == True:
                att_arrive = defenceur.goto((x,y,theta))
                arrive = att_arrive
            return True
    return False


def routine_defence(client, equipe,direction_regard,defenceur,enemie,attaquant):
    print("def")
    xball, yball = client.ball
    # il faut copier le code pour l'equipe -1
    # la prédisction ne marche et bloque le robot
    if equipe == 1:

                #BUT POTENTIEL /!\ 1 time.sleep 0.2
        
        y_but_potentiel = prediction_balle(client,equipe,defenceur) #1 time.sleep 0.2
        if abs(y_but_potentiel) < 0.3:
            arrive = False
            while not arrive == True:
                att_arrive = defenceur.goto((0.915*equipe,y_but_potentiel,math.pi*direction_regard))
                arrive = att_arrive
            return

        #SURFACE DE REPARATION

        if xball > 0.515  and abs(yball) < 0.45: #quand le x de la balle passe le x de la surface de réparation et y surface rep    /!\ N'est pas le même opur equipe = -1
            # print("surface de reparation")
            if balle_mouvement(client) == False:
                positionnement_kick(client, equipe, defenceur, direction_regard, enemie) #crash ici
                goto_kick(client, equipe, defenceur, direction_regard, enemie)
                # print("degagement lent")
                return
            elif vitesse_balle(client) < 0.7: #Pour que le goal réagisse plus vite à la balle : en dessous de 0.7 m/s je considère que ce n'est plus un tir et que le mieux à faire et de lui foncer dessus
                start_time = time.monotonic() #Pendant 0.3 secondes
                # print("go_to_rapide")
                while (time.monotonic()-start_time)<0.3: #Test pour forcer le goal à garder un comportement pendant une durée
                    # print(time.time())
                    xball,yball = client.ball
                    x = xball - 0.0823 #un peu derrière pour pouvoir la pousser dans le bon sens (ou ratrapper le retard caméra)
                    y = yball 
                    z = math.pi*direction_regard
                    att_arrive = defenceur.goto((x,y,z))
                    arrive = att_arrive
                return
            

        #DEGAGEMENT ATTAQUANT PREEMPTER

        if distance_ennemie(client, enemie) > 0.2 and abs(attaquant.position[1]) >0.58: #Degagement
                goto_kick(client,equipe,defenceur,direction_regard,enemie)
                return
               
        if abs(client.robots[enemie][ennemie_le_plus_près(client,enemie)].position[1]) >0.58 and abs(attaquant.position[1]) >0.58: #Degagement
            goto_kick(client,equipe,defenceur,direction_regard,enemie)
            return
               

        

        #GOAL VOLANT

        if goal_volant(client,equipe,direction_regard,defenceur) != False:

            goal_volant(client,equipe,direction_regard,defenceur)
            return
        suivre_balle(client,equipe,direction_regard,defenceur)
         

        


        
        return

            

    if equipe == (-1):

        #BUT POTENTIEL /!\ 1 time.sleep 0.2
        
        y_but_potentiel = prediction_balle(client,equipe,defenceur) #1 time.sleep 0.2
        if abs(y_but_potentiel) < 0.3:
            arrive = False
            while not arrive == True:
                att_arrive = defenceur.goto((0.915*equipe,y_but_potentiel,math.pi*direction_regard))
                arrive = att_arrive
            return


        #SURFACE DE REPARATION

        if xball < -0.515  and abs(yball) < 0.45: #quand le x de la balle passe le x de la surface de réparation et que les robots adverse ne sont pas trop proche
            # print("surface de reparation")
            if balle_mouvement(client) == False:
                positionnement_kick(client, equipe, defenceur, direction_regard, enemie) #crash ici
                goto_kick(client, equipe, defenceur, direction_regard, enemie)
                # print("degagement lent")
                return
            elif vitesse_balle(client) < 0.7: #Pour que le goal réagisse plus vite à la balle : en dessous de 0.7 m/s je considère que ce n'est plus un tir et que le mieux à faire et de lui foncer dessus
                start_time = time.monotonic()
                # print("go_to_rapide")
                while (time.monotonic()-start_time)<0.3: #Test pour forcer le goal à garder un comportement pendant une durée
                    xball,yball = client.ball
                    x = xball - 0.0823 #un peu derrière pour pouvoir la pousser dans le bon sens (ou ratrapper le retard caméra)
                    y = yball 
                    z = math.pi*direction_regard
                    att_arrive = defenceur.goto((x,y,z))
                    arrive = att_arrive
                return
            

        #DEGAGEMENT ATTAQUANT PREEMPTER

        if distance_ennemie(client, enemie) > 0.2 and abs(attaquant.position[1]) >0.58: #Degagement
                goto_kick(client,equipe,defenceur,direction_regard,enemie)
                return
               

        if abs(client.robots[enemie][ennemie_le_plus_près(client,enemie)].position[1]) >0.58 and abs(attaquant.position[1]) >0.58: #Degagement
            goto_kick(client,equipe,defenceur,direction_regard,enemie)
            return
               

        

        #GOAL VOLANT

        if goal_volant(client,equipe,direction_regard,defenceur) != False:

            goal_volant(client,equipe,direction_regard,defenceur)
            return
        suivre_balle(client,equipe,direction_regard,defenceur)
         

        


        return
