"""
COSC 4370 Homework #4
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import numpy as np

def load_obj(file_name):
    scene = pywavefront.Wavefront(file_name, collect_faces=True)
    vertices = scene.vertices
    faces = []
    for mesh in scene.mesh_list:
        for face in mesh.faces:
            faces.append(face)
    return vertices, faces

def compute_normals(vertices, faces):
    normals = []
    for face in faces:
        v1 = np.array(vertices[face[0]])
        v2 = np.array(vertices[face[1]])
        v3 = np.array(vertices[face[2]])
        edge1 = v2 - v1
        edge2 = v3 - v1
        normal = np.cross(edge1, edge2)
        normal = normal / np.linalg.norm(normal)
        normals.append(normal)
    return normals

def lighting():
    glLightfv(GL_LIGHT0, GL_POSITION, (10, -10, 0, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.0, 0.0, 0.0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def draw_obj(vertices, faces, normals):
    glBegin(GL_TRIANGLES)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])
        for vertex in face:
            glColor3f(0.0, 0.0, 1.0)
            glVertex3fv(vertices[vertex])
    glEnd()
    

def main():
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)


    glMatrixMode(GL_MODELVIEW)
    #glOrtho(-25,25,-25,25,-25,25)
    glTranslate(0, -5, -50)
    glRotatef(-80, 1, 0, 0)

    lighting()

    vertices, faces = load_obj('teapot.obj')
    normals = compute_normals(vertices, faces)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotate(2,0,0,1)

        draw_obj(vertices, faces, normals)
        pygame.display.flip()
        clock.tick(60)

main()
