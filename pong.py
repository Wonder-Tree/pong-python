from operator import pos
import pygame
import posecamera
import cv2
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Initializing the display window
WIN_WIDTH = 800
WIN_HEIGHT = 600


# draws the paddle. Also restricts its movement between the edges
# of the window.
def drawrect(screen, x, y):
    if x <= 0:
        x = 0
    if x >= 699:
        x = 699
    pygame.draw.rect(screen, RED, [x, y, 150, 40])

def main(callback=None):

    pygame.init()

    size = (WIN_WIDTH, WIN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong - PoseCamera")

    # Starting coordinates of the paddle
    rect_x = 400
    rect_y = 580

    # initial speed of the paddle
    rect_change_x = 0
    rect_change_y = 0

    # initial position of the ball
    ball_x = 50
    ball_y = 50

    # speed of the ball
    ball_change_x = 5
    ball_change_y = 5

    score = 0

    # PoseCamera luncher calback
    if(callback is not None):
        callback()
    
    # init PoseCamera sdk
    det = posecamera.pose_tracker.PoseTracker()
    
    cam = cv2.VideoCapture(0)

        
    # game's main loop
    done = False
    clock = pygame.time.Clock()

    while not done:

        if cam.isOpened():
            ret, image = cam.read()
            image = cv2.flip(image, 1)
            image = cv2.resize(image, (800, 600))

            pose = det(image)

            # get nose coordinates
            nose = pose.keypoints["nose"]

            # set the controller according to nose x position
            rect_x = nose[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rect_change_x = -6
                elif event.key == pygame.K_RIGHT:
                    rect_change_x = 6

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    rect_change_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    rect_change_y = 0


        # draw webcam frame
        image =cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.fliplr(image)
        image = np.rot90(image)

        pyframe = pygame.surfarray.make_surface(image)
        screen.blit(pyframe, (0, 0))

        rect_x += rect_change_x
        rect_y += rect_change_y

        ball_x += ball_change_x
        ball_y += ball_change_y

        # this handles the movement of the ball.
        if ball_x < 0:
            ball_x = 0
            ball_change_x = ball_change_x * -1
        elif ball_x > 785:
            ball_x = 785
            ball_change_x = ball_change_x * -1
        elif ball_y < 0:
            ball_y = 0
            ball_change_y = ball_change_y * -1
        elif ball_x > rect_x and ball_x < rect_x + 100 and ball_y == 565:
            ball_change_y = ball_change_y * -1
            score = score + 1
        elif ball_y > 600:
            ball_change_y = ball_change_y * -1
            score = 0

        pygame.draw.circle(screen, BLUE, (ball_x, ball_y), 20)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.fliplr(image)
        image = np.rot90(image)
        
        drawrect(screen, rect_x, rect_y)

        # score board
        font = pygame.font.SysFont('Arial', 30, False, False)
        text = font.render("Score " + str(score), True, WHITE)
        screen.blit(text, [380, 50])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
