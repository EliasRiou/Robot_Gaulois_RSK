import math

from utils.helpers import position_du_goal_adverse

import time 






def repositionnement_robot_y(client, equipe, direction_regard, attaquant): #ah pour but de repositionner le robot si il est à un y trop près de la balle abs(yrobot-yball) < 0.15
    yball = client.ball[1]
    xrobot,yrobot = attaquant.position
    if yrobot < yball:
        arrive = False
        while not arrive == True:
            att_arrive = attaquant.goto((xrobot,yball-0.20*equipe,math.pi*direction_regard))
            arrive = att_arrive
    if yrobot > yball:
        arrive = False
        while not arrive == True:
            att_arrive = attaquant.goto((xrobot,yball+0.20*equipe,math.pi*direction_regard))
            arrive = att_arrive
    return

def repositionnement_robot_x(client, equipe, direction_regard, attaquant):
    xball,yball = client.ball
    xrobot,yrobot = attaquant.position
    if yrobot < yball:
        arrive = False
        while not arrive == True:
            att_arrive = attaquant.goto((xball+0.30*equipe,yball-0.20*equipe,math.pi*direction_regard))
            arrive = att_arrive
    if yrobot > yball:
        arrive = False
        while not arrive == True:
            att_arrive = attaquant.goto((xball+0.30*equipe,yball+0.20*equipe,math.pi*direction_regard))
            arrive = att_arrive
    return

def positionnement_kick(client, equipe, attaquant,direction_regard, enemie):
    xball,yball = client.ball
    ygoal = position_du_goal_adverse(client,enemie)
    if ygoal < 0 :
        cible_y = 0.25 #le goal est loin du y = -0.3 donc tire vers y = 0.25
    else :
        cible_y = -0.25
    theta = math.atan((cible_y-yball)/((-0.915)*equipe-xball))+math.pi*direction_regard
    x = xball-math.cos(theta)*0.15
    y = yball-math.sin(theta)*0.15
    arrive = False
    while not arrive == True:
        att_arrive = attaquant.goto((x,y,theta))
        arrive = att_arrive

def goto_kick(client, equipe, attaquant, direction_regard, enemie):
    xball,yball = client.ball
    ygoal = position_du_goal_adverse(client,enemie)
    if abs(ygoal - 0.3) > abs(ygoal + 0.3):
        cible_y = 0.25 #le goal est loin du y = -0.3 donc tire vers y = 0.25
    else :
        cible_y = -0.25
    theta = math.atan((cible_y-yball)/((-0.915)*equipe-xball))+math.pi*direction_regard
    x = xball-math.cos(theta)*0.06 #test vraie valeur 0.0823
    y = yball-math.sin(theta)*0.06
    arrive = False
    while not arrive == True:
        att_arrive = attaquant.goto((x,y,theta))
        arrive = att_arrive       
    attaquant.kick()
    time.sleep(0.2)
    
    



def routine_attaque(client,equipe,direction_regard,attaquant,enemie):
    xball,yball = client.ball
    xrobot,yrobot = attaquant.position

    if equipe == 1:
        if xball < 0.615:
            if xrobot > xball + 0.15 : # /!\ marche que pour equipe = 1
                #positionnement_kick(client, equipe, attaquant, direction_regard, enemie)
                goto_kick(client, equipe, attaquant, direction_regard, enemie)
                return
            elif abs(yrobot)-abs(yball) < 0.15 and xrobot < xball:
                repositionnement_robot_y(client, equipe, direction_regard, attaquant)
                repositionnement_robot_x(client, equipe, direction_regard, attaquant)
                goto_kick(client, equipe, attaquant, direction_regard, enemie)
                return
            positionnement_kick(client, equipe, attaquant, direction_regard, enemie)
            goto_kick(client, equipe, attaquant, direction_regard, enemie)
            return
        
        while not xball < 0.615:
            xball,yball = client.ball
            if yball < 0.3: # J'evite que le robot parte en touche
                x = 0.5 * equipe
                y = yball + 0.3
                theta = math.atan((yball-yrobot)/(xball-xrobot))
                print (theta)
                arrive = False
                while not arrive == True:
                    att_arrive = attaquant.goto((x,y,theta))
                    arrive = att_arrive 
                continue
            x = 0.5 * equipe
            y = yball - 0.3
            theta = math.atan((yball-yrobot)/(xball-xrobot))
            print (theta)
            arrive = False
            while not arrive == True:
                att_arrive = attaquant.goto((x,y,theta))
                arrive = att_arrive 
            continue

    if equipe == -1:
        if xball > -0.615:
            if xrobot < xball - 0.15: # /!\ marche que pour equipe = -1
                #positionnement_kick(client, equipe, attaquant, direction_regard, enemie)
                goto_kick(client, equipe, attaquant, direction_regard, enemie)
                return
            elif abs(yrobot)-abs(yball) < 0.15 and xrobot > xball:
                repositionnement_robot_y(client, equipe, direction_regard, attaquant)
                repositionnement_robot_x(client, equipe, direction_regard, attaquant)
                goto_kick(client, equipe, attaquant, direction_regard, enemie)
                return
            positionnement_kick(client, equipe, attaquant, direction_regard, enemie)
            goto_kick(client, equipe, attaquant, direction_regard, enemie)
            return   

    
        while not xball > -0.615:
            xball,yball = client.ball
            if yball < 0.3: # J'evite que le robot parte en touche
                x = 0.5 * equipe
                y = yball + 0.3
                theta = math.atan((yball-yrobot)/(xball-xrobot))
                arrive = False
                while not arrive == True:
                    att_arrive = attaquant.goto((x,y,theta))
                    arrive = att_arrive 
                continue
            x = 0.5 * equipe
            y = yball - 0.3
            theta = math.atan((yball-yrobot)/(xball-xrobot))
            arrive = False
            while not arrive == True:
                att_arrive = attaquant.goto((x,y,theta))
                arrive = att_arrive 
            continue
    return