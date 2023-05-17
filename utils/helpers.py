import math

def suivre_balle_regard(client, equipe, direction_regard,robot,enemie): 
    xball, yball = client.ball

    x_robot_adv_1,y_robot_adv_1 = client.robots[enemie][1]
    x_robot_adv_2,y_robot_adv_2 = client.robots[enemie][2]
    dis1 = math.sqrt((xball - x_robot_adv_1)**2)+math.sqrt((yball - y_robot_adv_1)**2)
    dis2 = math.sqrt((xball - x_robot_adv_2)**2)+math.sqrt((yball - y_robot_adv_2)**2)
    if abs(dis1) < abs(dis2):
        x, y, theta = client.robots[enemie][1] #je voudrais récupérer uniquement l'angle [2]
    else:
        x, y, theta = client.robots[enemie][2] #faire mieux sans else
    
    
    xrobot, yrobot = robot.position
    if abs(yrobot + math.sin(theta)*(0.915*equipe-xrobot)) < 0.3:
        arrive = False
        while not arrive == True: #goto que si la balle peut entrer dans les cages
            att_arrive = robot.goto((equipe*0.915,yrobot + math.sin(theta)*(0.915*equipe-xrobot),(direction_regard*math.pi+theta)))
            arrive = att_arrive
    if abs(xrobot)-abs(xball) < 0.09:
        robot.kick()
    return

def suivre_balle(client, equipe, direction_regard,robot): #ajouter limite des cages ?
    xball, yball = client.ball
    xrob, yrob = robot.position
    robot.goto((equipe*0.915,yball,(direction_regard*math.pi)))
    return
    
    
    return

def regarder_balle(direction_regard, balle, position_defenseur):
    xball,yball = balle
    xdef,ydef = position_defenseur
    return direction_regard*math.pi+math.atan((ydef-yball)/(xdef-xball))

def distance_ennemie(client, enemie):
    xadv1, yadv1 = client.robots[enemie][1].position #on récupère la position des robots adverse
    xadv2, yadv2 = client.robots[enemie][2].position
    xball, yball = client.ball
    xdis1 = xadv1 - xball
    ydis1 = yadv1 - yball
    xdis2 = xadv2 - xball
    ydis2 = yadv2 - yball  #mesure de la distance x,y des deux robot par rapport à la balle -> pythagore
    dis1 = math.sqrt(xdis1**2+ydis1**2)
    dis2 = math.sqrt(xdis2**2+ydis2**2)
    return min(dis1,dis2) #retourne la plus petite valeur

def position_du_goal_adverse(client, enemie):#peut être devoir ajouter des conditions -position x du goal
    xball, yball = client.ball
    xadv1, yadv1 = client.robots[enemie][1].position #on récupère la position des robots adverse
    xadv2, yadv2 = client.robots[enemie][2].position
    if abs(xadv1 - 0.9)  < abs(xadv2 - 0.9): #test quel robot est le plus près des cages, risque de défaut si les deux robots sont près des cages
        return yadv1 #retourne la position en y du "goal"
    return yadv2

def ennemie_le_plus_près(client, enemie):
    xadv1, yadv1 = client.robots[enemie][1].position #on récupère la position des robots adverse
    xadv2, yadv2 = client.robots[enemie][2].position
    xball, yball = client.ball
    xdis1 = xadv1 - xball
    ydis1 = yadv1 - yball
    xdis2 = xadv2 - xball
    ydis2 = yadv2 - yball  #mesure de la distance x,y des deux robot par rapport à la balle -> pythagore
    dis1 = math.sqrt(xdis1**2+ydis1**2)
    dis2 = math.sqrt(xdis2**2+ydis2**2)
    if dis1 < dis2:
        return 1 #retourne le numéro de l'adv le plus près de la balle 
    return 2
