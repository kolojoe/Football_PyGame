import sys
import pygame

pygame.init()

size = width, height = 320, 640
screen = pygame.display.set_mode(size)

black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
player_size = (10, 10)
white = 255, 255, 255

# Field bounds is a rect used to draw the field and keep objects in bounds
field_bounds = pygame.Rect((0,0), size)
yard2px_height = height/120
yard2px_width = width/54

# Field matrix holds 54 * 120 spaces representing the possible
# spaces of occupation
field_matrix = [[None for _ in range(54)] for _ in range(120)]

# Offensive line can be anywhere along the 54 yards wide and
# up to 6 yards deep
off_line_matrix = [[None for _ in range(54)] for _ in range(6)]

class Player(pygame.sprite.Sprite):
    def __init__(self, color, size, pos):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface(size)
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.update(pos, self.rect.size)

    def set_position(self, pos):
        self.rect.update(pos, self.rect.size)


offense_group = pygame.sprite.Group()
offense = {
    "wrx": Player(red, player_size, (30*yard2px_width, 50*yard2px_height)),
    "wry": Player(red, player_size, (26*yard2px_width, 50*yard2px_height))
}

for pos, player in offense.items():
    offense_group.add(player)

def draw_field(bounds_rect):
    pygame.draw.rect(screen, green, bounds_rect)
    margin = 15
    # Draw the outerbounds
    pygame.draw.line(screen, white, (bounds_rect.left, bounds_rect.bottom), (bounds_rect.left, bounds_rect.top), width=margin)
    pygame.draw.line(screen, white, (bounds_rect.left, bounds_rect.bottom), (bounds_rect.right, bounds_rect.bottom), width=margin)
    pygame.draw.line(screen, white, (bounds_rect.left, bounds_rect.top), (bounds_rect.right, bounds_rect.top), width=margin)
    pygame.draw.line(screen, white, (bounds_rect.right, bounds_rect.bottom), (bounds_rect.right, bounds_rect.top), width=margin)

    next_line = yard2px_height*10 # Start at the beginning of the end zone
    # Draw the yard lines
    for i in range(10):
        pygame.draw.line(screen, white, (bounds_rect.left, next_line), (bounds_rect.right, next_line), width=5)
        pygame.draw.line(screen, white, (bounds_rect.left, next_line + yard2px_height*5), (bounds_rect.right, next_line + yard2px_height*5), width=3)
        next_line += yard2px_height*10

    # Draw the final end zone line
    pygame.draw.line(screen, white, (bounds_rect.left, next_line), (bounds_rect.right, next_line), width=5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # ballrect = ballrect.move(speed)
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = -speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]

    screen.fill(black)
    draw_field(field_bounds)
    offense_group.draw(screen)
    # screen.blit()
    # screen.blit(ball, ballrect)
    pygame.display.flip()