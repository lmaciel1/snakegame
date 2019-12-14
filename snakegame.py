import math 
import random 
import pygame
import tkinter as tk
from tkinter import messagebox


print("Welcome to the Main Menu. What difficulty would you like to play on?")

difficulty = input("Easy, Medium, or Hard?: ")

if difficulty == "Easy":

    class cube(object):
        rows = 25
        w = 500
        def __init__(self,start, dirnx=1, dirny=0, color=(255,0,0)):
            self.pos = start
            self.dirnx = 1 
            self.dirny = 0 
            self.color = color 

        def move(self, dirnx, dirny):
            self.dirnx = dirnx
            self.dirny = dirny 
            self.pos = (self.pos[0]+self.dirnx, self.pos[1] + self.dirny) 


        def draw(self,surface,eyes=False):
            dis = self.w//self.rows 
            i = self.pos[0]
            j = self.pos[1]

            pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))
            #keeps white lines of the grid outside of the food cube 
            if eyes:
                centre= dis//2
                radius = 3
                circleMiddle = (i*dis+centre-radius,j*dis+8)
                circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
                pygame.draw.circle(surface,(0,0,0), circleMiddle, radius)
                pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)



    class snake(object):
        body = []
        turns = {}

        def __init__(self, color,pos):
            self.color = color
            self.head = cube(pos)
            #the head is always equal to a cube at a given position
            self.body.append(self.head)
            self.dirnx = 0
            #keeps track of what direction the snake is moving 
            self.dirny = 1

        def move(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pygame.key.get_pressed()  
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        self.dirnx = -1
                        self.dirny = 0 
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pygame.K_RIGHT]:
                        self.dirnx = 1
                        self.dirny = 0 
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        
                    elif keys[pygame.K_DOWN]:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys [pygame.K_UP]:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            # the different conditionals allow for the body to move with the head
            # utilizes a dictionary to do so 
            #has to be elif so they cant click multiple keys at once 
    
            for i,c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns: 
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                    else: c.move(c.dirnx, c.dirny)


            #for each cube in the body, we are checking for 

        def reset(self,pos):
            self.head = cube(pos)
            self.body = []
            self.body.append(self.head)
            self.turns = {}
            self.dirnx = 0
            self.dirny = 1


        def addCube(self):
            tail = self.body[-1]
            dx, dy = tail.dirnx, tail.dirny 

            if dx == 1 and dy == 0:
                self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
            elif dx == -1 and dy == 0:
                self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
            elif dx == 0 and dy == 1:
                self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
            elif dx == 0 and dy == -1:
                self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

                #this function properly adds cubes to the tail of the snake
                #gives it based on the direction that the snake is moving 
            self.body[-1].dirnx = dx
            self.body[-1].dirny = dy 

        def draw(self,surface):
            for i,c in enumerate(self.body):
                if i == 0:
                    c.draw(surface,True)
                else:
                    c.draw(surface)

    def drawGrid (w,rows,surface):
        sizeBtwn = w//rows 

        x= 0 
        y= 0 
        for l in range(rows):
            x = x + sizeBtwn
            y =  y + sizeBtwn

            pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) 
            pygame.draw.line(surface, (255,255,255), (0,y), (w,y)) 

                #draws two lines for us for every loop in the for loop
                #start and ends position 

    def redrawWindow(surface):
        global rows, width, s, snack
        surface.fill((0,0,0)) 
        s.draw(surface)
        snack.draw(surface)
        drawGrid(width, rows, surface)
        pygame.display.update()
        #draws the window for the game 

    def randomSnack(rows,item):
        positions = item.body 

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
                continue 
            else: 
                break 

        return (x,y)

            #this keeps the snack from spawning on the snake 

    #def message_box(subject, content):
        #root = tk.Tk()    
        #root.attributes("-topmost", True)
    # root.withdraw()
    # messagebox.showinfo(subject,content)
        

    def main():
        global width,rows, s, snack
        width = 500
        rows = 25
        #can play with this to make it harder by creating less space 
        win = pygame.display.set_mode((width, width))
        s = snake((255,0,0),(10,10))                                
        #gives the snake its starting color and position 
        snack = cube(randomSnack(rows,s), color =(0,255,0))
        flag = True

        clock = pygame.time.Clock()

        while flag:
            pygame.time.delay(50)
            clock.tick(10)
            #delay the game by 50 milliseconds and clock.tick has it run at 10 frames per second 
            s.move()
            if s.body[0].pos == snack.pos:
                s.addCube()
                snack = cube(randomSnack(rows,s), color =(0,255,0))
                #this conditional is what checks if the head of the snake has touched the snack 
            
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                    print('Score: ', len(s.body))
                    #message_box('You Lost!', 'Play again...')
                    s.reset((10,10))
                    break
            
            redrawWindow(win)   


        #inversely proportional 
        #this while loop is what the game runs on

        pass  



    main()
