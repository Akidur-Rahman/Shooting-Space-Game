import pygame,sys

# Game Setup
pygame.init()
display_width,display_height = 800,600
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("No Caption")
clock  = pygame.time.Clock()

# print(pygame.font.get_fonts())


class scorebar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.trans_width = 50
        self.minus = 10
        self.green = 50
    def update(self,up,down):
        if up and self.green<200:
            self.green +=5
        elif down and self.width>10:
            self.width -=5
            self.green -=5

        if self.width < self.green:
            self.width +=2
        if self.trans_width> self.width:
            self.trans_width-=2
        else:
            self.trans_width = self.width

        pygame.draw.rect(display,(0,255,0),(400,300,self.green,30))
        pygame.draw.rect(display,(255,255,0),(400,300,self.trans_width,30))
        pygame.draw.rect(display,(255,0,0),(400,300,self.width,30))
        pygame.draw.rect(display,(0,0,0),(400,300,200,30),3)

score = scorebar()
score_group = pygame.sprite.Group()
score_group.add(score)

up, down = False,False
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        up = True
    elif keys[pygame.K_DOWN]:
        down = True
    else:
        up = False
        down = False

    display.fill((255,255,255))
    score_group.update(up,down)
    pygame.display.update()