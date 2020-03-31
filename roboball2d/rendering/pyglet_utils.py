import numpy as np

try:
    import pyglet.gl as gl
except:
    # may fail on cluster or on bamboo
    pass
    
"""
List of standalone functions useful when using pyglet.
These functions may be convenient when programming callbacks for
the pyglet renderer. See : :py:class:`roboball2d.rendering.pyglet_renderer.PygletRenderer`
 and :py:meth:`roboball2d.demos.rendering_callback`.
"""

def draw_circle_sector(center, angle, radius, n, color, triangles_to_draw):
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glColor3f(*color)
    gl.glVertex2f(*center)
    for i in range(triangles_to_draw + 1):
        gl.glVertex2f(center[0] + np.cos(2.*np.pi/n*i + angle)*radius, 
                      center[1] + np.sin(2.*np.pi/n*i + angle)*radius)
    gl.glEnd()

def draw_ball(center, angle, radius, n, color, line_color):
    draw_circle_sector(center, angle, radius, n, color, n)
    gl.glBegin(gl.GL_LINES)
    gl.glColor3f(*line_color)
    gl.glVertex2f(center[0] - np.cos(angle)*radius, 
                  center[1] - np.sin(angle)*radius)
    gl.glVertex2f(center[0] - np.cos(angle + np.pi)*radius, 
                  center[1] - np.sin(angle + np.pi)*radius)
    gl.glEnd()

def draw_box(center, diameter, length, phi, color):
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glTranslatef(center[0], center[1], 0.)
    gl.glRotatef(phi, 0., 0., 1.)
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3f(*color)
    gl.glVertex2f(-0.5*diameter, -0.5*length)
    gl.glVertex2f(0.5*diameter, -0.5*length)
    gl.glVertex2f(0.5*diameter, 0.5*length)
    gl.glVertex2f(-0.5*diameter, 0.5*length)
    gl.glEnd()
    gl.glPopMatrix()

def draw_racket( racket_position,
                 racket_angle,
                 racket_diameter,
                 racket_thickness,
                 racket_color ):

    draw_box(racket_position,
             racket_diameter,
             racket_thickness,
             racket_angle/np.pi*180,
             racket_color)

def draw_rod(rod_position,
             rod_angle,
             rod_diameter,
             rod_length,
             rod_color):

    draw_box(rod_position,
             rod_diameter,
             rod_length,
             rod_angle/np.pi*180,
             rod_color)


# To visualize velocities and desired velocities
def draw_vector(initial_point, vector, width, arrow_head_size, color):
    length = np.linalg.norm(vector)
    # orthogonal vector used for constructing vertices that make up 
    # arrow shape
    w = (vector[1]/length, -vector[0]/length)
    # factor scaling vector such that it only reaches to arrow head and not to tip
    rescale = (length - arrow_head_size)/length
    v_re = [rescale*x for x in vector]

    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glTranslatef(initial_point[0], initial_point[1], 0.)
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glColor3f(*color)
    # rectangle
    gl.glVertex2f( 0.5*w[0]*width,              0.5*w[1]*width)
    gl.glVertex2f( 0.5*w[0]*width + v_re[0],  0.5*w[1]*width + v_re[1])
    gl.glVertex2f(-0.5*w[0]*width + v_re[0], -0.5*w[1]*width + v_re[1])
    gl.glVertex2f(-0.5*w[0]*width + v_re[0], -0.5*w[1]*width + v_re[1])
    gl.glVertex2f(-0.5*w[0]*width,             -0.5*w[1]*width)
    gl.glVertex2f( 0.5*w[0]*width,              0.5*w[1]*width)
    # arrow head
    gl.glVertex2f( 0.5*w[0]*arrow_head_size + v_re[0],  
            0.5*w[1]*arrow_head_size + v_re[1])
    gl.glVertex2f(-0.5*w[0]*arrow_head_size + v_re[0], 
            -0.5*w[1]*arrow_head_size + v_re[1])
    gl.glVertex2f(vector[0], vector[1])
    gl.glEnd()
    gl.glPopMatrix()