if difficulty == "Medium":

    class cube(object):
        rows = 15
        w = 500
        def __init__(self,start, dirnx=1, dirny=0, color=(255,0,0)):
            self.pos = start
            self.dirnx = 1 
            self.dirny = 0 
            self.color = color 

        def move(self, dirnx, dirny):
            self.dirnx = dirnx
            self.dirny = dirny 
            self.pos = (self.pos[0]+self.dirnx, self.pos[1] + self.dirny) 


        def draw(self,surface,eyes=False):
            dis = self.w//self.rows 
            i = self.pos[0]
            j = self.pos[1]

            pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))
            #keeps white lines of the grid outside of the food cube 
            if eyes:
                centre= dis//2
                radius = 3
                circleMiddle = (i*dis+centre-radius,j*dis+8)
                circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
                pygame.draw.circle(surface,(0,0,0), circleMiddle, radius)
                pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)



    class snake(object):
        body = []
        turns = {}

        def __init__(self, color,pos):
            self.color = color
            self.head = cube(pos)
            #the head is always equal to a cube at a given position
            self.body.append(self.head)
            self.dirnx = 0
            #keeps track of what direction the snake is moving 
            self.dirny = 1

        def move(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pygame.key.get_pressed()  
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        self.dirnx = -1
                        self.dirny = 0 
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pygame.K_RIGHT]:
                        self.dirnx = 1
                        self.dirny = 0 
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        
                    elif keys[pygame.K_DOWN]:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys [pygame.K_UP]:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            # the different conditionals allow for the body to move with the head
            # utilizes a dictionary to do so 
            #has to be elif so they cant click multiple keys at once 
    
            for i,c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns: 
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                    else: c.move(c.dirnx, c.dirny)


            #for each cube in the body, we are checking for 

        def reset(self,pos):
            self.head = cube(pos)
            self.body = []
            self.body.append(self.head)
            self.turns = {}
            self.dirnx = 0
            self.dirny = 1


        def addCube(self):
            tail = self.body[-1]
            dx, dy = tail.dirnx, tail.dirny 

            if dx == 1 and dy == 0:
                self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
            elif dx == -1 and dy == 0:
                self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
            elif dx == 0 and dy == 1:
                self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
            elif dx == 0 and dy == -1:
                self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

                #this function properly adds cubes to the tail of the snake
                #gives it based on the direction that the snake is moving 
            self.body[-1].dirnx = dx
            self.body[-1].dirny = dy 

        def draw(self,surface):
            for i,c in enumerate(self.body):
                if i == 0:
                    c.draw(surface,True)
                else:
                    c.draw(surface)

    def drawGrid (w,rows,surface):
        sizeBtwn = w//rows 

        x= 0 
        y= 0 
        for l in range(rows):
            x = x + sizeBtwn
            y =  y + sizeBtwn

            pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) 
            pygame.draw.line(surface, (255,255,255), (0,y), (w,y)) 

                #draws two lines for us for every loop in the for loop
                #start and ends position 

    def redrawWindow(surface):
        global rows, width, s, snack
        surface.fill((0,0,0)) 
        s.draw(surface)
        snack.draw(surface)
        drawGrid(width, rows, surface)
        pygame.display.update()
        #draws the window for the game 

    def randomSnack(rows,item):
        positions = item.body 

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
                continue 
            else: 
                break 

        return (x,y)

            #this keeps the snack from spawning on the snake 

    #def message_box(subject, content):
        #root = tk.Tk()    
        #root.attributes("-topmost", True)
    # root.withdraw()
    # messagebox.showinfo(subject,content)
        

    def main():
        global width,rows, s, snack
        width = 500
        rows = 15
        #can play with this to make it harder by creating less space 
        win = pygame.display.set_mode((width, width))
        s = snake((255,0,0),(10,10))                                
        #gives the snake its starting color and position 
        snack = cube(randomSnack(rows,s), color =(0,255,0))
        flag = True

        clock = pygame.time.Clock()

        while flag:
            pygame.time.delay(50)
            clock.tick(10)
            #delay the game by 50 milliseconds and clock.tick has it run at 10 frames per second 
            s.move()
            if s.body[0].pos == snack.pos:
                s.addCube()
                snack = cube(randomSnack(rows,s), color =(0,255,0))
                #this conditional is what checks if the head of the snake has touched the snack 
            
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                    print('Score: ', len(s.body))
                    #message_box('You Lost!', 'Play again...')
                    s.reset((10,10))
                    break
            
            redrawWindow(win)   


        #inversely proportional 
        #this while loop is what the game runs on

        pass  



    main()
