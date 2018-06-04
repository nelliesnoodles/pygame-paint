#!usr/bin/python3
# -*- coding: utf-8 -*-
import pygame as pg
from sys import exit
from time import sleep


pg.init()

class SkullGlobals(object):
    """ class container for globally used variables """
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 800
        self.CENTER_SCREEN_X = 0 + self.WIDTH//12
        self.CENTER_SCREEN_Y = 0 + self.HEIGHT//12
        self.CENTER_SCREEN_H = self.HEIGHT - self.HEIGHT//6
        self.CENTER_SCREEN_W = self.WIDTH - self.WIDTH//6
        self.background_color = (110, 100, 110)
        self.BLUE = (40, 60, 200)
        self.LBLUE = (100, 100, 255)
        self.BORDER = (self.WIDTH + self.HEIGHT)//200
        self.left_y = 0 + self.HEIGHT//100
        self.left_x = 0 + self.WIDTH//100
        self.right_y = self.HEIGHT - self.left_y
        self.right_x = self.WIDTH - self.left_x
        self.small_height = self.left_y * 5
        self.small_width = self.left_x * 10
        self.left_upper_y = 0 + (self.HEIGHT//10)
        self.left_upper_x = 0 + (self.WIDTH//10)
        self.left_upper_right_y = self.HEIGHT - self.BORDER
        self.right_lower_x = self.WIDTH - (self.WIDTH//10)
        self.right_lower_y = self.HEIGHT - (self.HEIGHT//10)
        self.CENTER = (self.WIDTH//2, self.HEIGHT//2)
        self.FULL_SIZE = (self.WIDTH//4 + self.HEIGHT//4)//2
        self.SMALL_SIZE = (self.WIDTH//50 + self.HEIGHT//50)//2
        self.RED = (230, 50, 50)
        self.GREEN = (50, 230, 50)
        self.D_WHITE = (200,200,200)
        self.base_color = 150
        self.menu_bar_color = (90, 100, 80)


## can not do this --> self.screen = pg.display.set_mode((globals.WIDTH, globals.HEIGHT))

globals = SkullGlobals()
screen = pg.display.set_mode((globals.WIDTH, globals.HEIGHT))
pg.display.set_caption(('My Painter'))
screen.fill(globals.background_color)
animation_timer = pg.time.Clock()
pg.display.flip()

class DrawSurface(object):
    def __init__(self):
        self.width = globals.CENTER_SCREEN_W
        self.height = globals.CENTER_SCREEN_H
        self.x_pos = globals.CENTER_SCREEN_X
        self.y_pos = globals.CENTER_SCREEN_Y

    def draw_surface(self):
        w = int(self.width)
        h = int(self.height)
        center_screen = pg.Surface((w, h))
        center_screen.fill(globals.D_WHITE)
        screen.blit(center_screen, (self.x_pos, self.y_pos))

    def get_placement(self):
        end_x = self.x_pos + self.width
        end_y = self.y_pos + self.height
        position_size = [self.x_pos, self.y_pos, end_x, end_y]
        return position_size

class WindowRect(object):
    def __init__(self, screen, pos_x, pos_y, width, height):
        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = (130, 160, 130)
        self.thickness = globals.BORDER

    def draw_rect(self):
        size = (self.pos_x, self.pos_y, self.width, self.height)
        border_size = (self.pos_x - 3, self.pos_y - 3, self.width + 5, self.height + 5)
        pg.draw.rect(self.screen, globals.menu_bar_color, border_size, 5 )
        pg.draw.rect(self.screen, self.color, size, 0)

    def get_dimensions(self):
        """ return the needed dimensions for use """
        end_x_pos = self.pos_x + self.width
        end_y_pos = self.pos_y + self.height
        rect_list_dims = [self.pos_x, self.pos_y, end_x_pos, end_y_pos]
        return rect_list_dims

class ButtonXY(object):
    """Class for drawing rectangle,  and getting position of rectangle"""
    def __init__(self, my_screen, pos_x, pos_y, rect_width, rect_height, R, G, B, name):
        self.my_screen = my_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = rect_width
        self.height = rect_height
        self.R = R
        self.G = G
        self.B = B
        self.name = name
        self.font = pg.font.SysFont('Arial', self.height//3)

    def place_rect(self):
        """ pygame.draw.rect(screen, color, (x, y, width, height), width of outline) """
        thick = 5
        color = (self.R, self.G, self.B)
        light_color = (140, 130, 150)
        size = (self.pos_x, self.pos_y, self.width, self.height)
        inner_box = (self.pos_x + 3, self.pos_y + 3, self.width - 6, self.height - 6)
        center_height = self.height//4
        center_width = self.width//4
        text_pos_x = self.pos_x + center_width
        text_pos_y = self.pos_y + center_height
        #text_size = self.font.size(self.name)
        # ADJUSTING center position by TEXT size will require a lot of error proofing...
        pg.draw.rect(self.my_screen, color, size, 5)
        pg.draw.rect(self.my_screen, light_color, inner_box, 0)
        self.my_screen.blit(self.font.render(self.name, True, (0, 0, 0)), (text_pos_x, text_pos_y))

    def get_rect_place(self):
        """ return the needed dimensions for button click check """
        end_x_pos = self.pos_x + self.width
        end_y_pos = self.pos_y + self.height
        rect_list_dims = [self.pos_x, self.pos_y, end_x_pos, end_y_pos]
        return rect_list_dims



class CircleXY(object):
    """ Class for drawing circle to screen """
    def __init__(self,my_screen, pos_x, pos_y, radius, R, G, B, speed, thickness):
        self.my_screen = my_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.R = R
        self.G = G
        self.B = B
        self.x_change = speed
        self.y_change = speed
        self.thickness = thickness

    def draw_circle(self):
        """ place a circle at mouse position """
        color = (self.R, self.G, self.B)
        position = (self.pos_x, self.pos_y)
        pg.draw.circle(self.my_screen, color, position, self.radius, self.thickness)

class DrawCircle(object):
    """ place a circle at initiated position, with given radius, color
        **speed and thickness may be used later**  """
    def __init__(self, my_screen, pos_x, pos_y, radius, color, speed=None, thickness=0):
        self.my_screen = my_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.thickness = thickness

    def add_circle(self):
        position = (self.pos_x, self.pos_y)
        pg.draw.circle(self.my_screen, self.color, position, self.radius, self.thickness)

class ColorPicker(object):
    """
        Color change graphic to allow change of color of circles
        Making all dimensions dependant on globals will help to scale the whole thing later
    """
    def __init__(self):
        self.width = globals.WIDTH//5
        self.height = globals.HEIGHT//5
        self.x_pos = globals.WIDTH - self.width - globals.BORDER
        self.y_pos = globals.HEIGHT - (self.height * 2) - globals.BORDER
        self.window = WindowRect(screen, self.x_pos, self.y_pos, self.width, self.height)
        self.font = pg.font.SysFont('Arial', self.height//5)

    def start_rect(self):
        """ Graphical parts of color picker  rect(surface, color, size, thick)"""
        self.window.draw_rect()
        size_w = self.width//5
        size_h = self.height//5
        diff_x = (self.x_pos + self.width) - size_w
        diff_y = (self.y_pos + self.height) - size_h
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        light = (200, 200, 200)
        dark = (0, 0, 0)
        upper_R = (self.x_pos, self.y_pos, size_w, size_h)
        lower_R = (diff_x, self.y_pos, size_w, size_h)
        upper_L = (self.x_pos, diff_y, size_w, size_h)
        lower_L = (diff_x, diff_y, size_w, size_h)
        half_lower_L = (diff_x, diff_y, size_w//2, size_h)
        pg.draw.rect(screen, red, upper_R, 0)         #B
        pg.draw.rect(screen, green, lower_R, 0)       #D
        pg.draw.rect(screen, blue, upper_L, 0)        #A
        pg.draw.rect(screen, light, lower_L, 0)       #C
        pg.draw.rect(screen, dark, half_lower_L, 0)


    def color_buttons(self):
        """Buttons to go below, left, right, above color choices
            red_box = (self.x_pos, self.y_pos, size_w, size_h)
            green_box = (diff_x, self.y_pos, size_w, size_h)
            blue_box = (self.x_pos, diff_y, size_w, size_h)
            shade_box = (diff_x, diff_y, size_w, size_h)
        """
        size_w = self.width//5
        size_h = self.height//5
        diff_x = (self.x_pos + self.width) - size_w
        diff_y = (self.y_pos + self.height) - size_h
        border = 2
        red = (255, 0, 0)
        blue = (0, 0, 255)
        grey = (75, 75, 75)
        green = (0, 255, 0)
        black = (0, 0, 0)
        plus = " + "
        plus = self.font.render(plus, True, black)
        minus = " - "
        minus = self.font.render(minus, True, black)

        # make the boxes locations dependant on the start_rect() color boxes

        green_left = (diff_x - size_w - border, self.y_pos, size_w, size_h)
        green_down = (diff_x, self.y_pos + size_h + border, size_w, size_h)
        shade_left = (diff_x - size_w - border, diff_y, size_w, size_h)
        shade_up = (diff_x, diff_y - size_h - border, size_w, size_h)
        red_right = (self.x_pos + size_w + border, self.y_pos, size_w, size_h)
        red_down = (self.x_pos, self.y_pos + size_h + border, size_w, size_h)
        blue_up = (self.x_pos, diff_y - size_h - border, size_w, size_h)
        blue_right = (self.x_pos + size_w + border, diff_y, size_w, size_h)

        pg.draw.rect(screen, blue, blue_right, 3)
        screen.blit(minus, (self.x_pos + size_w, diff_y))
        pg.draw.rect(screen, blue, blue_up, 3)
        screen.blit(plus, (self.x_pos, diff_y - size_h))
        pg.draw.rect(screen, red, red_down, 3)
        screen.blit(minus, (self.x_pos, self.y_pos + size_h))
        pg.draw.rect(screen, red, red_right, 3)
        screen.blit(plus, (self.x_pos + size_w, self.y_pos))
        pg.draw.rect(screen, green, green_left, 3)
        #print("green_left =", green_left)
        screen.blit(plus, (diff_x - size_w, self.y_pos))
        pg.draw.rect(screen, green, green_down, 3)
        screen.blit(minus, (diff_x, self.y_pos + size_h))
        pg.draw.rect(screen, grey, shade_left, 3)
        screen.blit(minus, (diff_x - size_w, diff_y))
        pg.draw.rect(screen, grey, shade_up, 3)
        screen.blit(plus, (diff_x, diff_y - size_h))


    def get_button_place(self, which_button):
        """
        From the button locations defined in color_buttons()
        return the coordinates needed to detect mouse click in button
        """
        size_w = self.width//5
        size_h = self.height//5
        diff_x = (self.x_pos + self.width) - size_w
        diff_y = (self.y_pos + self.height) - size_h
        border = 2
        # Making the variables less mathy to return
        # basically we need to return the (x, y, x+width, y+width)
        GL_x = diff_x - size_w - border
        GL_y = self.y_pos
        GD_y = self.y_pos + size_h + border
        BU_y = diff_y - size_h - border
        BR_x = self.x_pos + size_w + border
        RR_x = self.x_pos + size_w + border
        RD_y = self.y_pos + size_h + border
        SHL_x = diff_x - size_w - border
        SHU_y = diff_y - size_h - border



        green_left = (GL_x, self.y_pos, GL_x + size_w, self.y_pos + size_h)
        green_down = (diff_x, GD_y, diff_x + size_w, GD_y + size_h)
        shade_left = (SHL_x, diff_y, SHL_x + size_w, diff_y + size_h)
        shade_up = (diff_x, SHU_y - border, diff_x + size_w, diff_y + size_h)
        red_right = (RR_x, self.y_pos, RR_x + size_w, self.y_pos + size_h)
        red_down = (self.x_pos, RD_y, self.x_pos + size_w, RD_y + size_h)
        blue_up = (self.x_pos, BU_y, self.x_pos + size_w, BU_y + size_h)
        blue_right = (BR_x, diff_y, BR_x + size_w, diff_y + size_h)

        if which_button == "plus red":
            return red_right
        elif which_button == "minus red":
            return red_down
        elif which_button == "plus green":
            #print("plus green=", green_left)
            return green_left
        elif which_button == "minus green":
            return green_down
        elif which_button == "plus shade":
            return shade_up
        elif which_button == "minus shade":
            return shade_left
        elif which_button == "plus blue":
            return blue_up
        elif which_button == "minus blue":
            return blue_right

        else:
            pass




    def run(self, R, G, B):
        """ create draw the color picker window graphics """
        radius = self.width//5
        diff_x = self.x_pos + self.width
        diff_y = self.y_pos + self.height
        pos_x = (self.x_pos + diff_x)//2
        pos_y = (self.y_pos + diff_y)//2
        position = (pos_x, pos_y)
        color = (R, G, B)
        self.start_rect()
        pg.draw.circle(screen, color, position, radius, 0)
        self.color_buttons()

class StateEngine(object):
    """ Class container for running engine, screen, updates """

    def __init__(self):
        self.on_button = ButtonXY(screen, globals.left_x, globals.left_y, globals.small_width, globals.small_height, globals.base_color - 100, globals.base_color, globals.base_color - 100, "ON")
        self.new_circle_button = ButtonXY(screen, globals.left_x + globals.small_width + 8, globals.left_y, globals.small_width, globals.small_height, globals.base_color - 100, globals.base_color, globals.base_color - 100, "NEW")
        self.off_button = ButtonXY(screen, (globals.right_x - globals.small_width), (globals.right_y - globals.small_height) , globals.small_width, globals.small_height, globals.base_color, globals.base_color - 100, globals.base_color -100, "OFF")
        self.color_button = ButtonXY(screen, (globals.right_x - globals.small_width * 2 - 8), (globals.right_y - globals.small_height), globals.small_width, globals.small_height, globals.base_color, globals.base_color -100, globals.base_color - 100, "COLOR")
        self.rect_list = [self.on_button, self.off_button, self.new_circle_button, self.color_button]
        self.ON = CircleXY(screen, globals.left_upper_x, globals.left_upper_y, globals.SMALL_SIZE,  50, 230, 50, 1, 0)
        self.OFF = CircleXY(screen, globals.right_lower_x, globals.right_lower_y, globals.SMALL_SIZE, 200, 50, 50, 1, 0)
        self.object_list = [self.ON, self.OFF]
        self.running = True
        self.center_surface = DrawSurface()
        self.drawn_circs = []
        self.dsp = self.center_surface.get_placement()
        self.windows = []
        self.new_window = ColorPicker()
        self.red = 0
        self.green = 0
        self.blue = 0

    def screen_update(self):
        self.center_surface.draw_surface()
        pg.draw.rect(screen, globals.menu_bar_color, (0, 0, globals.WIDTH, globals.HEIGHT//20), 0)
        pg.draw.rect(screen, globals.menu_bar_color, (0, globals.HEIGHT - globals.HEIGHT//20, globals.WIDTH, globals.HEIGHT//20), 0)
        for rects in self.rect_list:
            rects.place_rect()
        for circs in self.drawn_circs:
            circs.add_circle()
        for window in self.windows:
            window.run(self.red, self.green, self.blue)



    def update_buttons(self, position, on, off, new, color_pick):

        for rects in self.rect_list:
            cbd = rects.get_rect_place()
            if cbd[0] < position[0] < cbd[2]:
                if cbd[1] < position[1] < cbd[3]:
                    #print("IN BUTTON", rects.name)
                    if rects.name == "ON":
                        on = True
                        off = False
                    if rects.name == "OFF":
                        # I have to double click to get color picker off... need fixed
                        off = True
                        on = False
                        color_pick = False
                        if len(self.windows) > 0:
                            self.windows.pop()
                    if rects.name == "NEW":
                        new = True
                        on = True
                        color_pick = False
                    if rects.name == 'COLOR':
                        on = True
                        new = False
                        color_pick = True
                        off = False
                        new_window = ColorPicker()
                        self.windows.append(new_window)

        return on, off, new, color_pick

    def update_draws(self, on, off, new, color_pick):
        if on and not off:
            if new and not color_pick:
                radius = 20
                (x, y) = pg.mouse.get_pos()
                # dsp = Drawn Screen Parameters
                limit_x_left = self.dsp[0] - radius
                limit_x_right = self.dsp[2] - radius
                limit_y_top = self.dsp[1] - radius
                limit_y_bottom = self.dsp[3] - radius

                if limit_x_left < x < limit_x_right:
                    if limit_y_top < y < limit_y_bottom:

                        color = (self.red, self.green, self.blue)

                        circle = DrawCircle(screen, x, y, radius, color)
                        self.drawn_circs.append(circle)
    def check_color_picker(self, position, on, off, new, color_pick):
        if on and color_pick:
            if not off and not new:
                (gx, gy, gdx, gdy) = self.new_window.get_button_place("plus green")
                (g2x, g2y, g2dx, g2dy) = self.new_window.get_button_place("minus green")
                (bx, by, bdx, bdy) = self.new_window.get_button_place("plus blue")
                (b2x, b2y, b2dx, b2dy) = self.new_window.get_button_place("minus blue")
                (rx, ry, rdx, rdy) = self.new_window.get_button_place("plus red")
                (r2x, r2y, r2dx, r2dy) = self.new_window.get_button_place("minus red")
                (shx, shy, shdx, shdy) = self.new_window.get_button_place("plus shade")
                (sh2x, sh2y, sh2dx, sh2dy) = self.new_window.get_button_place("minus shade")
                if gx < position[0] < gdx and gy < position[1] < gdy:
                    if 0 <= self.green <= 250:
                        self.green += 5
                elif g2x < position[0] < g2dx and g2y < position[1] < g2dy:
                    if 255 >= self.green >= 5:
                        self.green -= 5
                elif bx < position[0] < bdx and by < position[1] < bdy:
                    if 0 <= self.blue <= 250:
                        self.blue += 5
                elif b2x < position[0] < b2dx and b2y < position[1] < b2dy:
                    if 255 >= self.blue >= 5:
                        self.blue -= 5
                elif rx < position[0] < rdx and ry < position[1] < rdy:
                    if 0 <= self.red <= 250:
                        self.red += 5
                elif r2x < position[0] < r2dx and r2y < position[1] < r2dy:
                    if 255 >= self.red >= 5:
                        self.red -= 5
                elif shx < position[0] < shdx and shy < position[1] < shdy:
                    # I tried increments of 10, shade difference was much more dramatic
                    if 0 <= self.red <= 250:
                        self.red += 5
                    if 0 <= self.green <= 250:
                        self.green += 5
                    if 0 <= self.blue <= 250:
                        self.blue += 5
                elif sh2x < position[0] < sh2dx and sh2y < position[1] < sh2dy:
                    if 255 >= self.red >= 5:
                        self.red -= 5
                    if 255 >= self.green >= 5:
                        self.green -= 5
                    if 255 >= self.blue >= 5:
                        self.blue -= 5

class DrawIt(object):
    """ class container for defining pygame screen run and iteraction """
    def __init__(self):
        self.engine = StateEngine()
        self.running = True
    def run_draw(self):
        on = False
        off = False
        new = False
        color_pick = False
        screen.fill(globals.background_color)
        while self.running:
            animation_timer.tick(60)
            screen.fill(globals.background_color)
            self.engine.screen_update()
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    exit(0)
                if event.type == pg.MOUSEBUTTONDOWN:
                    position = pg.mouse.get_pos()
                    on, off, new, color_pick = self.engine.update_buttons(position, on, off, new, color_pick)
                    self.engine.update_draws(on, off, new, color_pick)
                    self.engine.check_color_picker(position, on, off, new, color_pick)

            if on:
                item = self.engine.object_list[0]
                item.draw_circle()

            if off:
                item = self.engine.object_list[1]
                item.draw_circle()
            #print(" object_list length ==========", len(self.object_list))
            pg.display.flip()


drawing = DrawIt()
drawing.run_draw()
