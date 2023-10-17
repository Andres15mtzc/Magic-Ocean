import maya.cmds as cmds
import random

def crearGeisers(wX,wZ):
    path = "../objetos/geiser/geiser.obj"
    geisersList = []
    ############################################ Textura de arena
    #Creamos un material typo lambert
    cmds.shadingNode("lambert", asShader=True,name="texturaGeiser")
    #Abre la carpeta para escoger la imagen
    cmds.shadingNode("file",asTexture=True,name="pathImageGeiser")
    #Conectan los 2 nodos
    cmds.connectAttr("pathImageGeiser.outColor","texturaGeiser.color")
    imagePath = "../Materials/arena.jpg"
    cmds.setAttr("pathImageGeiser.fileTextureName",imagePath,type="string")
    for i in range(0,int((wX+wZ)/30)):
        #Importar objeto
        cmds.file(path,i=True,groupReference= False)
        #Renombrar objeto
        cmds.rename("pCylinder1","geiser_"+str(i))
        #Seleccionar el geiser
        cmds.select("geiser_"+str(i))
        #Acomodar el geiser
        tx=random.uniform(-wX/2, wX/2)
        tz=random.uniform(-wZ/2, wZ/2)
        cmds.move(tx,0.5,tz)
        #Crear burbujas
        geiser= crearBurbujas("geiser_"+str(i), tx, 0.5, tz, i)
        geisersList.append(geiser)
        #Asignar material al objeto
        cmds.hyperShade(assign="texturaGeiser")
        #Crear el nodo para duplicar las imagenes
        cmds.shadingNode("place2dTexture", asUtility=True,name="uvFile")
        #Conectar todo lo que hicimos al objeto
        cmds.defaultNavigation(connectToExisting=True,source="uvFile",destination="pathImageGeiser")
    cmds.group(geisersList, n="Geisers")
    #Suavizar objetos
    cmds.select("Geisers")
    cmds.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
    
