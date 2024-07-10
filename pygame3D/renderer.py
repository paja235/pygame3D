from mathlib import *
import pygame as pg
import copy
import loadOBJ as obj

class Camera:
    __slots__ = ('pos','rot', 'fov','n','f','proj','view', 'front', 'right')
    def __init__(self, pos: vec3 = vec3(0,0,0), rot: vec3 = vec3(0,0,0), fov: float = 90, near: float = 0.1, far: float = 100):
        self.pos = pos
        self.rot = rot
        self.fov = fov
        self.n = near
        self.f = far
        self.front = vec3(0,0,-1)
        self.front.normalize()
        self.right = vec3(0,0,-1)
        self.genView()
        self.genProj()
    def genView(self):
        self.view: mat4 = mat4()
        front = self.front
        right = self.right
        up: vec3 = front ^ right
        up.normalize()
        self.view.m = [
            [right.x, up.x, -front.x, 0],
            [right.y, up.y, -front.y, 0],
            [right.z, up.z, -front.z, 0],
            [0,0,0,1]
        ]
    def genProj(self):
        self.proj: mat4 = mat4()
        F = self.f
        N = self.n
        FOV = self.fov*PI/180
        H: float = 1/math.tan(FOV/2)
        W: float = H/(1200/800)
        self.proj.m = [
            [W,   0,   0,   0],
            [0,   H,   0,   0],
            [0,   0,  -(F+N)/(F-N),  -2*F*N/(F-N)],
            [0,   0, -1,   0],
            np.int32
        ]
        print("Generated perspective matrix")
    def Update(self):
        self.front.rotate(self.rot.y+180)
        self.right.rotate(self.rot.y+270)
        self.genView()


class DirectionalLight:
    __slots__ = ('brightness', 'col', 'dir')
    def __init__(self, brightness: float, col: tuple, dir: vec3):
        self.brightness = brightness
        self.col = col
        self.dir = dir

sunce = DirectionalLight(0,0,vec3(0,-1,0))

tris = []
def RenderScene(wn: pg.Surface, cam: Camera):
    global tris
    tris.sort()
    for tri in tris:
        tri.Render(wn, cam)
    tris.clear()
    

class Triangle:
    __slots__ = ('a', 'b', 'c', 'col')
    def __init__(self, a: vec3, b: vec3, c: vec3, col):
        self.a = copy.deepcopy(a)
        self.b = copy.deepcopy(b)
        self.c = copy.deepcopy(c)
        self.col = col
    def trans(self, wn: pg.Surface, cam: Camera):
        a = cam.proj * (cam.view * (self.a-cam.pos))
        b = cam.proj * (cam.view * (self.b-cam.pos))
        c = cam.proj * (cam.view * (self.c-cam.pos))
        if a.w < 0.00001 or b.w < 0.00001 or c.w < 0.00001:
            return
        a /= a.w
        b /= b.w
        c /= c.w
        a1 = vec3(600+a.x*600,400-a.y*400,a.z)
        b1 = vec3(600+b.x*600,400-b.y*400,b.z)
        c1 = vec3(600+c.x*600,400-c.y*400,c.z)
        tris.append(Triangle2D(a1,b1,c1,self.col))
        tris.pop()
        

class Triangle2D:
    __slots__ = ('a','b','c','o','col', 'normal')
    def __init__(self, a, b, c, normal, col):
        self.a = a
        self.b = b
        self.c = c
        self.normal = normal
        self.o = (a.z+b.z+c.z)/3
        self.col = col
        tris.append(self)
    def Render(self, wn: pg.Surface, cam: Camera):
        #if(self.normal & -vec3(cam.front.x, 0, cam.front.y) < -0.1): return
        t = max(0.2, self.normal & -sunce.dir)
        pg.draw.polygon(wn, (self.col[0]*t, self.col[1]*t, self.col[2]*t), ((self.a.x, self.a.y), (self.b.x, self.b.y), (self.c.x, self.c.y)))

    def __lt__(self, t):
        return self.o > t.o
    def __gt__(self, t):
        return self.o > t.o

class Mesh:
    __slots__ = ('vertices', 'faces')
    def __init__(self, vertices=[], faces=[]):
        self.vertices = vertices
        self.faces = faces
    @classmethod
    def fromFile(cls, path: str):
        vertices, faces = obj.loadOBJ(path)
        return cls(vertices, faces)
                
    def trans(self, wn: pg.Surface, cam: Camera):
        l = copy.deepcopy(self.vertices)
        i=0
        while(i < len(l)):
            a = cam.proj * (cam.view * (l[i]-cam.pos))
            l[i] = a / a.w
            l[i] = vec4(600+l[i].x*600,400-l[i].y*400,l[i].z, a.w)
            i += 1
        for i in self.faces:
            t1 = l[i.verts[0]]
            t2 = l[i.verts[1]]
            t3 = l[i.verts[2]]
            if t1.w < 0.00001 or t2.w < 0.00001 or t3.w < 0.00001:
                continue
                
            tris.append(Triangle2D(vec3(t1.x,t1.y,t1.z),vec3(t2.x,t2.y,t2.z),vec3(t3.x,t3.y,t3.z), i.normal, (143, 207, 227)))
            tris.pop()
            
        