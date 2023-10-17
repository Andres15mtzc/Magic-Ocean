import maya.cmds as cmds
import random

def crearArena(wX, wZ):
    #Subdivisiones en X y Z del plano
    subX,subY = 10,10
    #Condicionales para poner las subdivisiones del plano 
    if(wX >= 80):
        subX = 30
    elif(wX >= 50):
        subX = 20
    elif(wX >= 30):
        subX = 15
    if(wZ >= 80):
        subY = 30
    elif(wZ >= 50):
        subY = 20
    elif(wZ >= 30):
        subY = 15
    #Creamos el plano con las subdivisiones que salieron de las condicionales
    cmds.polyPlane(n="Arena",sx=subX,sy=subY,w=wX,h=wZ)
    #Activamos el softselect y obtenemos el máximo de vertex del plano
    cmds.softSelect(sse=1)
    maxVtx = cmds.polyEvaluate(v=True)
    #Ciclo for para randomizar el ancho del softselect y el cómo movemos los vertex desde -1 a 1
    for i in range(0,maxVtx,5):
            cmds.softSelect(ssd=random.randint(4,7))
            cmds.select("Arena.vtx["+str(i)+"]")
            cmds.move(random.randint(-1,1),y=True)
    ############################################ Textura de arena
    #Creamos un material typo lambert
    cmds.shadingNode("lambert", asShader=True,name="textura")
    #Abre la carpeta para escoger la imagen
    cmds.shadingNode("file",asTexture=True,name="pathImage")
    #Conectan los 2 nodos
    cmds.connectAttr("pathImage.outColor","textura.color")
    imagePath = "../Materials/arena.jpg"
    cmds.setAttr("pathImage.fileTextureName",imagePath,type="string")
    cmds.select("Arena")
    cmds.hyperShade(assign="textura")
    #Crear el nodo para duplicar las imagenes
    cmds.shadingNode("place2dTexture", asUtility=True,name="uvFile")
    #Conectar todo lo que hicimos al objeto
    cmds.defaultNavigation(connectToExisting=True,source="uvFile",destination="pathImage")
    #Suavizar objetos
    cmds.select("Arena")
    cmds.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
    
