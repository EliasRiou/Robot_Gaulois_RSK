import rsk
import numpy as np
import math
with rsk.Client(host='127.0.0.1', key='') as client:
    
    def dectected_adverse():
        xadv,yadv=client.robots["blue"][1].position
        if(xadv<1.83/2 and xadv>0):
            return True
        else:
            return False
    def positionIntercepte():
        xball,yball=client.ball
        xadv,yadv=client.robots["blue"][1].position
        xgoal,ygoal=client.robots["green"][2].position
        x=(xball-xadv)
        y=(yball-yadv)
        if(x==0):
            x=0.0001
        m=y/x
        p=yball-m*xball
        ygoal=m*xgoal+p
        if(intervalle(ygoal)):
            return ygoal
    def positionSimutIntercepte(xadv,yadv):
        xball,yball=client.ball
        xgoal,ygoal=client.robots["green"][2].position
        x=(xball-xadv)
        y=(yball-yadv)
        if(x==0):
            x=0.0001
        m=y/x
        p=yball-m*xball
        ygoal=m*xgoal+p
        if(intervalle(ygoal)):
            return ygoal
        else:
            return client.robots["green"][2].position[1]
    def intervalle(ygoal):
        if(ygoal<0.34 and ygoal>-0.34):
            return True
        else:
            return False
    #fonction qui créer une zone autour de la balle pour détecter si un robot rentre dans la zone
    def zone():
        xball,yball=client.ball
        xadv,yadv=client.robots["blue"][1].position
        if(xball-xadv<0.3 or xball-xadv>-0.3 or yball-yadv<0.3 or yball-yadv>-0.3):
            return True
        else:
            return False
        
    def simultJAdverse():
        xball,yball=client.ball
        orientation = client.robots["blue"][1].orientation
        xadv=xball+(math.cos(orientation))*rsk.constants.robot_radius
        yadv=yball+(math.sin(orientation))*rsk.constants.robot_radius
        return positionSimutIntercepte(xadv,yadv)  

    while True:
        try:
            if(dectected_adverse() and intervalle(simultJAdverse()) and zone()):
                client.robots["green"][2].goto((client.robots["green"][2].position[0],simultJAdverse(),np.pi), wait=False)
                client.robots["blue"][1].kick(1)
        except:
            print("error")