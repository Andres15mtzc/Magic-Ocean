import maya.cmds as cmds
import math
import array as arr
import random

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
    