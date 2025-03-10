import pygame as pg
import time
import random as rand
import numpy as np

#initialize pygame
pg.init()

#define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
orange = (255,165,0)
blue = (0,0,255)

#define boundaries
width =  200
height = 400

game_speed = 5

rot_num = 0


#define display
game_display = pg.display.set_mode((width,height))

#set title of window
pg.display.set_caption("test game")

#define clock for game speed
clock = pg.time.Clock()

piece_size = 20

saved_pieces_x = []
saved_pieces_y = []

piece_x = []
piece_y = []

line_clear = 0

piece_num = 0


def run_game():
    game_over=False

    rot_num = 0

    piece_x = [0]
    piece_y = [0]


    #set falling piece_x and block_y
    piece_x,piece_y,piece_num,rot_num = add_piece(rot_num)
    
    game_over = False
    
    line_clear = 0

    y_speed = piece_size
    x_speed = 0
    saved_pieces_x = []
    saved_pieces_y = []
    while game_over == False:
        #print(height) 
        #fill background
        game_display.fill(black)
        
        #draw the piece
        for i in range(len(piece_x)):
            pg.draw.rect(game_display,orange,[piece_x[i],piece_y[i],piece_size,piece_size])
        for i in range(len(saved_pieces_x)):
            pg.draw.rect(game_display,blue,[saved_pieces_x[i],saved_pieces_y[i],piece_size,piece_size])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x_speed = -piece_size
                    #y_speed = 0
                if event.key == pg.K_RIGHT:
                    x_speed = piece_size
                    #y_speed = 0
                if event.key == pg.K_UP:
                    rot_num,piece_x,piece_y = spin_piece(piece_x, piece_y, piece_num, rot_num,y_speed,saved_pieces_x,saved_pieces_y) 
                #if event.key == pg.K_DOWN:
                    #x_speed = 0
                    #y_speed = piece_size

        #spin the piece
        #spin_centers_x = [-500,20,]
        #spin_centers_y = [-500,-40,]
        

                #if piece_x[x] == saved_pieces_x[u]-x_speed and piece_y[x] == saved_pieces_y[u]-y_speed:
        for x in range(len(piece_x)):
            for u in range(len(saved_pieces_x)):
                if piece_x[x] == saved_pieces_x[u]-x_speed and piece_y[x] == saved_pieces_y[u]-y_speed:
                    x_speed = 0

        piece_hit = False
        #check for collisions
        for x in range(len(piece_x)):
            for u in range(len(saved_pieces_x)):
                
                if piece_x[x] == saved_pieces_x[u] and piece_y[x] == saved_pieces_y[u]-y_speed:
                    #for i in range(len(piece_x)):
                    #    piece_x[i] -= x_speed 
                    #    piece_y[i] -= y_speed
                    for i in range(len(piece_x)):
                        saved_pieces_x.append(piece_x[i])
                        saved_pieces_y.append(piece_y[i])
                    piece_x,piece_y,piece_num,rot_num = add_piece(rot_num)
                    piece_hit = True
                    
        if piece_hit == True:
            saved_pieces_x, saved_pieces_y,line_clear = check_tetris(saved_pieces_x, saved_pieces_y,line_clear)
        
        #check for floor
        #print(piece_y)
        for y in range(len(piece_y)):     
            if piece_y[y] >= height-piece_size:
                x_speed=0
                for i in range(len(piece_x)):
                    saved_pieces_x.append(piece_x[i])
                    saved_pieces_y.append(piece_y[i])
                piece_x, piece_y, piece_num,rot_num= add_piece(rot_num)
                saved_pieces_x, saved_pieces_y,line_clear = check_tetris(saved_pieces_x,saved_pieces_y,line_clear)
            if piece_x[y]+x_speed < 0 or piece_x[y]+x_speed+piece_size > width:
                x_speed=0


        
        #change speed
        for i in range(len(piece_x)):
            #print(x_speed)
            #print(piece_x[i])
            piece_x[i] += x_speed
            piece_y[i] += y_speed
            
        x_speed = 0
    
        pg.display.update()
        clock.tick(game_speed)
    pg.quit()
    quit()

def add_piece(rot_num):
    #indexes: 0-cube;1-line;2-z;3-s;4-L;5-J;6-T
    piece_list_x = [[100,100,120,120], [100]*4, [100,120,120,140], [100,120,120,140], [100,100,100,120], [100,120,120,120], [100,120,120,140]]
    piece_list_y = [[100,120,100,120], [100,120,140,160], [100,100,120,120], [120,120,100,100], [100,80,60,100], [100,100,80,60], [80,80,100,80]]
    
    random_num = rand.randint(0,6)
    
    #random_num = 6

    piece_x = piece_list_x[random_num]
    piece_y = piece_list_y[random_num]
    
    
    rot_num = 0

    return piece_x, piece_y, random_num, rot_num