if difficulty ==  "Hard":
    class cube(object):
        rows = 10
        w = 500
        def __init__(self,start, dirnx=1, dirny=0, color=(255,0,0)):
            self.pos = start
            self.dirnx = 1 
            self.dirny = 0 
            self.color = color 

        def move(self, dirnx, dirny):
            self.dirnx = dirnx
            self.dirny = dirny 
            self.pos = (self.pos[0]+self.dirnx, self.pos[1] + self.dirny) 


        def draw(self,surface,eyes=False):
            dis = self.w//self.rows 
            i = self.pos[0]
            j = self.pos[1]

            pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))
            #keeps white lines of the grid outside of the food cube 
            if eyes:
                centre= dis//2
                radius = 3
                circleMiddle = (i*dis+centre-radius,j*dis+8)
                circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
                pygame.draw.circle(surface,(0,0,0), circleMiddle, radius)
                pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)



    class snake(object):
        body = []
        turns = {}

        def __init__(self, color,pos):
            self.color = color
            self.head = cube(pos)
            #the head is always equal to a cube at a given position
            self.body.append(self.head)
            self.dirnx = 0
            #keeps track of what direction the snake is moving 
            self.dirny = 1

        def move(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pygame.key.get_pressed()  
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        self.dirnx = -1
                        self.dirny = 0 
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pygame.K_RIGHT]:
                        self.dirnx = 1
                        self.dirny = 0 
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        
                    elif keys[pygame.K_DOWN]:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys [pygame.K_UP]:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            # the different conditionals allow for the body to move with the head
            # utilizes a dictionary to do so 
            #has to be elif so they cant click multiple keys at once 
    
            for i,c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns: 
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                    else: c.move(c.dirnx, c.dirny)


            #for each cube in the body, we are checking for 

        def reset(self,pos):
            self.head = cube(pos)
            self.body = []
            self.body.append(self.head)
            self.turns = {}
            self.dirnx = 0
            self.dirny = 1


        def addCube(self):
            tail = self.body[-1]
            dx, dy = tail.dirnx, tail.dirny 

            if dx == 1 and dy == 0:
                self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
            elif dx == -1 and dy == 0:
                self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
            elif dx == 0 and dy == 1:
                self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
            elif dx == 0 and dy == -1:
                self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

                #this function properly adds cubes to the tail of the snake
                #gives it based on the direction that the snake is moving 
            self.body[-1].dirnx = dx
            self.body[-1].dirny = dy 

        def draw(self,surface):
            for i,c in enumerate(self.body):
                if i == 0:
                    c.draw(surface,True)
                else:
                    c.draw(surface)

    def drawGrid (w,rows,surface):
        sizeBtwn = w//rows 

        x= 0 
        y= 0 
        for l in range(rows):
            x = x + sizeBtwn
            y =  y + sizeBtwn

            pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) 
            pygame.draw.line(surface, (255,255,255), (0,y), (w,y)) 

                #draws two lines for us for every loop in the for loop
                #start and ends position 

    def redrawWindow(surface):
        global rows, width, s, snack
        surface.fill((0,0,0)) 
        s.draw(surface)
        snack.draw(surface)
        drawGrid(width, rows, surface)
        pygame.display.update()
        #draws the window for the game 

    def randomSnack(rows,item):
        positions = item.body 

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
                continue 
            else: 
                break 

        return (x,y)

            #this keeps the snack from spawning on the snake 

    #def message_box(subject, content):
        #root = tk.Tk()    
        #root.attributes("-topmost", True)
    # root.withdraw()
    # messagebox.showinfo(subject,content)
        

    def main():
        global width,rows, s, snack
        width = 500
        rows = 10
        #can play with this to make it harder by creating less space 
        win = pygame.display.set_mode((width, width))
        s = snake((255,0,0),(10,10))                                
        #gives the snake its starting color and position 
        snack = cube(randomSnack(rows,s), color =(0,255,0))
        flag = True

        clock = pygame.time.Clock()

        while flag:
            pygame.time.delay(50)
            clock.tick(10)
            #delay the game by 50 milliseconds and clock.tick has it run at 10 frames per second 
            s.move()
            if s.body[0].pos == snack.pos:
                s.addCube()
                snack = cube(randomSnack(rows,s), color =(0,255,0))
                #this conditional is what checks if the head of the snake has touched the snack 
            
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                    print('Score: ', len(s.body))
                    #message_box('You Lost!', 'Play again...')
                    s.reset((10,10))
                    break
            
            redrawWindow(win)   


        #inversely proportional 
        #this while loop is what the game runs on

        pass  



    main()