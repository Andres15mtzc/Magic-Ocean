import maya.cmds as cmds
import math
import random
import array as arr
import mtoa.utils as mutils

class M_Window(object):
    #constructor
    def __init__(self):
        self.window= "ArenaWindow"
        self.title= "Sand Creator"
        self.size= (300, 300)
        self.wX= 0
        self.wZ= 0
        self.Peces= 0
        
        #close old window if its opened
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)
        self.resetScene()  
          
        #Create window
        self.window= cmds.window(self.window, title=self.title, widthHeight=self.size)
        
        #Create layout
        cmds.columnLayout()
        self.valuewX= cmds.text(l="Lenght of the sand")
        self.valwX= cmds.intField(minValue=30, maxValue=100, value=30)
        self.valuewZ= cmds.text(l="Widht of the sand")
        self.valwZ= cmds.intField(minValue=30, maxValue=100, value=30)
        #self.slider= cmds.intSlider(min=1, max=30, value=0, step=1)
        self.createSandBtn= cmds.button(l="Generate Sand", c=self.createSand)
        #Reset Scene
        self.resetSceneBtn= cmds.button(l="Reset Scene", c=self.resetScene)
        #Close
        self.closeBtn= cmds.button(l="Close", c=self.closeUI)
        
        cmds.showWindow()
        
    def createSand(self, *args):
        self.wX= cmds.intField(self.valwX, query=True, value=True)
        self.wZ= cmds.intField(self.valwZ, query=True, value=True)
        #Crear la arena
        crearArena(self.wX, self.wZ)
        
        #Cambiar el UI
        
        #close old window if its opened
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)
            
        #Create window
        self.window= cmds.window(self.window, title=self.title, widthHeight=self.size)
        
        #Create layout
        cmds.columnLayout()
        #Algas
        self.createAlgasBtn= cmds.button(l="Add Algas", c=self.createAlga )
        #Geisers
        self.createGeisersBtn= cmds.button(l="Add Geisers", c=self.createGeisers )
        #Camara
        self.createCameraBtn= cmds.button(l="Add camera", c=self.createCamera )
        #Luz
        self.createLuzBtn= cmds.button(l="Add light", c=self.createLuz )
        #Peces
        self.numberPeces= cmds.text(l="Number of fishes")
        self.noPeces= cmds.intField(minValue=0, maxValue=20, value=0)
        self.createAlgasBtn= cmds.button(l="Add Fishes", c=self.createPeces )
        #Close
        self.closeBtn= cmds.button(l="Close", c=self.closeUI)
        
        cmds.showWindow()
    
    def createAlga(self, *args):
        crearAlga(self.wX, self.wZ)
    
    def createGeisers(self, *args):
        crearGeisers(self.wX, self.wZ)
    def createLuz(self, *args):
        ponerLuces(self.wX, self.wZ)
    def createCamera(self, *args):
        ponerCamara(self.wX, self.wZ)
        
    def createPeces(self, *args):
        self.Peces= cmds.intField(self.noPeces, query=True, value=True)
        crearPeces(self.wX, self.wZ, self.Peces)
        
    def resetScene(self, *args):
        cmds.file(force=True,newFile = True)
        
    def closeUI(self, *args):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)
            
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
    
def crearBurbujas(geiser, tx, ty, tz, i):
    cmds.particle( p=((tx,ty,tz)), n='particles_'+str(i))
    cmds.emitter( 'particles_'+str(i), r=2, n='emitter_'+str(i), type="dir", dx=0, dy=1, dz=0, sp=0.2, spd=5)
    cmds.nParticle( n='emitted_'+str(i))
    #Modificar emitted
    cmds.setAttr('emitted_'+str(i)+'Shape.radius', 0.5)
    cmds.setAttr('emitted_'+str(i)+'Shape.particleRenderType', 4)
    cmds.setAttr('emitted_'+str(i)+'Shape.ignoreSolverGravity', 1)
    cmds.setAttr('emitted_'+str(i)+'Shape.opacity', 0.4)
    cmds.setAttr('emitted_'+str(i)+'Shape.color[0].color_Color', 0.2714,0.2972,0.8143)
    cmds.setAttr('emitted_'+str(i)+'Shape.lifespanMode', 2)
    cmds.setAttr('emitted_'+str(i)+'Shape.lifespan', 10)
    cmds.setAttr('emitted_'+str(i)+'Shape.lifespanRandom', 3)
    cmds.setAttr('emitted_'+str(i)+'Shape.collide', 0)
    #Connect the emitter with the emitted
    cmds.connectDynamic( 'emitted_'+str(i), em='emitter_'+str(i))
    cmds.group(geiser, 'particles_'+str(i), 'emitted_'+str(i), n="geiserGroup_"+str(i)) 
    return "geiserGroup_"+str(i)

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
    print("aaaaa")
    print(wX)
    if(wX >= 80):
        cmds.setAttr(listaLuces[0]+'.intensity',35)
        cmds.setAttr(listaLuces[0]+'.exposure',16)
       
    elif(wX >= 60):
        cmds.setAttr(listaLuces[0]+'.intensity',32)
        cmds.setAttr(listaLuces[0]+'.exposure',16)
        
    elif(wX >= 40):
        cmds.setAttr(listaLuces[0]+'.intensity',28)
        cmds.setAttr(listaLuces[0]+'.exposure',15)
        
    elif(wX >= 30):
        cmds.setAttr(listaLuces[0]+'.intensity',21.5)
        cmds.setAttr(listaLuces[0]+'.exposure',15)
      
myWindow= M_Window()
