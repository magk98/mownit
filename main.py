from numpy import sin, cos
import numpy as np
import scipy.integrate as integrate
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg
alpha1 = 30
alpha2 = 30

class InputLabel:
    def __init__(self, x, y, width, height, font, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (135, 206, 250)
        self.text = text
        self.value = ''
        self.right_side = ''
        self.txt_surface = font.render(text + ' = ', True, self.color)
        self.active = False

    def handle_event(self, event, font):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (30, 144, 255) if self.active else (135, 206, 250)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.right_side)
                    self.value = self.right_side
                    self.right_side = ''
                    changed_value = self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.right_side = self.right_side[:-1]
                else:
                    self.right_side += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text + ' = ' + self.right_side, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def derivs(state, t):

    dydx = np.zeros_like(state)
    # ***state is alpha1, p1, alpha2, p2***
    dydx[0] = state[1]                      # alpha1' = p1

    delta = state[2] - state[0]                     # (alpha2 - alpha1)
    den1 = (M1 + M2)*L1 - M2*L1*cos(delta)*cos(delta)
    dydx[1] = (M2*L1*state[1]*state[1]*sin(delta)*cos(delta) +  # p1' = ...
               M2*G*sin(state[2])*cos(delta) +
               M2*L2*state[3]*state[3]*sin(delta) -
               (M1 + M2)*G*sin(state[0]))/den1

    dydx[2] = state[3]          # alpha2' = p2

    den2 = (M1 + M2)*L2 - M2*L2*cos(delta)*cos(delta)
    dydx[3] = (-M2*L2*state[3]*state[3]*sin(delta)*cos(delta) +     # p2' = ...
               (M1 + M2)*G*sin(state[0])*cos(delta) -
               (M1 + M2)*L1*state[1]*state[1]*sin(delta) -
               (M1 + M2)*G*sin(state[2]))/den2

    return dydx


def count(m1, m2, l1, l2, alpha1, alpha2):
    # m1, m2, l1, l2
    global M1, M2, L1, L2
    M1, M2, L1, L2 = m1, m2, l1, l2

    # create a time array from 0..20 sampled at 0.05 second steps
    dt = 0.05
    t = np.arange(0.0, 200, dt)

    # alpha1 and alpha2 are the initial angles in degrees
    # p1 and p2 are the initial angular velocities (degrees per second)

    p1 = 0.0
    p2 = 0.0

    # initial state
    state = np.radians([alpha1, p1, alpha2, p2])

    # integrate (solving) ODE using scipy.integrate.
    salvation = integrate.odeint(derivs, state, t)

    x1 = L1*sin(salvation[:, 0])  # alpha1
    y1 = -L1*cos(salvation[:, 0])

    x2 = L2*sin(salvation[:, 2]) + x1  # alpha2
    y2 = -L2*cos(salvation[:, 2]) + y1

    return x1, y1, x2, y2

    """
    ====================================
                Pygame part
    ====================================
    """


def main():

    global M1, M2, L1, L2, alpha1, alpha2
    x1_temp, y1_temp, x2_temp, y2_temp = count(1, 1, 1.5, 2, 359, 180)
    x1 = [(SCREEN_WIDTH // 2 + x*100) for x in x1_temp]
    y1 = [(SCREEN_HEIGHT // 2 - y*100) for y in y1_temp]
    x2 = [(SCREEN_WIDTH // 2 + x*100) for x in x2_temp]
    y2 = [(SCREEN_WIDTH // 2 - y*100) for y in y2_temp]

    is_running = True
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Double Pendulum")
    font = pygame.font.SysFont('Arial', 12)
    index = 0
    input_box1 = InputLabel(20, 50, 140, 32, font, "M1")
    input_box2 = InputLabel(20, 90, 140, 32, font, "M2")
    input_box3 = InputLabel(20, 130, 140, 32, font, "L1")
    input_box4 = InputLabel(20, 170, 140, 32, font, "L2")
    input_box5 = InputLabel(20, 210, 140, 32, font, "ALPHA 1")
    input_box6 = InputLabel(20, 250, 140, 32, font, "ALPHA 2")
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5, input_box6]

    while is_running:
        pygame.time.delay(50)
        index = (index + 1) % len(x1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
            for box in input_boxes:
                box.handle_event(event, font)
                if box.value != '':
                    if box.text == 'M1':
                        M1 = box.value
                    elif box.text == 'M2':
                        M2 = box.value
                    elif box.text == 'L1':
                        L1 = box.value
                    elif box.text == 'L2':
                        L2 = box.value
                    elif box.text == 'ALPHA 1':
                        alpha1 = box.value
                    elif box.text == 'ALPHA 2':
                        alpha2 = box.value
                    x1_temp, y1_temp, x2_temp, y2_temp = count(int(M1), int(M2), int(L1), int(L2), int(alpha1), int(alpha2))
                    x1 = [(SCREEN_WIDTH // 2 + x*100) for x in x1_temp]
                    y1 = [(SCREEN_HEIGHT // 2 - y*100) for y in y1_temp]
                    x2 = [(SCREEN_WIDTH // 2 + x*100) for x in x2_temp]
                    y2 = [(SCREEN_WIDTH // 2 - y*100) for y in y2_temp]
                    box.value = ''
        #Drawing white screen and figures
        win.fill((241, 237, 233))
        circle1 = pygame.draw.circle(win, (5, 5, 5), (int(x1[index]), int(y1[index])), 10, 0)
        pygame.draw.line(win, (5, 5, 5), [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], [circle1.x + 10, circle1.y + 10], 1)
        circle2 = pygame.draw.circle(win, (5, 5, 5), (int(x2[index]), int(y2[index])), 10, 0)
        pygame.draw.line(win, (5, 5, 5), [circle1.x + 10, circle1.y + 10], [circle2.x + 10, circle2.y + 10], 1)

        for box in input_boxes:
            box.draw(win)

        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