def check_tetris(saved_pieces_x,saved_pieces_y,line_clear):
    for i in range(int(height/20)):
        #print(height)
        #print(i)
        j = i*20
        #print("yes, this ran")
        #print(saved_pieces_y)
        num_on_row = 0
        for d in range(len(saved_pieces_x)):
            if saved_pieces_y[d] == j:
                num_on_row += 1
        #print(num_on_row)
        if num_on_row == int(width/20):
            line_clear += 1

            for k in range(len(saved_pieces_y) - 1, -1, -1):
                #print(k)
                if j == saved_pieces_y[k]:
                    saved_pieces_y.pop(k)
                    saved_pieces_x.pop(k)
            for k in range(len(saved_pieces_y)):
                if saved_pieces_y[k] < j:
                    saved_pieces_y[k] += 20

            print(line_clear)
    return(saved_pieces_x, saved_pieces_y,line_clear)





def spin_piece(piece_x,piece_y,piece_num,rot_num,y_speed,saved_pieces_x,saved_pieces_y):
    piece_lowest_x = 900000
    piece_lowest_y = 900000
    
    original_piece_x = piece_x[:]
    original_piece_y = piece_y[:]


    piece_grid = []
    
    #find lowest of eact piece
    piece_lowest_x = min(piece_x)
    piece_lowest_y = max(piece_y)
    
    #set up grid
    for i in range(4):
        piece_grid.append([])
        for j in range(4):
            piece_grid[i].append(0)

    #scale to correct coordinate set
    for i in range(len(piece_x)):
        piece_x[i] = int((piece_x[i] - piece_lowest_x)/20)
        piece_y[i] = int((-piece_y[i] + piece_lowest_y)/20)
    
    #add the pieces to the grid
    for i in range(len(piece_x)):
        piece_grid[piece_x[i]][piece_y[i]] = 1
    
    #reverse grid
    for i in range(len(piece_grid)):
        piece_grid[i] = piece_grid[i][::-1]


    #transpose grid
    new_piece_grid = []
    for i in range(len(piece_grid)):
        new_piece_grid.append([])
        for j in range(len(piece_grid[i])):
            new_piece_grid[i].append(piece_grid[j][i])
    piece_grid = new_piece_grid

