from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import pygame
import random
from PowerUP import PowerUp

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40  # Width of a brick (in pixels)
BRICK_HEIGHT = 15  # Height of a brick (in pixels)
BRICK_ROWS = 10  # Number of rows of bricks
BRICK_COLS = 10  # Number of columns of bricks
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10  # Radius of the ball (in pixels)
PADDLE_WIDTH = 75  # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels)
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Initialize pygame for sound 202411
        pygame.init()
        pygame.mixer.init()

        # Load sounds 202411
        self.bounce_sound = pygame.mixer.Sound("sound/bounce.mp3")
        self.brick_sound = pygame.mixer.Sound("sound/brick.wav")
        self.background_music = "sound/Gravity.mp3"
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Play background music in a loop

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)
        # Create a paddle
        self.paddle = GRect(width=PADDLE_WIDTH, height=PADDLE_HEIGHT, x=(window_width - paddle_width) / 2,
                            y=window_height - PADDLE_OFFSET)
        self.paddle.filled = True
        self.window.add(self.paddle)
        onmousemoved(self.handle_mouse_moved)

        # Create a scoreboard 202411
        self.score = 0  # Initialize the score to 0
        self.scoreboard = GLabel(f"Score: {self.score}", x=10, y=30)  # Display score at the top
        self.scoreboard.font = "Times-24"
        self.window.add(self.scoreboard)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.original_x = (window_width - ball_radius * 2) / 2
        self.original_y = (window_height - ball_radius * 2) / 2
        self.ball.filled = True
        self.window.add(self.ball, self.original_x, self.original_y)
        self.starting = False

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        self.check_collisions()

        self.powerups = []
        self.paddle_expanded = False
        self.expand_timer = 0
        self.expand_duration = 5000

        # Initialize our mouse listeners
        onmouseclicked(self.click)
        self.bricks = []
        # Draw bricks
        for i in range(brick_rows):
            for j in range(brick_cols):
                x_position = j * (brick_width + brick_spacing)
                y_position = brick_offset + i * (brick_height + brick_spacing)
                brick = GRect(width=brick_width, height=brick_height, x=x_position, y=y_position)
                brick.filled = True
                if i // 2 == 0:
                    brick.fill_color = brick.color = 'purple'
                elif i // 2 == 1:
                    brick.fill_color = brick.color = 'orange'
                elif i // 2 == 2:
                    brick.fill_color = brick.color = 'yellow'
                elif i // 2 == 3:
                    brick.fill_color = brick.color = 'green'
                else:
                    brick.fill_color = brick.color = 'blue'
                self.window.add(brick)
                self.bricks.append(brick)

    def handle_mouse_moved(self, event):
        mouse_x = event.x
        new_x = mouse_x - self.paddle.width / 2
        if new_x < 0:
            new_x = 0
        elif new_x > self.window.width - self.paddle.width:
            new_x = self.window.width - self.paddle.width
        self.paddle.x = new_x

    def click(self, event):
        if not self.starting:
            self.starting = True
            self.__dx = random.randint(1, MAX_X_SPEED)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def check_collisions(self):  # revised on 202411
        x1, y1 = self.ball.x, self.ball.y
        x2, y2 = self.ball.x + (2 * BALL_RADIUS), self.ball.y
        x3, y3 = self.ball.x, self.ball.y + (2 * BALL_RADIUS)
        x4, y4 = self.ball.x + (2 * BALL_RADIUS), self.ball.y + (2 * BALL_RADIUS)
        for point in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]:
            obj = self.window.get_object_at(point[0], point[1])
            if obj is not None:
                if obj == self.scoreboard:
                    continue  # Skip this iteration, do not process collisions with the scoreboard
                if obj == self.paddle:
                    if self.__dy > 0:
                        self.__dy = -self.__dy
                        self.bounce_sound.play()

                elif obj in self.bricks:
                    self.__dy = -self.__dy
                    self.window.remove(obj)
                    self.bricks.remove(obj)
                    self.brick_sound.play()
                    self.score += 10  # Increase score by 10 when a brick is hit
                    self.update_score()  # Update the scoreboard
                    if random.random() < 0.6:
                        self.create_powerup(obj.x, obj.y)
                        self.expand_paddle()
                for powerup in self.powerups:
                    if self.ball_overlaps_with_powerup(powerup):
                        self.window.remove(powerup)
                        self.powerups.remove(powerup)
                        self.score += 30
                        self.update_score()
                if self.score > 500:
                    self.increase_ball_speed()

    def expand_paddle(self):
        if not self.paddle_expanded:
            new_width = min(self.paddle.width * 1.5, self.window.width)
            new_paddle = GRect(width=new_width, height=self.paddle.height, x=self.paddle.x, y=self.paddle.y)
            new_paddle.filled = True
            new_paddle.fill_color = "orange"
            self.window.remove(self.paddle)
            self.window.add(new_paddle)
            self.paddle = new_paddle
            self.paddle_expanded = True
            self.expand_timer = pygame.time.get_ticks()

    def increase_ball_speed(self):
        """
        Increase the ball speed by a factor.
        """
        speed_factor = 1.02
        new_dx = self.get_dx() * speed_factor
        new_dy = self.get_dy() * speed_factor
        self.set_dx(new_dx)
        self.set_dy(new_dy)

    def ball_overlaps_with_powerup(self, powerup):
        ball_x1, ball_y1 = self.ball.x, self.ball.y
        ball_x2, ball_y2 = self.ball.x + self.ball.width, self.ball.y + self.ball.height
        return not (ball_x2 < powerup.x or ball_x1 > powerup.x + powerup.width or
                    ball_y2 < powerup.y or ball_y1 > powerup.y + powerup.height)

    def create_powerup(self, x, y):
        powerup = PowerUp(x, y)
        self.window.add(powerup)
        self.powerups.append(powerup)

    def update(self):
        ...
        if self.paddle_expanded:
            current_time = pygame.time.get_ticks()
            if current_time - self.expand_timer >= self.expand_duration:
                original_paddle = GRect(width=PADDLE_WIDTH, height=PADDLE_HEIGHT, x=self.paddle.x, y=self.paddle.y)
                original_paddle.filled = True
                original_paddle.fill_color = "black"
                self.window.remove(self.paddle)
                self.window.add(original_paddle)
                self.paddle = original_paddle
                self.paddle_expanded = False
        for powerup in self.powerups:
            powerup.move()
            if powerup.y > self.window.height:
                self.window.remove(powerup)
                self.powerups.remove(powerup)

    def update_score(self):  # 202411
        """Update the score on the scoreboard"""
        self.scoreboard.text = f"Score: {self.score}"  # Update the score text
        self.window.add(self.scoreboard)

    def restart(self):
        self.ball.x = self.original_x
        self.ball.y = self.original_y
        self.__dx = 0
        self.__dy = 0
        self.starting = False

    def get_dx(self):
        """
        Getter of dx.
        :return self.__dx: the value of private variable dx.
        """
        return self.__dx

    def get_dy(self):
        """
        Getter of dy.
        :return self.__dy: the value of private variable dy.
        """
        return self.__dy

    def set_dx(self, new_dx):
        """
        Setter function to update dx and bounce the ball.
        :param new_dx: the new dx value passed from the server side to the coder side.
        :return: None, this function does not return anything.
        """
        self.__dx = new_dx

    def set_dy(self, new_dy):
        """
        Setter function to update dy and bounce the ball.
        :param new_dy: the new dy value passed from the server side to the coder side.
        :return: None, this function does not return anything.
        """
        self.__dy = new_dy
