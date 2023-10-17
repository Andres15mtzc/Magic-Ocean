
def ponerCamara(wX,wZ):
    #crear Camara
    cmds.camera(name="camara1")
    cmds.setKeyframe("camara1", at='tx' , v=-wX/2,t=0)
    cmds.setKeyframe("camara1", at='ty' , v=4.688,t=0)
    cmds.setKeyframe("camara1", at='tz' , v=-wZ/4,t=0)
    cmds.setKeyframe("camara1", at='rx' , v=4.2,t=0)
    cmds.setKeyframe("camara1", at='ry' , v=-117.6,t=0)
    
    #Poner vista de la camara
    cmds.lookThru("camara1")

ponerCamara(30 ,30)