#    corner = 0
#    line = 0
#    for i in range(len(piece_grid)):
#        for j in range(len(piece_grid[i])):
#            above = 0
#            below = 0
#            left = 0
#            right = 0
#            bl=0
#            tl=0
#            br=0
#            tr=0
#            if piece_grid[i][j] == 1:
#                if i+1 < len(piece_grid):
#                    if piece_grid[i+1][j] == 1:
#                        above += 1
#                if i-1 < len(piece_grid):
#                    if piece_grid[i-1][j] == 1:
#                        below += 1
#                if j+1 < len(piece_grid[i]):
#                    if piece_grid[i][j+1] == 1:
#                        right += 1
#                if j-1 < len(piece_grid[i]):
#                    if piece_grid[i][j-1] == 1:
#                        left += 1
#                if i-1 < len(piece_grid) and j-1 < len(piece_grid):
#                    if piece_grid[i-1][j-1] == 1:
#                        tl += 1
#                if i-1 < len(piece_grid) and j+1 < len(piece_grid):
#                    if piece_grid[i-1][j+1] == 1:
#                        tr += 1
#                if i+1 < len(piece_grid) and j-1 < len(piece_grid):
#                    if piece_grid[i+1][j-1] == 1:
#                        bl += 1
#                if i+1 < len(piece_grid) and j+1 < len(piece_grid):
#                    if piece_grid[i+1][j+1] == 1:
#                        br += 1
#                print(f'up: {above} below:{below} right{right} left{left} tl{tl} bl{bl} br{br} tr{tr}')
#                if (above >= 1 or below >= 1) and (left >=1 or right >= 1):
#                    corner += 1
#                    print("corner")
#                if below ==1 and above == 1 or left ==1 and right == 1:
#                    line += 1
#                    print("line")


    print(f"rot num {rot_num}")
    if piece_num == 0:
        middle_rot = 1
        x_diff = 1
        y_diff = 1
    elif piece_num == 1: 
        middle_rot = 1
        if rot_num == 0 or rot_num == 2:
            x_diff = 2
            y_diff = 0
            #print("yes")
            piece_lowest_x -=20
        if rot_num==1 or rot_num == 3:
            x_diff = 0
            y_diff = 2
            piece_lowest_x -=0
            piece_lowest_y += 20
    elif piece_num == 2:
        #print("yes")
        if rot_num == 0 or rot_num == 2:
            x_diff = 0
            y_diff = 1
            piece_lowest_y += 20
        elif rot_num == 1 or rot_num == 3:
            x_diff = 0
            y_diff = 0
            piece_lowest_x -=40
    elif piece_num == 3:
        if rot_num == 0 or rot_num == 2:
            x_diff = 0
            y_diff = 0
            piece_lowest_x -=20
        elif rot_num == 1 or rot_num == 3:
            x_diff = 0
            y_diff = 1
            #piece_lowest_y += 20
            piece_lowest_x -=20
    elif piece_num == 4:
        if rot_num == 0 or rot_num == 2:
            x_diff = 2
            y_diff = 0
            piece_lowest_x -= 40
        elif rot_num ==1 or rot_num == 3:
            #print("yes")
            x_diff = 0
            y_diff = 1
            piece_lowest_y += 20

    elif piece_num == 5:
        if rot_num == 0 or rot_num == 2:
            x_diff = 2
            y_diff = 0
            piece_lowest_x -= 40
        elif rot_num ==1 or rot_num == 3:
            x_diff = 0
            y_diff = 1
            piece_lowest_y += 20
    
    elif piece_num == 6:
        if rot_num == 0:
            x_diff = 0
            y_diff = 0
            piece_lowest_x -= 20
        elif rot_num ==1:
            x_diff = 1
            y_diff = 0
            piece_lowest_x -= 40
            piece_lowest_y += 0
        elif rot_num == 2:
            x_diff = 0
            y_diff = 1
            piece_lowest_x -= 20
        elif rot_num == 3:
            x_diff = 0
            y_diff = 0
            piece_lowest_x -= 20
            piece_lowest_y += 0


    #else:
    #    
    #    y_diff = 0
    #    x_diff = 0
        

    new_piece_grid = []
    for i in range(4):
        new_piece_grid.append([])
        for j in range(4):
            new_piece_grid[i].append(0)

    for i in range(len(piece_grid)):
        for j in range(len(piece_grid[i])):
            if piece_grid[i][j] == 1:
                piece_grid[i][j]=0
                print(i)
                print(j)
                new_piece_grid[i-y_diff][j+x_diff] = 1
    piece_grid = new_piece_grid

    #transpose grid
    new_piece_grid = []
    for i in range(len(piece_grid)):
        new_piece_grid.append([])
        for j in range(len(piece_grid[i])):
            new_piece_grid[i].append(piece_grid[j][i])
    piece_grid = new_piece_grid

    #reverse grid
    #for i in range(len(piece_grid)):
    #    piece_grid[i] = piece_grid[i][::-1]
    
    #print(piece_grid)
    list_num = 0
    for i in range(len(piece_grid)):
        for j in range(len(piece_grid[i])):
            if piece_grid[i][j] == 1:
                piece_x[list_num] = j
                piece_y[list_num] = i
                list_num += 1
    temp_piece_x = piece_x[:]
    temp_piece_y = piece_y[:]
    #print(piece_x)
    for i in range(len(piece_x)):
        temp_piece_x[i] = int(piece_x[i]*20+piece_lowest_x)
        temp_piece_y[i] = int(-piece_y[i]*20+piece_lowest_y)
    
    #print(temp_piece_x)
    #check for collisions

    piece_x = temp_piece_x[:]
    piece_y = temp_piece_y[:]

    
    #print(saved_pieces_x)
    print(original_piece_x)
    for x in range(len(piece_x)):
        for u in range(len(saved_pieces_x)):
            if piece_x[x] == saved_pieces_x[u] and piece_y[x] == saved_pieces_y[u]-y_speed:
                piece_x = original_piece_x[:]
                piece_y = original_piece_y[:]
                print("tdctdct")
            #elif piece_x != temp_piece_x:
                #piece_x = temp_piece_x[:]
                #piece_y = temp_piece_y[:]


    if rot_num < 3:
        rot_num += 1
    else:
        rot_num = 0
    print(piece_x, piece_y, original_piece_x, original_piece_y)
    return(rot_num,piece_x,piece_y)
    print(piece_x)
run_game()
