
import os, random, pygame, math

#Gameboard 800 x 600

class Player():
    def __init__(self):
        self.length = 60
        self.height = 5
        self.x = 400
        self.y = 480
        self.speed = 20
        self.ballsLeft = 3

    def PlayerMove(self,event,ball,demo):
        self.mousePos = pygame.mouse.get_pos()
        if (demo == False):
            self.x = self.mousePos[0]
        else:
            self.x = ball.x
        
    def ShootBall(self,ball,event):
        if ball.held == True and self.ballsLeft > 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.held = False
                    ballAngle = math.radians(random.randint(45,60))
                    ball.vel[0] = ball.speed*math.cos(ballAngle)
                    ball.vel[1] = -1*math.sqrt((ball.speed**2)-(ball.vel[0]**2))

    def DrawPlayer(self,game):
        pygame.draw.rect(game.display,(128,128,128),[int(self.x-self.length/2),int(self.y-self.height/2),self.length,self.height])

class Block():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.height = 20
        self.width = 80
        self.drawX = (x*self.width)-(self.width/2)
        self.drawY = (y*self.height)-(self.height/2)
        self.leftWall = self.x-(self.width/2)
        self.rightWall = self.x+(self.width/2)
        self.topWall = self.y-(self.height/2)
        self.botWall = self.y+(self.height/2)
        self.colors = {1:(148,0,211),2:(75,0,130),3:(0,0,255),4:(0,255,0),5:(255,255,0),6:(255,127,0),7:(255,0,0)}
        self.color = self.colors[z]

