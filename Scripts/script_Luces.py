import maya.cmds as cmds
import mtoa.utils as mutils

def ponerLuces(wX,wZ):
    #Creamos la luz de arnold 
    mutils.createLocator("aiAreaLight", asLight=True)
    
    #Posicion inicial de la luz 
    cmds.setKeyframe("aiAreaLight1", at='tx' , v=-1.5*wX,t=0)
    cmds.setKeyframe("aiAreaLight1", at='ty' , v=65.593,t=0)
    cmds.setKeyframe("aiAreaLight1", at='tz' , v=-1.5*wZ,t=0)
    cmds.setKeyframe("aiAreaLight1", at='rx' , v=-48.378,t=0)
    cmds.setKeyframe("aiAreaLight1", at='ry' , v=-113.258,t=0)
    cmds.setKeyframe("aiAreaLight1", at='rz' , v=1.988,t=0)
    cmds.setKeyframe("aiAreaLight1", at='sx' , v=44.677,t=0)
    cmds.setKeyframe("aiAreaLight1", at='sy' , v=44.677,t=0)
    cmds.setKeyframe("aiAreaLight1", at='sz' , v=44.677,t=0)
    
    #Obtenemos la lista de todos las formas de luz que estan en la escena en este momento, solo obtenemos la de arnold
    dagLightTypes = list(set(cmds.nodeType("shape", derived=True, isTypeName=True)).intersection(cmds.listNodeTypes("light")))
    listaLuces = cmds.ls(type=dagLightTypes)
    
    #Color
    cmds.setAttr(listaLuces[0]+'.color',0.034,0.055,0.292) 
    
    
    if(wX >= 80 and wX<100):
        cmds.setAttr(listaLuces[0]+'.intensity',35)
        cmds.setAttr(listaLuces[0]+'.exposure',16)
       
    elif(wX >= 60 and wX<80 ):
        cmds.setAttr(listaLuces[0]+'.intensity',32)
        cmds.setAttr(listaLuces[0]+'.exposure',16)
        
    elif(wX >= 40 and wX<60):
        cmds.setAttr(listaLuces[0]+'.intensity',28)
        cmds.setAttr(listaLuces[0]+'.exposure',15)
        
    elif(wX >= 30 and wX<40):
        cmds.setAttr(listaLuces[0]+'.intensity',21.5)
        cmds.setAttr(listaLuces[0]+'.exposure',15)
  
ponerLuces(30 ,30)