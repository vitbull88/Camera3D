import pygame
import math

pygame.init()

XSIZE=800
YSIZE=800
FOV=min(XSIZE,YSIZE)
size = (XSIZE, YSIZE)

#colori
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE=(0,0,255)
PURPLE=(255,0,255)
YELLOW=(255,255,0)
LIGHT_BLUE=(0,255,255)
#colors=(RED,GREEN,BLUE,PURPLE,YELLOW,LIGHT_BLUE)

def rotate(pos,rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)
    return x*c-y*s, y*c+x*s
    


class Camera:
    
    def __init__(self, pos, rot):
        self.pos = pos
        self.rot = rot

    def mouse_control(self, event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x/=300
            y/=300
            self.rot[0] += y
            self.rot[1] += x
        
    def update(self, dt, key):
        s = dt * 10
        
        #up and down
        if key[pygame.K_q]: self.pos[1] +=s
        if key[pygame.K_e]: self.pos[1] -=s


        x,y = s*math.sin(self.rot[1]), s*math.cos(self.rot[1])
        
        # forward and backward
        if key[pygame.K_w]:
            self.pos[0] += x
            self.pos[2] += y
        if key[pygame.K_s]:
            self.pos[0] -=x
            self.pos[2] -=y

        #right and left
        if key[pygame.K_a]:
            self.pos[0] -=y
            self.pos[2] +=x
        if key[pygame.K_d]:
            self.pos[0] +=y
            self.pos[2] -=x

class Cube:
    
    vertices = (1,1,1), (-1,1,1), (-1,-1,1), (1,-1,1),(1,1,-1), (-1,1,-1), (-1,-1,-1), (1,-1,-1)
    edges = (0,1), (1,5), (4,5), (0,4), (5,6), (4,7), (0,3), (1,2), (2,6), (6,7), (3,7), (2,3)
    faces = (0,1,5,4),(1,2,6,5),(4,5,6,7),(0,3,7,4),(0,1,2,3),(2,3,7,6)
    colors=(RED,GREEN,BLUE,PURPLE,YELLOW,LIGHT_BLUE)
    
    def __init__(self,pos):
        x,y,z = pos
        self.verts = [(x+X/2,y+Y/2,z+Z/2) for X,Y,Z in self.vertices]
            


screen = pygame.display.set_mode(size)



xc = XSIZE//2
yc = YSIZE//2

#creo il titolo della finestra
pygame.display.set_caption("3D CUBE")
"""
#cubo

verts = (1,1,1), (-1,1,1), (-1,-1,1), (1,-1,1),(1,1,-1), (-1,1,-1), (-1,-1,-1), (1,-1,-1)

edges = (0,1), (1,5), (4,5), (0,4), (5,6), (4,7), (0,3), (1,2), (2,6), (6,7), (3,7), (2,3)

faces = (0,1,5,4),(1,2,6,5),(4,5,6,7),(0,3,7,4),(0,1,2,3),(2,3,7,6)"""



camera = Camera ([0, 0, -5],[0,0])

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

cubes = [Cube((0,0,0)),Cube((-2,0,0)),Cube((2,0,0))]

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        camera.mouse_control(event)
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        
        
    dt = clock.tick()/1000

    screen.fill(WHITE)

    
    """for edge in edges:
        p=[]
        for x,y,z in verts[edge[0]], verts[edge[1]]:

            x -= camera.pos[0] 
            y -= camera.pos[1]
            z -= camera.pos[2]

            x,z = rotate((x,z),camera.rot[1])
            y,z = rotate((y,z),camera.rot[0])
            
            f=200/z
            x,y=x*f,y*f
            
            p.append([xc + int(x), yc + int(y)])
            
        pygame.draw.line(screen, BLACK, p[0],p[1],1)"""

  
    face_list=[]
    face_color=[]
    depth=[]

    for obj in cubes:
    
        vert_list = []
        screen_coords = []
        
        for x,y,z in obj.verts:
            x -= camera.pos[0] 
            y -= camera.pos[1]
            z -= camera.pos[2]
            x,z = rotate((x,z),camera.rot[1])
            y,z = rotate((y,z),camera.rot[0])
            vert_list.append([x,y,z])

            f=FOV/z
            x,y=x*f,y*f
            screen_coords.append([xc+int(x),yc+int(y)])
            
     
        
        for f in range(len(obj.faces)):
            face = obj.faces[f]
            on_screen = False
            for i in face:
                x,y = screen_coords[i]
                if vert_list[i][2]>0 and x>0 and x<XSIZE and y>0 and y<YSIZE:
                    on_screen = True
                    break
            if on_screen == True:
                coords=[screen_coords[i] for i in face]
                face_list.append(coords)
                face_color.append(obj.colors[f])
                depth.append([sum(sum(vert_list[j][i] for j in face)**2 for i in range(3))])
      
    order = sorted(range(len(face_list)), key=lambda i:depth[i], reverse=1)
            

    for i in order:
        try:pygame.draw.polygon(screen, face_color[i], face_list[i])
        except:pass    
        

    key = pygame.key.get_pressed()
    camera.update(dt,key)
    pygame.display.flip()

pygame.quit()
