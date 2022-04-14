import pygame
import random
import os
#run "pip install pygame" in terminal

pygame.mixer.init()

pygame.init()

width = 900
height = 500

white = (255, 255, 255)
red = (255, 0, 0)
black = (0,0,0)

fps = 30
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def showText(text, color, x, y):
    screenText = font.render(text, True, color)
    gameWindow.blit(screenText, [x,y])

def plotSnake(gameWindow, color, snakeList, snakeSize):
    for x,y in snakeList:
        pygame.draw.rect(gameWindow, color, [x, y, snakeSize, snakeSize])

#creating window and giving it a title
gameWindow = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

def welcome():
    exitGame = False

    while not exitGame:
        gameWindow.fill((233, 220, 229))
        showText("Welcome to Snakes", black, 260, 200)
        showText("Press Space Bar to Play", black, 240, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    try:
                        pygame.mixer.music.load("bgmusic.mp3")
                        pygame.mixer.music.play()
                    except:
                        pass
                    gameLoop()

        pygame.display.update()
        clock.tick(fps)


def gameLoop():
    exitGame = False
    gameOver = False

    snakeSize = 10
    score = 0
    snakeList = []
    snakeLength = 1

    foodX = random.randint(20, width//1.5)
    foodY = random.randint(20, height//1.5)

    snakeX = 45
    snakeY = 55

    velocityX = 0
    velocityY = 0
    newVelocity = 5

    if not os.path.exists("highscore.txt"):
        with open ("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as g:
        highScore = g.read()

    while not exitGame:
        #the update function is needed everytime when the window is modified
        gameWindow.fill(white)
        showText(f"Score: {score}      High Score: {highScore}", black, 5, 5)

        head = []
        head.append(snakeX)
        head.append(snakeY)
        snakeList.append(head)
        print(head)
        print(snakeList)

        if gameOver:
            gameWindow.fill(white)
            showText(f"Game Over! Score: {score}", black, width//4, height//3)
            showText(f"Press Enter To Continue", black, width//4, (height//3)+40)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            if (snakeX < 0) or (snakeX > width) or (snakeY < 0) or (snakeY > height):
                gameOver = True
                try:
                    pygame.mixer.music.load("explosion.mp3")
                    pygame.mixer.music.play()
                except:
                    pass

            if len(snakeList) > snakeLength:
                del snakeList[0]

            if head in snakeList[:-1]:
                gameOver = True
                try:
                    pygame.mixer.music.load("explosion.mp3")
                    pygame.mixer.music.play()
                except:
                    pass


            plotSnake(gameWindow, black, snakeList, snakeSize)
            pygame.draw.rect(gameWindow, red, [foodX, foodY, snakeSize, snakeSize])
            pygame.display.update()
            clock.tick(fps)

            #pygame.event.get function will get all the event for example - pressing of a button
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exitGame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocityX = newVelocity
                        velocityY = 0

                    elif event.key == pygame.K_LEFT:
                        velocityX = -newVelocity
                        velocityY = 0

                    elif event.key == pygame.K_DOWN:
                        velocityX = 0
                        velocityY = newVelocity

                    elif event.key == pygame.K_UP:
                        velocityX = 0
                        velocityY = -newVelocity

            snakeX += velocityX
            snakeY += velocityY

            if abs(snakeX - foodX) < 6 and abs(snakeY - foodY) < 6:
                score = score + 10
                if score > int(highScore):
                    with open("highscore.txt", "w") as f:
                        highScore = score
                        f.write(str(score))
                foodX = random.randint(20, width//1.5)
                foodY = random.randint(20, height//1.5)
                snakeLength += 5

    pygame.quit()
    quit()

welcome()



