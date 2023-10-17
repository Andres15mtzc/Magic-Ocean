import maya.cmds as cmds
import random

def crearPeces(wX, wZ, number):
    #Path donde se encuentran mis objetos 
    pathObj = "../objetos/peces/"
    pathMat = "../Materials/"
    pathList= ["pezAmarillo", "pezAzul", "pezNaranja", "pezPayaso"]
    pecesList = []
    
    ############################################ Textura de pezAmarillo
    #Creamos un material typo lambert
    cmds.shadingNode("lambert", asShader=True,name="texturapezAmarillo")
    #Abre la carpeta para escoger la imagen
    cmds.shadingNode("file",asTexture=True,name="pathImagepezAmarillo")
    #Conectan los 2 nodos
    cmds.connectAttr("pathImagepezAmarillo.outColor","texturapezAmarillo.color")
    imagePath = "../Materials/pezAmarillo.jpg"
    cmds.setAttr("pathImagepezAmarillo.fileTextureName",imagePath,type="string")
    
    ############################################ Textura de pezAzul
    #Creamos un material typo lambert
    cmds.shadingNode("lambert", asShader=True,name="texturapezAzul")
    #Abre la carpeta para escoger la imagen
    cmds.shadingNode("file",asTexture=True,name="pathImagepezAzul")
    #Conectan los 2 nodos
    cmds.connectAttr("pathImagepezAzul.outColor","texturapezAzul.color")
    imagePath = "../Materials/pezAzul.jpg"
    cmds.setAttr("pathImagepezAzul.fileTextureName",imagePath,type="string")
    
    ############################################ Textura de pezNaranja
    #Creamos un material typo lambert
    cmds.shadingNode("lambert", asShader=True,name="texturapezNaranja")
    #Abre la carpeta para escoger la imagen
    cmds.shadingNode("file",asTexture=True,name="pathImagepezNaranja")
    #Conectan los 2 nodos
    cmds.connectAttr("pathImagepezNaranja.outColor","texturapezNaranja.color")
    imagePath = "../Materials/pezNaranja.jpg"
    cmds.setAttr("pathImagepezNaranja.fileTextureName",imagePath,type="string")
    
    ############################################ Textura de pezPayaso
    #Creamos un material typo lambert
    cmds.shadingNode("lambert", asShader=True,name="texturapezPayaso")
    #Abre la carpeta para escoger la imagen
    cmds.shadingNode("file",asTexture=True,name="pathImagepezPayaso")
    #Conectan los 2 nodos
    cmds.connectAttr("pathImagepezPayaso.outColor","texturapezPayaso.color")
    imagePath = "../Materials/pezPayaso.jpg"
    cmds.setAttr("pathImagepezPayaso.fileTextureName",imagePath,type="string")
    
    for i in range(0,number):
        ####################### Importar pez ###############################
        varRandom = random.randint(0,3)
        #Importar objeto
        pez= pathList[varRandom]
        cmds.file(pathObj+pez+"/"+pez+".obj",i=True,groupReference= False)
        #Renombrar objeto
        cmds.rename("pez1","pez_"+str(i))
        #Seleccionar objeto y moverlo en una posicion random
        cmds.select("pez_"+str(i))
        #Asignar material al objeto
        cmds.hyperShade(assign="textura"+pez)
        #Crear el nodo para duplicar las imagenes
        cmds.shadingNode("place2dTexture", asUtility=True,name="uvFile")
        #Conectar todo lo que hicimos al objeto
        cmds.defaultNavigation(connectToExisting=True,source="uvFile",destination="pathImage"+pez)
        #Agregar al grupo
        pecesList.append("pez_"+str(i))
        #Seleccionar el pez
        cmds.select("pez_"+str(i))
        #Acomodar el pez
        cmds.setAttr(".ry", 90)
        size= random.randint(1,2)
        cmds.scale(size,size,size)
        cmds.move(random.randint(int(-wX/2), int(wX/4)),random.uniform(2, 10),random.randint(int(-wZ/4), int(wZ/2)))
        #Animar pez
        tz= cmds.getAttr(".tz")
        cmds.setKeyframe(at="tz", v=tz, t=0)
        cmds.setKeyframe(at="tz", v=-wZ, t=random.randint(200,400))
    cmds.group(pecesList, n="Peces")
    #Suavizar objetos
    cmds.select("Peces")
    cmds.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
    