class Ball():
    def __init__(self,player):
        self.vel = [0,0]
        self.color = (255,255,255)
        self.x = player.x
        self.y = player.y+10
        self.radius = 5
        self.held = True
        self.speed = 6

    def Bounce(self,player,game,wallDirection,demo):
        if wallDirection == 'rl':
            self.vel[0] = self.vel[0]*-1
        elif wallDirection == 'ud':
            self.vel[1] = self.vel[1]*-1
        else:
            fract = (self.x-player.x)/(player.length/2)
            if (demo == True):
                fract = random.random()*0.8
            self.vel[0] = math.copysign(1,fract)*math.copysign(1,self.vel[0])*self.speed*math.fabs(fract)
            self.vel[1] = -1*math.sqrt((self.speed**2)-(self.vel[0]**2))
            
    def DrawBall(self,game):
        pygame.draw.circle(game.display,(255,255,255),[int(self.x),int(self.y)],int(self.radius))

    def HeldBall(self,player):
        if (self.held == True):
            self.x = player.x
            self.y = player.y-self.radius-player.height+1

    def MoveBall(self,player,game,demo):
        self.CollisionCheck(player,game,demo)
        self.x += self.vel[0]
        self.y += self.vel[1]
    
    def CollisionCheck(self,player,game,demo):
        self.gridx1 = int(self.x//80)+1
        self.gridy1 = int(self.y//20)+1

        self.gridx2 = int((self.x+self.vel[0])//80)+1
        self.gridy2 = int((self.y+self.vel[1])//20)+1

        if (self.y > 700):
            if (player.ballsLeft > 0):
                self.held = True
                player.ballsLeft -= 1
            else:
                self.held = False
                self.vel = [0,0]

        if (self.y < 0):
            self.Bounce(player,game,'ud',demo)

        if (self.x < 0 or self.x > 800):
            self.Bounce(player,game,'rl',demo)

        if ((player.x-player.length/2) < self.x < (player.x+player.length/2)) and (player.y+5 < self.y < player.y+10):
            self.Bounce(player,game,'na',demo)

        if not (self.gridx1 == self.gridx2 and self.gridy1 == self.gridy2):
            for block in game.blockList:
                if (self.gridx2 == block.x and self.gridy2 == block.y):
                    game.blockList.remove(block)
                    game.score += 1000
                    if (self.gridx1 == self.gridx2):
                        self.Bounce(player,game,'ud',demo)
                    elif (self.gridy1 == self.gridy2):
                        self.Bounce(player,game,'rl',demo)
                    else:
                        self.Bounce(player,game,'ud',demo)
                        self.Bounce(player,game,'rl',demo)

class Game():
    def __init__(self):
        self.blockList = []
        self.display = pygame.display.set_mode((800,600))
        self.gameOver = False
        self.clock = pygame.time.Clock()
        self.score = 0
        self.gamedOver = False
        self.win = False

    def CreateGame(self):
        for i in range(1,11): #11
            for j in range(2,8): #8
                k = 9-j
                self.newBlock = Block(i,j,k)
                self.blockList.append(self.newBlock)
    
    def DrawWalls(self):
        for block in self.blockList:
            pygame.draw.rect(self.display,(255,255,255),[int(block.drawX-(block.width/2)),int(block.drawY-(block.height/2)),block.width,block.height])
            pygame.draw.rect(self.display,block.color,[int(block.drawX-(block.width/2)+1),int(block.drawY-(block.height/2)+1),block.width-2,block.height-2])

def UpdateScore(game):
    scoreText = gameFont.render(' SCORE: '+str(int(game.score))+' ',True,(255,255,255),(0,0,0))
    game.display.blit(scoreText,(30,550))
    if (len(game.blockList) == 0):
        game.win = True
        game.gameOver = True

def UpdateLives(game,player):
    livesText = gameFont.render(' LIVES: '+str(int(player.ballsLeft))+' ',True,(255,255,255),(0,0,0))
    game.display.blit(livesText,(180,550))

    if (player.ballsLeft == 0):
        game.gameOver = True

def QuitGame(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            os._exit(1)

pygame.init()
player = Player()
ballList = [Ball(player)]
game = Game()
game.CreateGame()
pygame.display.set_caption('Breakout')

demo = True

gameFont = pygame.font.SysFont('8bitOperatorPlus-Regular.ttf', 20)
scoreText = gameFont.render(' SCORE: '+str(int(game.score))+' ',True,(0,0,0), (255,255,255))
livesText = gameFont.render(' SCORE: '+str(int(player.ballsLeft))+' ',True,(0,0,0), (255,255,255))

restartText = gameFont.render('Press Enter to Restart',True,(255,255,255),(0,0,0))
restartRect = restartText.get_rect()
restartRect.center = (400,350)

def GameOverText(win):
    gameOverFont = pygame.font.SysFont('8bitOperatorPlus-Regular.ttf', 100)
    if (win == False):
        gameOverText = gameOverFont.render('GAME OVER',True,(255,255,255),(0,0,0))
    else:
        gameOverText = gameOverFont.render('YOU WIN',True,(255,255,255),(0,0,0))
    gameOverRect = gameOverText.get_rect()
    gameOverRect.center = (400,300)
    return (gameOverText,gameOverRect)

while True:
    pygame.draw.rect(game.display,(0,0,0),[0,0,800,600])
    for event in pygame.event.get():
        player.ShootBall(ballList[0],event)
        if (demo == False):
            player.PlayerMove(event,ballList[0],demo)
        QuitGame(event)
        if (game.gameOver == True):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player = Player()
                game = Game()
                game.CreateGame()
    if (demo == True):
        player.PlayerMove(event,ballList[0],demo)
    ballList[0].HeldBall(player)
    ballList[0].MoveBall(player,game,demo)
    ballList[0].DrawBall(game)

    player.DrawPlayer(game)
    game.DrawWalls()

    UpdateScore(game)
    UpdateLives(game,player)

    if (game.gameOver == False):
        pygame.display.update()
    else:
        if (game.gamedOver == False):
            (gameOverText,gameOverRect) = GameOverText(game.win)
            game.display.blit(gameOverText,gameOverRect)
            game.display.blit(restartText,restartRect)
            pygame.display.update()
            game.gamedOver = True
            
    game.clock.tick(120)

