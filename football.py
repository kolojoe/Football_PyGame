import sys
import pygame
from pygame.math import Vector2
import random

pygame.init()

size = width, height = 500, 1000
screen = pygame.display.set_mode(size)

black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
player_size = (10, 10)
ball_size = (20,20)
white = 255, 255, 255
blue = 0, 0, 255
brown = 101, 67, 33
ball = pygame.Rect((0,0), ball_size)

dT = 0

# Field bounds is a rect used to draw the field and keep objects in bounds
field_bounds = pygame.Rect((0,0), size)
yard2px_height = height/120
yard2px_width = width/54
yard2px = Vector2(yard2px_width,yard2px_height)

# Field matrix holds 54 * 120 spaces representing the possible
# spaces of occupation
field_matrix = [[None for _ in range(54)] for _ in range(120)]

# Offensive line can be anywhere along the 54 yards wide and
# up to 6 yards deep
off_line_matrix = [[None for _ in range(54)] for _ in range(6)]

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, size, speed):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of a rectangle
        self.image = pygame.Surface(size)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = Vector2()
        self.residual = Vector2()

class Player_Possession(Ball):
    def __init__(self, color, size, speed):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of a rectangle
        self.image = pygame.Surface(size)
        self.image.fill(color)
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = Vector2()
        self.residual = Vector2()

    # def set_possession(self, possession, pos):
    #     self.possession = possession
    #     self.pos = pos
    #     while possession == True:
    #         self.rect.update((pos[0]*yard2px_width, pos[1]*yard2px_height), self.rect.size)
        

class Player(pygame.sprite.Sprite):
    def __init__(self, color, size, speed, role, ofb):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface(size)
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = Vector2()
        self.residual = Vector2()
        self.role = role
        self.possession = False
        self.ofb = ofb

    #player class update function
    def update(self):
        #INITIAL role will pull from dict
        if self.role == 'passer':
            self.update_passer()
            pass
        if self.role == 'blocker':
            #self.update_blocker()
            pass
        if self.role == 'receiver':
            self.update_receiver()
        if self.role == 'coverage':
            self.update_coverage()
            #so on and so forth
        if self.possession:
            ball.clamp_ip(self.rect)

    #boolean to determine player possession
    def set_possession(self, possession):
        self.possession = possession

    #sets initial play behavior for each player on the field      
    def set_route(self,route):
        self.route = route
        # if route == 'block':
        #     role = 'blocker'
        # elseif role = 'receiver'
        if self.route == "noroute":
            return
        self.route_index = 0
        self.set_target(self.route[self.route_index])

#receiver behavior   
    def update_receiver(self):
        """bring in route from previous function, hold pos if final target reached, update position towards target over time
        """
        if self.target == None:
            return    
        position=Vector2(self.rect.center)
        self.direction = (self.target - position)
        if self.direction.magnitude() < 12:
            self.next_target()
            return 
        distance = self.direction.normalize() * self.speed * 0.016
        distance += self.residual
        self.residual = Vector2(distance.x-int(distance.x), distance.y-int(distance.y))              
        self.rect.move_ip(distance) 

        nearest = min([Vector2(position - yeet.rect.center).magnitude() for yeet in defense_group])
        print(nearest)
        if nearest > 50:
            self.ofb = True
        else:
            self.ofb = False
            


    def set_position(self, pos):
        self.rect.update((pos[0]*yard2px_width, pos[1]*yard2px_height), self.rect.size)

    def set_target(self, rel_target):
        rel_target = Vector2(rel_target)*yard2px.elementwise()
        position = Vector2(self.rect.center)
        self.target = position + rel_target
    


#coverage behavior
    def set_coverage(self, coverage, man):
        """bring in coverage call out, make asignment based on position dictionary
        """
        self.coverage = coverage
        #print(Receiver.set_target(Player.target))
        
        # if self.coverage == (coverage(int(2)):
        #     #blitz()
        #     pass        

        #for man ... zone coverage later
        if self.coverage == 'man':
            #pass in offensive role from offensive and defensive position dictionaries
            self.target = man

    def update_coverage(self):
        """bring in coverage from previous function, set pos relative to zone or assigned player, update position over time
        """
        position = Vector2(self.rect.center)*yard2px.elementwise()
        target = Vector2(self.target.rect.center)*yard2px.elementwise()
        self.direction = (target - position)
        if self.direction.magnitude() == 0:
            return
        distance = self.direction.normalize() * self.speed * 0.016
        distance += self.residual
        self.residual = Vector2(distance.x-int(distance.x), distance.y-int(distance.y))
        self.rect.move_ip(distance)



    def next_target(self):
        self.route_index += 1
        #ends the route once the max number of index items (target points) is achieved
        if self.route_index == len(self.route):
            self.target = None
        #continue the route if target points remain
        else:
            self.set_target(self.route[self.route_index])
        
        
 #passer behavior
    def pass_ball(self):
        #survey players on field, check for open receiver
        if self.possession:
            for yeet in offense_group:
                if yeet.role == 'receiver' and yeet.ofb:
                    yeet.possession = True
                    #update role to runner tbd later
                    self.possession = False

    def update_passer(self):
        self.pass_ball()
        

    
    #def throw(self):
        #if open receiver, throw ball
        
