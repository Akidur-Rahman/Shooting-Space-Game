import pygame, sys, random

# Game Setup
pygame.init()
display_width,display_height = 1100,690
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Shoting Game")
clock  = pygame.time.Clock()
textfont = pygame.font.SysFont("verdana",20)

# Global variables
background_start = 200
background_end = 1050
background_pic_size = display_width - 250
kill_count = 0

# Image
player_pic = "Jet.png"
enemy_jet_1 = "enemy jet 1.png"
background_pic = pygame.image.load("Background space.jpg")
background_pic = pygame.transform.scale(background_pic,(background_pic_size,display_height))
life_pic = pygame.image.load("life.png")
life_pic = pygame.transform.scale(life_pic,(35,35))

fighter_jet_pic = pygame.image.load("Enemy fighter jet.png")
fighter_jet_pic = pygame.transform.scale(fighter_jet_pic,(100,100))
fighter_jet_pic = pygame.transform.rotate(fighter_jet_pic,180)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, Player_pic):
        super().__init__()
        self.y = 600
        self.border_dis = 30
        self.image = pygame.image.load(Player_pic)
        self.image = pygame.transform.scale(self.image,(150,150))
        self.rect = self.image.get_rect()
        self.rect.center = 500,600
        pygame.mouse.set_pos(500,600)
    # Health
        self.width = 150
        self.trans_width = 150
        self.green = 150
        self.health_max = 180
    def update(self):
    # Movement Of Player
        if pygame.mouse.get_pos()[0] - self.border_dis >= background_start and pygame.mouse.get_pos()[0] + self.border_dis <= background_end:
            self.rect.center = pygame.mouse.get_pos()[0],self.y

    # Collision
        if pygame.sprite.spritecollide(self,life_groupp,True):
            self.player_hp(True,False)
        if pygame.sprite.spritecollide(self,enemy_group,True):
            self.player_hp(False,True)
        else:
            self.player_hp(False,False)
        
    def player_hp(self,plus,minus):
        if plus and self.green + 100<self.health_max:
            self.green +=100
        elif plus:
            plus_hp = self.health_max - self.green
            self.green +=plus_hp
        elif minus and self.width>10:
            self.width -=40
            self.green -=40
        
        if self.width < self.green:
            self.width +=1
        if self.trans_width> self.width:
            self.trans_width-=1
        else:
            self.trans_width = self.width

        pygame.draw.rect(display,(0,255,0),(10,10,self.green,30))
        pygame.draw.rect(display,(255,255,0),(10,10,self.trans_width,30))
        pygame.draw.rect(display,(255,0,0),(10,10,self.width,30))
        pygame.draw.rect(display,(0,0,0),(10,10,self.health_max,30),3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos,direction, color):
        super().__init__()
        self.image = pygame.Surface([7,20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.direction = direction
    def update(self):
        # if self.direction >0:
        #     self.rect.x = pos +45
        self.rect.y += 10 *self.direction
        # To Kill Bullets
        if self.rect.y <= 0:
            self.kill()
        # #Check collision with enemy
        # collide = pygame.sprite.spritecollide(self,enemy_group,False)
        # for enemy in  collide:
        #     enemy.scorebar_hit()
        #     #enemy_group.sprites()[0].scorebar_hit()
        #     self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_pic):
        super().__init__()
        self.image = pygame.image.load(enemy_pic)
        self.image = pygame.transform.scale(self.image,(50,50))
        self.image = pygame.transform.rotate(self.image,180)
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(background_start +25, background_end -25),-50
        # Scorebar
        self.health = 50            
        self.health_minus = 20
        self.score_time = 500
    def update(self):
        global kill_count

        self.rect.y +=2
        if self.rect.y >= display_height:
            self.kill()

        if self.health <=0:
            kill_count+=1
            # LIFE 
            if kill_count % 19 ==0:
                life_groupp.add(Life(self.rect.center))
            self.kill()
    # Scorebar
        if self.score_time<100:
            self.scorebar_draw()
            self.score_time+=1
        if pygame.sprite.spritecollide(self,bullet_group,True):
            self.scorebar_hit()
    def scorebar_hit(self):
        self.health -= self.health_minus
        self.score_time =0
    def scorebar_draw(self):
        pygame.draw.rect(display,(255,0,0),(self.rect.x +5, self.rect.y-25,self.health,10))

class Life(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = life_pic
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.y +=2
        if self.rect.y >= display_height:
            self.kill()

class Fighter_jet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fighter_jet_pic
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(background_start +50, background_end -50),-60
        #Jet velocity
        self.vel_x = random.randint(0,1)
        if self.vel_x == 0:
            self.vel_x = -1
        self.vel_y = 1
        self.y_pos = False
        # Scorebar
        self.health = 90        
        self.health_minus = 5
        self.score_time = 500
        self.fj_bullet = pygame.sprite.Group()
    def update(self):
        global kill_count
    
    # Bullet of Enemy Jet
        if fj_bullet_slower.check(10):
            self.fj_bullet.add(Bullet(self.rect.center,1,(255,0,0)))
        self.fj_bullet.draw(display)
        self.fj_bullet.update()

    # Movement of Enemy Jet
        self.move()
    # Kill if health is Zero
        if self.health <=0:
            kill_count+=1
    # LIFE Element
            if kill_count % 19 ==0:
                life_groupp.add(Life(self.rect.center))
            self.kill()        
    # Scorebar
        if self.score_time<150:
            self.scorebar_draw()
            self.score_time+=1
        if pygame.sprite.spritecollide(self,bullet_group,True):
            self.scorebar_hit()
    def scorebar_hit(self):
        self.health -= self.health_minus
        self.score_time =0
    def scorebar_draw(self):
        pygame.draw.rect(display,(255,0,0),(self.rect.x +5, self.rect.y-25,self.health,10))
    def move(self):
        self.rect.x +=2*self.vel_x
        self.rect.y += 2*self.vel_y

        if self.rect.x <=background_start or self.rect.x +100 >= background_end:
            self.vel_x *= -1
        if self.rect.y +100 >= display_height:
            self.vel_y *= -1
            self.y_pos = True
        elif self.rect.y <= 0 and self.y_pos:
            self.vel_y *= -1

class Time_slower():
    def __init__(self):
        self.count = 0
    def check(self,num):
        if self.count <= num:
            self.count+=1
            return False
        else:
            self.count = 0
            return True

# Player
player = Player(player_pic)
player_group = pygame.sprite.Group()
player_group.add(player)

# OBJECTS Group
bullet_group = pygame.sprite.Group()    # Bullet
enemy_group = pygame.sprite.Group()     # Enemy
life_groupp = pygame.sprite.Group()     # Life Group
fighter_jet_group = pygame.sprite.Group()

# Objects
bullet_slower = Time_slower()
enemy_slower = Time_slower()
fighter_jet_slower = Time_slower()
fj_bullet_slower = Time_slower()
# Variable
fighter_jet_list = []
mouse_left = False
i=0
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_left = True
            if event.button == 3:
                mouse_left = False
    
# Bullet
    if mouse_left and bullet_slower.check(10):
        bullet_group.add(Bullet(player.rect.center,-1,(0,255,0)))
# Enemy
    if enemy_slower.check(100):
        enemy_group.add(Enemy(enemy_jet_1))

# Fighter jet 
    if fighter_jet_slower.check(1000):
        fighter_jet_list.append(Fighter_jet())
        fighter_jet_group.add(fighter_jet_list[i])
        i +=1

# DRAW
    display.fill((255,255,255))
    #text = textfont.render("kills: {0}".format(kill_count),0,(0,0,0))
    text = textfont.render(("Kills: %s" % kill_count),1,(0,0,0))
    display.blit(text,(50,50))

    display.blit(background_pic,(background_start,0))
    fighter_jet_group.draw(display)
    enemy_group.draw(display)
    life_groupp.draw(display)
    bullet_group.draw(display)
    player_group.draw(display)

    fighter_jet_group.update()
    life_groupp.update()
    enemy_group.update()
    bullet_group.update()
    player_group.update()

    #for j in fighter_jet_list:
        #fj_bullet_group.update(self.rect.x)
    pygame.display.update()