import pygame as pg
from renderer import *

pg.init()
wn = pg.display.set_mode((1200,800))

clock = pg.time.Clock()

cam: Camera = Camera(fov=80, pos=vec3(0,0,5), near=0.01, far=100)
cube = Mesh.fromFile('majmunce.obj')
dt = 1
speed = 3
run = True
while(run):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    fps = clock.get_fps()
    pg.display.set_caption("ефпиес: " + str(round(fps,2)))
    wn.fill((0, 5, 23))
    keys = pg.key.get_pressed()
    mov = vec3(0,0,0)
    if(keys[pg.K_a]): mov -= cam.right
    if(keys[pg.K_d]): mov += cam.right
    if(keys[pg.K_w]): mov += cam.front
    if(keys[pg.K_s]): mov -= cam.front
    if(keys[pg.K_SPACE] or keys[pg.K_e]): cam.pos.y += 5*dt
    if(keys[pg.K_LCTRL] or keys[pg.K_q]): cam.pos.y -= 5*dt
    if(keys[pg.K_LEFT]):  cam.rot.y -= 50*dt
    if(keys[pg.K_RIGHT]): cam.rot.y += 50*dt
    cam.Update()
    mov.normalize()
    mov *= speed*dt
    cam.pos.x += mov.x
    cam.pos.z += mov.z
    cube.trans(wn, cam)
    #print(len(tris))
    RenderScene(wn, cam)
    pg.display.flip()
    dt = clock.tick(200)/1000

pg.quit()