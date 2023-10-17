import maya.cmds as cmds
import random

def crearAlga(wX, wZ):
    ####################### Importar alga ###############################
    #Path donde se encuentran mis objetos 
    path = "../objetos/alga/"
    algasList = []
    groupList = []
    ############################################ Textura de alga
    #Creamos un material typo lambert
    cmds.shadingNode("lambert", asShader=True,name="texturaAlga")
    #Abre la carpeta para escoger la imagen
    cmds.shadingNode("file",asTexture=True,name="pathImageAlga")
    #Conectan los 2 nodos
    cmds.connectAttr("pathImageAlga.outColor","texturaAlga.color")
    imagePath = "../Materials/AlgaTextura.png"
    cmds.setAttr("pathImageAlga.fileTextureName",imagePath,type="string")
    for i in range(0,int((wX+wZ)/10)):
        varRandom = random.randint(3,9)
        for e in range(0,varRandom):
            #Importar objeto
            cmds.file(path+'alga.obj',i=True,groupReference= False)
            #Renombrar objeto
            cmds.rename("_1","alga_"+str(i)+"_"+str(e+1))
            #Seleccionar objeto y moverlo en una posicion random
            cmds.select("alga_"+str(i)+"_"+str(e+1))
            #Asignar material al objeto
            cmds.hyperShade(assign="texturaAlga")
            #Crear el nodo para duplicar las imagenes
            cmds.shadingNode("place2dTexture", asUtility=True,name="uvFile")
            #Conectar todo lo que hicimos al objeto
            cmds.defaultNavigation(connectToExisting=True,source="uvFile",destination="pathImageAlga")
            #Seleccionar objeto y moverlo en una posicion random
            cmds.select("alga_"+str(i)+"_"+str(e+1))
            #Mover alga
            cmds.move(random.randint(-5,5),random.uniform(-2,-1),random.randint(-5,5))
            #Agregarlo a la lista del grupo
            algasList.append("alga_"+str(i)+"_"+str(e+1))
            #Animar alga
            vertex1=0
            vertex2=1
            vertex3=42
            vertex4=43
            
            for j in range(0,11):                
                vertex11=str(vertex1)
                vertex22=str(vertex2)
                vertex33=str(vertex3)
                vertex44=str(vertex4)
                
                vtxObj="alga_"+str(i)+"_"+str(e+1)+".vtx["+vertex11+":"+vertex22+"]","alga_"+str(i)+"_"+str(e+1)+".vtx["+vertex33+":"+vertex44+"]"
                cmds.select(vtxObj)
                mover=-0.6
                for k in range(0, 720, 20):
                    cmds.setKeyframe(vtxObj,at="pntz",v=mover,t=(j*3)+k)
                    mover = mover*(-1)
                vertex1=vertex1+2
                vertex2=vertex2+2
                vertex3=vertex3-2
                vertex4=vertex4-2
                    
        #Crear el grupo con toda la lista de objetos
        cmds.group( algasList, name='algas_'+str(i))
        cmds.select('algas_'+str(i))
        #Mover el grupo a una posicion random
        cmds.move(random.randint(-wX/2+5,wX/2-5),0,random.randint(-wZ/2+5,wZ/2-5))
        groupList.append('algas_'+str(i))
        algasList= []
    #Crear el grupo padre para limpiar el outliner
    cmds.group( groupList, name='Algas')
    groupList= [] 
    #Suavizar objetos
    cmds.select("Algas")
    cmds.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)