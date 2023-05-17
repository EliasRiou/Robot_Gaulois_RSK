import math

from utils.helpers import position_du_goal_adverse


from defense.defense_joueur import go_to_ball_droit_kick_centre



def go_to_ball_arc_kick_centre(client,equipe,direction_regard,robot):
    xball, yball = client.ball
    xrobot, yrobot = robot.position
    if equipe == 1: #!!! il faut tester de quel coté est quel couleur, c'est peut être l'inverse.
        xadv1, yadv1 = client.blue1.position #on récupère la position des robots adverse, on peut aussi avoir besoin de la position de l'autre robot allier
        xadv2, yadv2 = client.blue2.position
    else:
        xadv1, yadv1 = client.green1.position
        xadv2, yadv2 = client.green2.position
    if (yadv1 > yball and yadv1 < yball+0.25 and xadv1 < xball+0.25 and xadv1 > xball-0.25) or (yadv2 > yball and yadv2 < yball+0.25 and xadv2 < xball+0.25 and xadv2 > xball-0.25): #l'espace est encombré en y+
        robot.goto((xball,yball-0.20,direction_regard*math.pi)) #première étape de déplacement - esquive 
        robot.goto((xball-0.20*equipe,yball,direction_regard*math.pi)) #deuxième étape de déplacement - alignement
        robot.goto((xball+0.0823*equipe,yball,(direction_regard*math.pi))) #troisième étape de déplcement - approche kick
        robot.kick()
    elif yadv1 < yball and yadv1 > yball-0.25 and xadv1 < xball+0.25 and xadv1 > xball-0.25 or yadv2 < yball and yadv2 > yball-0.25 and xadv2 < xball+0.25 and xadv2 > xball-0.25: #l'espace est encombré en y-
        robot.goto((xball,yball+0.20,direction_regard*math.pi)) #première étape de déplacement - esquive 
        robot.goto((xball-0.20*equipe,yball,direction_regard*math.pi)) #deuxième étape de déplacement - alignement
        robot.goto((xball+0.0823*equipe,yball,(direction_regard*math.pi))) #troisième étape de déplcement - approche kick
        robot.kick()
    elif yrobot > 0: # ??
        robot.goto((xrobot,0.5,direction_regard*math.pi)) #retour en defence par le coté selon le côté
        robot.goto((equipe*0.8,0.5,direction_regard*math.pi))
    else:
        robot.goto((xrobot,-0.5,direction_regard*math.pi))
        robot.goto((equipe*0.8,-0.5,direction_regard*math.pi))
    return

def go_to_ball_droit_kick_cadre(client,equipe,direction_regard,robot,enemie): #fonction kick vers les cages     absolument tester sur le simulateur
    xball, yball = client.ball
    ygoal = position_du_goal_adverse(client,enemie)
    xrobot, yrobot = robot.position
    if abs(ygoal - 0.3) > abs(ygoal + 0.3):
        cible_y = 0.25 #le goal est loin du y = -0.3 donc tire vers y = 0.25
    else :
        cible_y = -0.25 #le goal est loin du y = 0.3 donc tire vers y = -0.25
    
    #if yball-yrobot > 0.18 and xrobot*equipe < xball*equipe:
        #robot.goto((xball+0.18*equipe,yball,math.pi*direction_regard),wait = False )

    nextPosition = {
       'x': xball+0.0823*equipe,
       'y': yball,
       'theta': math.atan((cible_y-yball)/(equipe*-0.915-xball))+math.pi*direction_regard
    }
    needsKick = False

    if yball-yrobot >= 0.09 and xrobot*equipe < xball*equipe:
        nextPosition['x'] = xball+0.15*equipe
        nextPosition['y'] = yrobot
        nextPosition['theta'] = math.pi*direction_regard
    elif yball-yrobot <= 0.09 and yball < yrobot and xrobot*equipe < xball*equipe:
        nextPosition['x'] = xball+0.15*equipe
        nextPosition['y'] = yrobot + 0.09 - abs(yball - yrobot)
        nextPosition['theta'] = math.pi*direction_regard
    elif yball-yrobot <= 0.09 and yball > yrobot and xrobot*equipe < xball*equipe:
        nextPosition['x'] = xball+0.15*equipe
        nextPosition['y'] = yrobot - 0.09 - abs(yball - yrobot)
        nextPosition['theta'] = math.pi*direction_regard
    else:
        needsKick = True
    
    robot.goto((
        nextPosition['x'], 
        nextPosition['y'], 
        nextPosition['theta']
    ))
    if needsKick:
        robot.kick()
    return

def nb_enemies_preempter(client, enemie):
    xadv1, yadv1 = client.robots[enemie][1].position #on récupère la position des robots adverse
    xadv2, yadv2 = client.robots[enemie][2].position
    nombre_robot_preempter = 0
    if abs(yadv1) > 0.60:
        nombre_robot_preempter = nombre_robot_preempter + 1
    if abs(yadv2) > 0.60:
        nombre_robot_preempter = nombre_robot_preempter + 1
    return (nombre_robot_preempter)

def attanquant_preempter(robot):
    xrobot, yrobot = robot.position
    if abs(yrobot) > 0.60:
        return True
    else:
        return False

def attaque(client, equipe,direction_regard,attaquant,enemie):
    xball = client.ball[0]
    xatt = attaquant.position[0]
    print(xball,xatt)
    if xball*equipe < 0 and xatt*equipe > xball*equipe:
        go_to_ball_droit_kick_cadre(equipe,direction_regard,attaquant,enemie)
    elif xball*equipe > 0 and xatt*equipe > xball*equipe:
        go_to_ball_droit_kick_centre(equipe,direction_regard,attaquant)
    else:
        go_to_ball_arc_kick_centre(equipe,direction_regard,attaquant)#a améliorer 
    return