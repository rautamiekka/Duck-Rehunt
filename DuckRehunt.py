#!/usr/bin/python
#-*- coding: UTF-8 -*-
'''NOTES:
    1|<"rautamiekka">|2011-05-15) Various indentations & extra blank lines to improve readability. Comments improved to explain the modifications. Augmented Assignment breaks the game.

'''
import pygame, random
pygame.init()

screen     = pygame.display.set_mode( (640,480) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.
screen_dim = screen.get_rect()

#Load in images. Lists replaced by tuples because of, for first, read-onlyness of the contained data; for second, higher performance.
dogImg = (
    pygame.image.load("DogIdle.gif"),
    pygame.image.load("DogDuck.gif"),
)

duckImg = (#Begin tuple.
    (#Inner tuple #1
        pygame.image.load("duckUD1.gif"),
        pygame.image.load("duckUD2.gif"),
        pygame.image.load("duckUD3.gif"),
    ),

    (#Inner tuple #2
        pygame.image.load("duckF1.gif"),
        pygame.image.load("duckF2.gif"),
        pygame.image.load("duckF3.gif"),
    ),

    (#Inner tuple #3
        pygame.image.load("duckShot.gif"),
    ),

    (#Inner tuple #4
        pygame.image.load("duckFall.gif"),
        pygame.transform.flip(pygame.image.load("duckFall.gif"), True, False),
    ),
)#End tuple.

negaDuckImg = (#Begin tuple.
    (#Inner tuple #1
        pygame.image.load("DarkwingSp.gif"),
    ),

    (#Inner tuple #2
        pygame.image.load("DarkwingFlap.gif"),
        pygame.image.load("DarkwingFlap2.gif"),
    ),
)#End tuple.

#Load in Sound
gunshot  = pygame.mixer.Sound("Gunshot.ogg")
quack    = pygame.mixer.Sound("Quack.ogg")

dSprites = pygame.sprite.Group()
flash    = pygame.sprite.Group()

score    = 0

"""Duck sprites are 136x124"""
class NegaDuck(pygame.sprite.Sprite):
    def __init__(self, dogHand):
        pygame.sprite.Sprite.__init__(self)
        self.image         = negaDuckImg[0][0]
        self.image         = self.image.convert()
        self.image.set_colorkey( (0,0,255) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.
        self.rect          = self.image.get_rect()
        self.rect.center   = (dogHand.rect.center)
        self.rect.centerx += 60
        self.changeDelay   = 0
        self.dog           = False
        self.enemy         = True

        #Death Animation Vars
        self.isDead    = False
        self.deadDelay = 10

        #Normal Animation Vars
        self.anim      = []
        self.animDelay = 15
        self.frame     = 0
        self.pause     = 0


        while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
            self.dx = random.randrange(-4,4)
            self.dy = random.randrange(-4,4)

            if not (self.dx,self.dy) == (0,0):
                break

        ##if score >= 100:
            ##self.dx *= 1.2
            ##self.dy *= 1.2

        self.setAnim()

    def update(self):
        if not self.isDead:
            self.rect.centerx += self.dx
            self.rect.centery += self.dy
            ##self.changeDelay += 1

            ##if self.changeDelay > 5:
                ##self.changeDelay = 0

            self.changeDir()
            self.animate()
        else:
            self.anidead()

    def anidead(self):
        self.rect.centery += 3
        self.pause        += 1

        if self.pause < 5:
            self.image = duckImg[2][0]
            self.image.set_colorkey( (0,0,255) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.
        elif self.pause >= self.deadDelay:
            self.frame += 1
            self.pause  = 5

            if self.frame >= len(self.anim):
                self.frame = 0

            self.image = self.anim[self.frame]

            self.image.set_colorkey( (0,0,255) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.

    def animate(self):
        self.pause += 1

        if self.pause >= self.animDelay:
            self.frame += 1
            ##print(self.frame)#To be Py v3.x-compliant, PRINT keyword must be used as a Function instead.
            self.pause  = 0

            if self.frame >= len(self.anim):
                self.frame = 0

            self.image = self.anim[self.frame]

            if self.dx < 0:
                self.image = pygame.transform.flip(self.image, True, False)

            self.image.set_colorkey( (0,0,255) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.

    def changeDir(self):
        if self.rect.left < 0:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx        = random.randrange(0,4)
                self.dy        = random.randrange(-4,4)
                self.rect.left = 0

                if (self.dx,self.dy) != (0,0):
                    break

        if self.rect.right > 640:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx = random.randrange(-4,0)
                self.dy = random.randrange(-4,4)
                self.rect.right = 640

                if (self.dx,self.dy) != (0,0):
                    break

        if self.rect.top < 0:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx       = random.randrange(-4,4)
                self.dy       = random.randrange(0,4)
                self.rect.top = 0

                if (self.dx,self.dy) != (0,0):
                    break

        if self.rect.bottom > 301:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx          = random.randrange(-4,4)
                self.dy          = random.randrange(-4,0)
                self.rect.bottom = 301

                if (self.dx,self.dy) != (0,0):
                    break

        self.setAnim()

    def setAnim(self):
        self.anim = negaDuckImg[0] if self.isDead else negaDuckImg[1]#Less lines with same result.

class Duck(pygame.sprite.Sprite):
    def __init__(self, dogHand):
        pygame.sprite.Sprite.__init__(self)
        self.image         = duckImg[2][0]
        self.image         = self.image.convert()
        self.image.set_colorkey( (136,216,0) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.
        self.rect          = self.image.get_rect()
        self.rect.center   = dogHand.rect.center
        self.rect.centerx += 60
        self.changeDelay   = 0
        self.dog           = False
        self.enemy         = False

        #Death Animation Vars
        self.isDead    = False
        self.deadDelay = 10

        #Normal Animation Vars
        self.anim      = []
        self.animDelay = 15
        self.frame     = 0
        self.pause     = 0


        while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
            self.dx = random.randrange(-4,4)
            self.dy = random.randrange(-4,4)

            if not (self.dx,self.dy) == (0,0):
                break

        ##if score >= 100:
            ##self.dx *= 1.2
            ##self.dy *= 1.2

        self.setAnim()

    def update(self):
        if not self.isDead:
            self.rect.centerx  += self.dx
            self.rect.centery  += self.dy
            ##self.changeDelay += 1

            ##if self.changeDelay > 5:
                ##self.changeDelay = 0

            self.changeDir()
            self.animate()
        else:
            self.anidead()

    def anidead(self):
        self.rect.centery += 3
        self.pause        += 1

        if self.pause < 5:
            self.image = duckImg[2][0]
            self.image.set_colorkey( (136,216,0) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.
        elif self.pause >= self.deadDelay:
            self.frame += 1
            self.pause  = 5

            if self.frame >= len(self.anim):
                self.frame = 0

            self.image = self.anim[self.frame]
            self.image.set_colorkey( (136,216,0) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.

    def animate(self):
        self.pause += 1

        if self.pause >= self.animDelay:
            self.frame += 1
            ##print(self.frame)#To be Py v3.x-compliant, PRINT keyword must be used as a Function instead.
            self.pause = 0

            if self.frame >= len(self.anim):
                self.frame = 0

            self.image = self.anim[self.frame]

            if self.dx < 0:
                self.image = pygame.transform.flip(self.image, True, False)

            self.image.set_colorkey( (136,216,0) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.

    def changeDir(self):
        if self.rect.left < 0:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx        = random.randrange(0,4)
                self.dy        = random.randrange(-4,4)
                self.rect.left = 0

                if (self.dx,self.dy) != (0,0):
                    break

        if self.rect.right > 640:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx         = random.randrange(-4,0)
                self.dy         = random.randrange(-4,4)
                self.rect.right = 640

                if (self.dx,self.dy) != (0,0):
                    break

        if self.rect.top < 0:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx       = random.randrange(-4,4)
                self.dy       = random.randrange(0,4)
                self.rect.top = 0

                if (self.dx,self.dy) != (0,0):
                    break

        if self.rect.bottom > 301:
            while 1:#Since True already resolves into 1, we speed up things a little by replacing True with 1.
                self.dx = random.randrange(-4,4)
                self.dy = random.randrange(-4,0)
                self.rect.bottom = 301

                if (self.dx,self.dy) != (0,0):
                    break

        self.setAnim()

    def setAnim(self):
        self.anim = duckImg[1] if self.dy == 0 else duckImg[0]#Less lines with same result.

        if self.isDead:
            self.anim = duckImg[3]

class Dog(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image        = dogImg[1]
        self.image        = self.image.convert()

        self.image.set_colorkey( (0,0,255) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.

        self.rect         = self.image.get_rect()
        self.rect.center  = (random.randrange(45,595),440)
        self.spawn        = True
        self.release      = False
        self.retreat      = False
        self.enemy        = False
        self.dog          = True
        self.releaseSpeed = 2
        self.negaCounter  = 0

        global score

    def update(self):
        global score

        self.releaseSpeed = 4 if score >= 100 else 5 if score >= 300 else 2#Less lines with same result.

        if self.spawn:
            self.rect.centery -= self.releaseSpeed

            if self.rect.top <= 200:
                self.spawn   = False
                self.release = True
                self.retreat = False
                self.image   = dogImg[0]
                self.image.set_colorkey( (0,0,255) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.
        elif self.release:
            self.negaCounter += 1

            if len( dSprites.sprites() ) > 6 and self.negaCounter >= 6:#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.
                dSprites.add( NegaDuck(self) )#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.
                self.negaCounter = 0
            else:
                dSprites.add( Duck(self) )#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.
                quack.play()

            self.spawn   = False
            self.release = False
            self.retreat = True
        elif self.retreat:
            self.rect.centery += self.releaseSpeed

            if self.rect.top > 320:
                self.spawn   = True
                self.retreat = False
                self.release = False
                self.reset()

    def reset(self):
        self.rect.center = (random.randrange(45,595),440)
        self.spawn       = True
        self.image       = dogImg[1]
        self.image.set_colorkey( (0,0,255) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.


class setPiece(pygame.sprite.Sprite):
    def __init__(self, image, topleft):
        pygame.sprite.Sprite.__init__(self)

        self.image        = image
        self.image        = self.image.convert()
        self.rect         = self.image.get_rect()
        self.rect.topleft = topleft

    def update(self):
        pass#The PASS keyword is used where nothing must be done, like here.

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image       = pygame.image.load("Crosshair.gif")
        self.image       = self.image.convert()
        self.rect        = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Flash(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image       = pygame.image.load("Gunshot.gif")
        self.image       = self.image.convert()
        self.rect        = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.pause       = 0

    def update(self):
        self.pause += 1

        if self.pause >= 5:
            flash.remove(self)

def main():
    pygame.display.set_caption("Duck Rehunt: Reckoning")
    pygame.mixer.init()
    pygame.mixer.Sound("Music.ogg").play(-1)

    background = pygame.Surface( screen.get_size() )#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.
    background.blit( pygame.image.load("Background.gif"), (0,0) )#Better readibility by separating the brackets of the inside Function & tuple from the brackets of the outside Function.
    screen.blit( background, (0,0) )#Better readibility by separating the brackets of the tuple from the brackets of the Function.

    foreground = setPiece( pygame.image.load("Foreground.gif"), (0,301) )#Better readibility by separating the brackets of the inside Function & tuple from the brackets of the outside Function.
    setSprites = pygame.sprite.Group(foreground)

    dSprites.add( Dog() )#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.

    crosshair = pygame.sprite.Group( Crosshair() )#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.

    keepGoing = True
    pause     = shotScore = 0
    delay     = 60

    global score

    scoreFont  = pygame.font.Font("HelveticaWorld.ttf",20)
    scoreboard = scoreFont.render( "Score: %d" % score, 1, (255,255,255) )#Better readibility by separating the brackets of the tuple and the Function parameters from the brackets of the Function.

    clock = pygame.time.Clock()

    while keepGoing:
        clock.tick(60)
        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gunshot.play()
                flash.add( Flash() )#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.

                pointCollide = [#Begin List Comprehension
                    sprite for sprite in dSprites.sprites() if sprite.rect.collidepoint( pygame.mouse.get_pos() )#Better readibility by separating the brackets of the inside Function from the brackets of the outside Function.
                ]#End List Comprehension

                if pointCollide != []:
                    for sprite in pointCollide:
                        if not sprite.dog and not sprite.isDead:
                            sprite.isDead = True
                            sprite.pause = 0

                            if sprite.enemy:#Here we can't use Ternary Operation because of different in-place operators.
                                shotScore -= 50
                            else:
                                shotScore += 5

                            sprite.setAnim()

                    shotScore  *= len(pointCollide)
                    score      += shotScore
                    shotScore   = 0
                    scoreboard  = scoreFont.render( "Score: %d" % score, 1, (255,255,255) )#Better readibility by separating the brackets of the tuple and the Function parameters from the brackets of the Function.


        #Garbage collection
        pause += 1
        if pause >= delay:
            dSprites.remove( [sprite for sprite in dSprites.sprites() if sprite.rect.centery >= 500] )

        dSprites.clear(screen, background)
        crosshair.clear(screen, background)
        flash.clear(screen, background)

        dSprites.update()
        crosshair.update()
        flash.update()

        dSprites.draw(screen)
        setSprites.draw(screen)
        screen.blit( scoreboard, (500,440) )#Better readibility by separating the brackets of the tuple and the Function parameter from the brackets of the Function.
        flash.draw(screen)
        crosshair.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()

pygame.quit()