#you know what this is
import pygame,random,thread
pygame.init()

#declared variables to be established
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
dark_green = (0,125,0)
dark_blue = (0,0,125)
yellow = (255,255,0)
display_width = 1200
display_height = 900
FPS = 25
block_size = 15
water_size = 270
water_size2 = 150
gameExit = False
title = True
rules = False
death = "alive!"
apples_eaten = "apples!"
NumApples = 0
direction = "right"
aniStart = 0
bite = pygame.mixer.Sound('bite.wav')
splash = pygame.mixer.Sound('splash.wav')
splat = pygame.mixer.Sound('splat.wav')
#tick = pygame.mixer.Sound('tick.wav')

#loads a sprite (image) (must be in same directory as game)

img = pygame.image.load('SnakeHead.png')    
water1 = pygame.image.load('WaterTile.png')
water2 = pygame.image.load('WaterTile2.png')
appleimage = pygame.image.load('Apple.png')
grass = pygame.image.load('grass.png')
flower = pygame.image.load('flower.png')
snakeimg = pygame.image.load('snake.gif')

#If you dont put your picture file in the same directory you need to enter the 
#path where it can be loaded from using forward slashes instead of backslashes:
#('c:/Python27/Games/SnakeGame/image_files/SnakeHead.png') for example.

def snake(block_size,snakelist):
    #pygame can rotate images (dont create multiple image files to load, that is sloppy)
    if direction == "right":
        head = pygame.transform.rotate(img,270) #<-- rotates image 270 degrees
    if direction == "left":
        head = pygame.transform.rotate(img,90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img,180)
        
    gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))#<--places snake head image to location
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, dark_green,[XnY[0],XnY[1],block_size,block_size])
        #draws additional blocks behind snake (when called)

#functions to display text

def message_to_screen(msg,color,line,column):
    screen_text = font.render(msg,True,color)
    gameDisplay.blit(screen_text,[line,column]) #<--your text position
def message_to_screen2(msg,color,line,column):
    screen_text = font2.render(msg,True,color)
    gameDisplay.blit(screen_text,[column,line])

def message_2_screen(msg,color,line,column):
    screen_text = font3.render(msg,True,color)
    gameDisplay.blit(screen_text,[line,column])
    
#sets font sizes for message functions

#Sysfont is the file of fonts. "None" is what font type it is.
font3 = pygame.font.SysFont("comicsansms",20)
font = pygame.font.SysFont("comicsansms",60)#<--font size
font2 = pygame.font.SysFont("comicsansms",35)

#pre sets to establish screen height, width and game title
gameDisplay = pygame.display.set_mode((display_width,display_height),0,32)
pygame.display.set_caption('Serpentine')

#sets the icon on the window bar next to your game title
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
#This also resizes the image to 32x32 pixel size which may distort it

clock =  pygame.time.Clock()
randLakeX,randLakeY,randLake2X,randLake2Y=0,0,0,0

#pause function
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        message_to_screen2("Paused",black,(display_width/2-250),(display_width/2-80))
        message_to_screen2("Press 'C' to continue or 'Q' to quit",black,(display_width/2-200),(display_height/2-150))
        pygame.display.update()
        clock.tick(5)
    
