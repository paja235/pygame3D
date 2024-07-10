
from mathlib import *

class Face:
    __slots__ = ('verts', 'normal')
    def __init__(self):
        self.verts = []

def loadOBJ(file_path):
    vertices = []
    normals = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            parts = line.split()
            if parts[0] == 'v':
                # Vertex coordinates
                v = tuple(map(float, parts[1:4]))
                vertices.append(vec3(v[0],v[1],v[2]))
            elif parts[0] == 'vn':
                # Vertex normals
                v = tuple(map(float, parts[1:4]))
                normals.append(vec3(v[0],v[1],v[2]))
            elif parts[0] == 'f':
                # Face indices
                face = Face()
                for p in parts[1:]:
                    indices = p.split('/')
                    vertex_index = int(indices[0]) - 1
                    normal_index = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else None
                    face.verts.append(vertex_index)
                    face.normal = normals[normal_index]
                faces.append(face)

    return vertices, faces
