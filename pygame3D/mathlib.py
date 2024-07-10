import math
import numpy as np
import copy

PI: float = 3.14159265358979323

class vec2:
    __slots__ = ('x','y')
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def print(self):
        print("vec2 ", self.x, self.y)
    def __truediv__(self, f: float):
        return vec2(self.x/f, self.y/f)
    def __mul__(self, f: float):
        return vec2(self.x*f, self.y*f)
    def mag(self) -> float:
        return math.sqrt(self.x*self.x+self.y*self.y)
    def normalize(self):
        m = self.mag()
        if(m != 0): self /= self.mag()
    def rotate(self, o):
        self.y = math.cos(o*PI/180)
        self.x = math.sin(o*PI/180)
class vec3:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    def print(self):
        print("vec3 ", self.x, self.y, self.z)
    def __add__(self, v):
        return vec3(self.x+v.x, self.y+v.y, self.z+v.z)
    def __sub__(self, v):
        return vec3(self.x-v.x, self.y-v.y, self.z-v.z)
    def __mul__(self, f: float):
        return vec3(self.x*f, self.y*f, self.z*f)
    def __truediv__(self, f: float):
        return vec3(self.x/f, self.y/f, self.z/f)
    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)
    def __xor__(self, v):
        return vec3(self.y*v.z-self.z*v.y, self.z*v.x-self.x*v.z, self.x*v.y-self.y*v.x)
    def __and__(self, v):
        return (self.x*v.x+self.y*v.y+self.z*v.z)
    def mag(self) -> float:
        return math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    def normalize(self):
        m = self.mag()
        if(m != 0): self /= self.mag()
    def rotate(self, o):
        self.z = math.cos(o*PI/180)
        self.x = math.sin(o*PI/180)
class vec4:
    __slots__ = ('x', 'y', 'z', 'w')
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    def print(self):
        print("vec ", self.x, self.y, self.z, self.w)
    def __truediv__(self, f: float):
        return vec4(self.x/f, self.y/f, self.z/f, self.w/f)

def mmul(mat1, mat2):
    result: mat4 = mat4()
    for i in range(4):
        for j in range(4):
            result.m[i][j] = sum(mat1.m[i][k] * mat2.m[k][j] for k in range(4))
    return result.m

class mat4:
    __slots__ = ('m')
    def __init__(self):
        self.m = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], np.float32)
    def translate(self, v: vec3):
        r: mat4 = mat4()
        r.m[0,3] = v.x
        r.m[1,3] = v.y
        r.m[2,3] = v.z
        self.m = mmul(self, r)
    def rotate(self, o):
        r: mat4 = mat4()
        r.m[0][0] =  math.cos(o*PI/180)
        r.m[0][2] =  math.sin(o*PI/180)
        r.m[2][0] = -math.sin(o*PI/180)
        r.m[2][2] =  math.cos(o*PI/180)
        self.m = mmul(self, r)
    def __mul__(self, v: vec4) -> vec4:
        r: vec4 = vec4(0,0,0,0)
        m = self.m
        r.x = v.x*m[0][0] + v.y*m[0][1] + v.z*m[0][2] + v.w*m[0][3]
        r.y = v.x*m[1][0] + v.y*m[1][1] + v.z*m[1][2] + v.w*m[1][3]
        r.z = v.x*m[2][0] + v.y*m[2][1] + v.z*m[2][2] + v.w*m[2][3]
        r.w = v.x*m[3][0] + v.y*m[3][1] + v.z*m[3][2] + v.w*m[3][3]
        return r
    def __mul__(self, v: vec3) -> vec4:
        r: vec4 = vec4(0,0,0,0)
        m = self.m
        r.x = v.x*m[0][0] + v.y*m[0][1] + v.z*m[0][2] + m[0][3]
        r.y = v.x*m[1][0] + v.y*m[1][1] + v.z*m[1][2] + m[1][3]
        r.z = v.x*m[2][0] + v.y*m[2][1] + v.z*m[2][2] + m[2][3]
        r.w = v.x*m[3][0] + v.y*m[3][1] + v.z*m[3][2] + m[3][3]
        return r