def gameLoop():
    #insert your variables into the function so they work
    global direction,randLakeX,randLakeY,randLake2X,randLake2Y
    
    def lakeRandomize():
        global randLakeX,randLakeY,randLake2X,randLake2Y
        randLakeX = round(random.randrange(100,(display_width-water_size-100))/30.0)*30.0
        randLakeY = round(random.randrange(100,(display_height-water_size-100))/30.0)*30.0 
        randLake2X = round(random.randrange(100,(display_width-water_size2-100))/30.0)*30.0
        randLake2Y = round(random.randrange(100,(display_height-water_size2-100))/30.0)*30.0 
        if (display_width/2 >= randLakeX and display_width/2 <= randLakeX+water_size) and (display_height/2 >= randLakeY and display_height/2 <= randLakeY + water_size):
            lakeRandomize()
        if (display_width/2 >= randLake2X and display_width/2 <= randLake2X + water_size2) and (display_height/2 >= randLake2Y and display_height/2 <= randLake2Y + water_size2):
            lakeRandomize()
    lakeRandomize()
    
    startAnimation()
    NumApples = 0
    snakeList = []
    snakeLength = 1
    gameExit = False
    gameOver = False
    title = False
    rules = False
    #waterTileX,waterTileY=0,0
    
    #defines where your snake starts and which direction it should start going
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0
    
    #sets position for apples and rounds them to force a grid positioning system
    randAppleX = round(random.randrange(100,(display_width-100)))    #/15.0)*15.0 
    randAppleY = round(random.randrange(100,(display_height-100)))   #/15.0)*15.0 
    randFlowerX = random.randrange(60,(display_width-60))
    randFlowerY = random.randrange(60,(display_height-60))
    
    while not gameExit:
    
        apples_eaten = "              Your serpent ate %d apples!" % NumApples
        
        #water collision that ends game
        #border water
        if lead_x < 30 or lead_x > display_width-45 or lead_y < 30 or lead_y > display_height-45:
            splash.play()
            death = "Your serpent fell into the water and drowned!"
            gameOver=True
        #big lake
        if lead_x >= randLakeX and lead_x <= randLakeX + water_size-15:
            if lead_y >= randLakeY and lead_y <= randLakeY + water_size-15: 
                splash.play()
                death = "Your serpent fell into the water and drowned!"
                gameOver=True
        #small lake
        if lead_x >= randLake2X and lead_x <= randLake2X + water_size2-15:
            if lead_y >= randLake2Y and lead_y <= randLake2Y + water_size2-15:
                splash.play()
                death = "Your serpent fell into the water and drowned!" 
                gameOver=True
                
        #game over sequence
        while gameOver == True:
            #gameDisplay.fill(dark_blue)
            message_to_screen(("  Game over!!!"),red,(display_width/2-200),300)
            message_to_screen2(death,yellow,100,250)
            message_to_screen2((apples_eaten),yellow,150,270)
            message_to_screen(("Press C to play again"),red,(display_width/2-270),400)
            message_to_screen(("  or Q to quit."),red,(display_width/2-200),480)
            pygame.display.update()     
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False  
                    if event.key == pygame.K_c:
                        gameLoop()
        
        #create grass
        def grassFill():
            grassTileX = 0
            grassTileY = 0
            while grassTileX < display_width-60:
                grassTileX += 30
                grassTileY = 0
                while grassTileY < display_height-60:
                    grassTileY += 30
                    if (grassTileX >= randLakeX-15 and grassTileX <= randLakeX + water_size-15) and (grassTileY >= randLakeY-15 and grassTileY <= randLakeY + water_size-15):
                        continue
                    elif (grassTileX >= randLake2X-15 and grassTileX <= randLake2X + water_size2-15) and (grassTileY >= randLake2Y-15 and grassTileY <= randLake2Y + water_size2-15):
                        continue
                    else:
                        gameDisplay.blit(grass,(grassTileX,grassTileY))
        
        grassFill()
                      
        #create a 'x' click quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit=True
            
            #set up movement controls
            if event.type == pygame.KEYDOWN:#<-- "if the player is HOLDING the key down
                #tick.play()
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -15 #<-- the distance your object moves
                    lead_y_change = 0 # <-- resets y axis so diagonal movement is not possible
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = 15 #<--associate this with the size of your object
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -15
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = 15
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
            
        #snake dies if it collides with self
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                splat.play()
                death = "            Your serpent bit its own tail!"
                gameOver = True
                        
        #makes x and y move continuosly.
        lead_x += lead_x_change 
        lead_y += lead_y_change
        
        #create border water
        #gameDisplay.fill(blue) #<--change background color
        
        
        #score counter
        message_2_screen(('Apples eaten: %d'%NumApples),yellow,500,0)
        
        #old solid color grass
        #pygame.draw.rect(gameDisplay,green,[15,15,display_width-30,display_height-30])
        
        #draw and place lakes
        #pygame.draw.rect(gameDisplay,blue,[randLakeX,randLakeY,water_size,water_size])
        #pygame.draw.rect(gameDisplay,blue,[randLake2X,randLake2Y,water_size2,water_size2])
        
        
        #create apple
        #pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,block_size,block_size])
        gameDisplay.blit(appleimage,(randAppleX,randAppleY))
        #the object that is created last is always on top

        gameDisplay.blit(flower,(randFlowerX,randFlowerY))
                
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLength:
            del snakeList[0]
        
        snake(block_size,snakeList)
        
        #draw your snakehead
        #pygame.draw.rect(gameDisplay,dark_green,[lead_x,lead_y,15,15])
        pygame.display.update() #<--applies your changes made
        
        #if snake and apple collision
        #if lead_x == randAppleX and lead_y == randAppleY:
            #if lead_y >= randAppleY and lead_y <= randAppleY + block_size):
        if (lead_x >= randAppleX and lead_x <= randAppleX + block_size) or (lead_x + block_size >= randAppleX and lead_x + block_size <= randAppleX + block_size):
            if (lead_y >= randAppleY and lead_y <= randAppleY + block_size) or (lead_y + block_size >= randAppleY and lead_y + block_size <= randAppleY + block_size):
                bite.play()
                NumApples += 1
                #reset apple placement
                randAppleX = (random.randrange(100,(display_width-100)))    #/15.0)*15.0 #sets position for apples
                randAppleY = (random.randrange(100,(display_height-100)))   #/15.0)*15.0 #the rounding forces the apple to
                #make snake longer
                snakeLength += 1
            
        #prevents apples from spawning on lakes
        if (randAppleX >= randLakeX and randAppleX <= randLakeX + water_size-15):
            if randAppleY >= randLakeY and randAppleY <= randLakeY + water_size-15: 
                randAppleX = round(random.randrange(100,(display_width-100)))  #/15.0)*15.0 #sets position for apples
                randAppleY = round(random.randrange(100,(display_height-100))) #/15.0)*15.0 #the rounding forces the apple to
        if randAppleX >= randLake2X and randAppleX <= randLake2X + water_size2-15:    
           if randAppleY >= randLake2Y and randAppleY <= randLake2Y + water_size2-15: 
                randAppleX = round(random.randrange(100,(display_width-100))) #/15.0)*15.0 
                randAppleY = round(random.randrange(100,(display_height-100))) #/15.0)*15.0 
        
        clock.tick(FPS)#<--sets frames per second
    pygame.quit()
    quit()