def team_creation():
    offense_group = pygame.sprite.Group()
    offense = {
        "wrx": Player(red, player_size, random.randint(80,99), 'receiver', False),
        "wry": Player(red, player_size, random.randint(80,99), 'receiver', False),
        "qb": Player(red, player_size, 70, 'passer', False),
        "c": Player(red, player_size, 55, 'blocker', False)
    }

    defense_group = pygame.sprite.Group()
    defense = {
        "cb1": Player(blue, player_size, random.randint(80,99), 'coverage', False),
        "cb2": Player(blue, player_size, random.randint(80,99), 'coverage', False)
    }
    
    for pos, player in offense.items():
        offense_group.add(player)

    for pos, player in defense.items():
        defense_group.add(player)

    
        
    return(offense_group, defense_group, offense, defense)

formation_off = {
    "c": (0,0),
    "qb": (0,7),
    "wrx": (-20,0),
    "wry": (20,0)
}

formation_def ={
    "cb1": ["wrx",(-2,-5)],
    "cb2": ["wry",(2,-5)]
}

def position_routes(missionary, doggy):
    """missionary = position on the field relative to origin
    doggy = player ass
    """
    if missionary[0] < 0:
        available_route_groups = ['any', 'left']
    else:
        available_route_groups = ['any', 'right']
    if doggy == "qb" or doggy == "c":
        route = "noroute"
        return route
    available = {}
    for route_group in available_route_groups:
        for name, route in routes[route_group].items():
            available[name] = route
    route = random.choice(list(available.values()))
    return route

weed = None

def player_setup(origin):
    """pull in playcall from playbook, Set up the player formation relative to the origin (location of the center), assign routes and assignments based on playcall
    Args:
        origin (tuple): a tuple containing the abs x,y position of the ball at the start of the play
        formation (string): a string containing name of formation
    """

    # while game_state='snap':
    #     if pos == "qb":
    #         possession = True
    #         return possession

    for key, pos in formation_off.items():
        route = position_routes(pos, key)
        abs_pos=[sum(x) for x in zip(pos,origin)]
        offense[key].set_position(abs_pos)
        offense[key].set_route(route)
    offense["c"].set_possession(True)
    weed = offense["c"]

    for key, pos in formation_def.items():
        man, rel_pos = pos[0], pos[1]
        off_pos = formation_off[man]
        #i = random.choice(list(coverage))
        #print(i)
        abs_pos=[sum(x) for x in zip(rel_pos, off_pos, origin)]
        defense[key].set_position(abs_pos)
        defense[key].set_coverage(coverage['man'], offense[man])


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

routes={
    #re-program slants and sluggos to relative position... all routes are defined at each target relative to last position
    #routes to program
        #in, stop and go, hitch, drag, out, corner, post, fly, flat, wheel, swing, seam, angle
    "any":{
        "go":[(0,-300)],
        },
    "left":{
        "rslant":[(0,-5), (5,-10), (10,-15), (15,-20), (20,-25), (25,-30)],
        "rsluggo":[(0,-5), (5,-10), (10,-15), (10,-300)],
        "r_in":[(0,-5), (0,-5), (5,0), (5,0), (5,0), (5,0), (5,0)]
        },
    "right":{
        "lslant":[(0,-5), (-5,-10), (-10,-15), (-15,-20), (-20,-25), (-25,-30)],
        "lsluggo":[(0,-5), (-5,-10), (-10,-15), (-10,-300)],
        },
    "noroute":{
        "noroute": None
    }
}


coverage={
    'man':'man',
    'blitz':'blitz'
}


low_hanging_ball = Ball(black, ball_size, 300)
offense_group, defense_group, offense, defense = team_creation()
game_state = 'pp'


clock=pygame.time.Clock()


while True:
    dT=clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if game_state=='pp':
        player_setup((27,60))
        game_state='snap'
        #need some sort of snap function or code to randomize penalties, fumbles, etc
        offense["c"].set_possession(False)
        offense["qb"].set_possession(True)
        weed = offense["qb"]

    if game_state=='snap':
        offense_group.update()
        defense_group.update()
        low_hanging_ball.update()
        # Player.set_possession.update()

    # ballrect = ballrect.move(speed)
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = -speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]
    screen.fill(blue)
    draw_field(field_bounds)
    #draw possession of ball
    pygame.draw.rect(screen, brown, ball)
    offense_group.draw(screen)
    defense_group.draw(screen)
    # set_possession.draw(screen)
    # screen.blit()
    # screen.blit(ball, ballrect)
    pygame.display.flip()