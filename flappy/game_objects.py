import os
import random
import pygame

try:
    from .constants import LOCAL_DIR
except ImportError:
    from constants import LOCAL_DIR


class Bird:
    IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join(LOCAL_DIR, "imgs", "bird" + str(x) + ".png"))) for x in range(1, 4)]
    ROT_VEL = 20
    MAX_ROTATION = 25
    ANIMATION_TIME = 5

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.tilt_angle = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # for downward acceleration
        displacement = self.vel * (self.tick_count) + 0.5 * (3) * (self.tick_count) ** 2

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement / abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            self.tilt_angle = max(self.tilt_angle, self.MAX_ROTATION)

        else:  # tilt down
            if self.tilt_angle > -90:
                self.tilt_angle -= self.ROT_VEL

    def draw(self, window: pygame.Surface):
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt_angle <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # tilt the bird
        blitRotateCenter(window, self.img, (self.x, self.y), self.tilt_angle)

    def get_mask(self) -> pygame.mask.Mask:
        return pygame.mask.from_surface(self.img)


def blitRotateCenter(surface: pygame.Surface, image: pygame.Surface, topleft: tuple, angle: float):
    """
    Rotate a surface and blit it to the window
    :param surface: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surface.blit(rotated_image, new_rect.topleft)


class Pipe:
    VEL = 5
    GAP = 200

    def __init__(self, x: int):
        pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join(LOCAL_DIR, "imgs", "pipe.png")).convert_alpha())
        self.x = x
        self.top = 0
        self.bottom = 0
        self.height = 0
        self.img_bot = pipe_img
        self.img_top = pygame.transform.flip(pipe_img, False, True)
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.img_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, window: pygame.Surface):
        window.blit(self.img_top, (self.x, self.top))
        window.blit(self.img_bot, (self.x, self.bottom))

    def collide(self, bird: Bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.img_top)
        bottom_mask = pygame.mask.from_surface(self.img_bot)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if b_point or t_point:
            return True
        return False


class Base:
    VEL = 5

    def __init__(self, y: int):
        self.img = pygame.transform.scale2x(pygame.image.load(os.path.join(LOCAL_DIR, "imgs", "base.png")).convert_alpha())
        self.width = self.img.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window: pygame.Surface):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))


class BackGround:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, "imgs", "bg.png")).convert_alpha(), (600, 900))

    def draw(self, window: pygame.Surface):
        window.blit(self.img, (0, 0))