def BorderWaterVerticle():
    borderWater=0
    while borderWater < display_height:
        gameDisplay.blit(water1,(0,borderWater))
        gameDisplay.blit(water1,(display_width-30, borderWater))
        borderWater += 30
def BorderWaterHorizontal():     
    borderWater=0
    while borderWater < display_width:
        borderWater += 30
        gameDisplay.blit(water1,(borderWater,0))
        gameDisplay.blit(water1,(borderWater, display_height-30))
def BorderWaterVerticle2():
    borderWater=0
    while borderWater < display_height:
        gameDisplay.blit(water2,(0,borderWater))
        gameDisplay.blit(water2,(display_width-30, borderWater))
        borderWater += 30
def BorderWaterHorizontal2():     
    borderWater=0
    while borderWater < display_width:
        borderWater += 30
        gameDisplay.blit(water2,(borderWater,0))
        gameDisplay.blit(water2,(borderWater, display_height-30))

#create border water and lakes
def largeLake1():
    waterTileX,waterTileY=randLakeX,randLakeY
    global randLakeX,randLakeY,water_size,water_size2
    for all in range(water_size/30):
        for every in range(water_size/30):
            gameDisplay.blit(water1,(waterTileX, waterTileY))
            waterTileX += 30
        waterTileY += 30
        waterTileX = randLakeX

def smallLake1():   
    global randLake2X,randLake2Y
    waterTile2X,waterTile2Y=randLake2X,randLake2Y
    for all in range(water_size2/30):
        for every in range(water_size2/30):
            gameDisplay.blit(water1,(waterTile2X, waterTile2Y))
            waterTile2X += 30
        waterTile2Y += 30
        waterTile2X = randLake2X 

def largeLake2():
    global randLake2X,randLake2Y,water_size,water_size2
    waterTileX,waterTileY=randLakeX,randLakeY   
    for all in range(water_size/30):
        for every in range(water_size/30):
            gameDisplay.blit(water2,(waterTileX, waterTileY))
            waterTileX += 30
        waterTileY += 30
        waterTileX = randLakeX
    
def smallLake2():  
    global randLake2X,randLake2Y
    waterTile2X,waterTile2Y=randLake2X,randLake2Y
    for all in range(water_size2/30):
        for every in range(water_size2/30):
            gameDisplay.blit(water2,(waterTile2X, waterTile2Y))
            waterTile2X += 30
        waterTile2Y += 30
        waterTile2X = randLake2X 
      
def waterAnimation():
    w=0
    while True:
        if w == 0:
            w += 1
            BorderWaterHorizontal()
            BorderWaterVerticle()
            largeLake1()
            smallLake1()
        elif w == 1:
            w -= 1
            BorderWaterHorizontal2()
            BorderWaterVerticle2() 
            largeLake2()
            smallLake2()
        clock.tick(2.0)
        
#opening sequence
def opening():
    global title
    while title == True:
        gameDisplay.fill(dark_blue)
        line1 = "Welcome to Serpentine!"
        message_to_screen(line1,yellow,300,200)
        message_to_screen(("(By Jonathan Carlson)"),green,300,300)
        message_to_screen(("Press ENTER to begin"),yellow,300,400)
        gameDisplay.blit(snakeimg,((display_width/2-50),550,))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    title = False
                    rules()               
                    
def rules():
    rules = True
    while rules == True:
        gameDisplay.fill(dark_green)
        message_to_screen2(("Rules:"),red,150,500)
        message_to_screen2(("Using the arrow keys, send your serpent to eat the red apples."),yellow,250,100)
        message_to_screen2(("Every apple your serpent eats makes it longer."),yellow,300,100)
        message_to_screen2(("Don't accidentally make your serpent bite itself."),yellow,350,100)
        message_to_screen2(("Dont let your serpent go in the blue water."),yellow,400,100)
        message_to_screen2(("See how long you can make your serpent!"),yellow,450,100)
        message_to_screen2("Press 'P' to pause your game.",yellow,550,100)
        message_to_screen2("Press 'ENTER' to start.",yellow,650,100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    rules = False
                    gameLoop()

def startAnimation():
    global aniStart
    if aniStart == 0:
        thread.start_new_thread(waterAnimation,())
        aniStart += 1
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
opening()