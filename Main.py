import random
from tkinter import *
bomb_symbol = 'b'



def create_board(character, width, height):
  coordinates = []
  for i in range(height):
    row = []
    for j in range(width):
      row.append(character)
    coordinates.append(row)
  return coordinates



#randomly places mines throughout the board

def bury_mines(gameboard,n):
  for i in range(n):
    rcol = random.randint(0,len(gameboard[0])-1)
    rrow = random.randint(0,(len(gameboard)-1))
    gameboard[rrow][rcol] = bomb_symbol
  return gameboard

#gets numebr of mines adjacent to particular square

def get_mine_count(gameboard):
  for y in range(len(gameboard)):
    for x in range(len(gameboard[0])):
      c = 0
      if gameboard[y][x] != bomb_symbol:
        for i in [-1,0, 1]:
          for j in[-1,0,1]:
            if y+i >= 0 and y+i<len(gameboard) and \
               x+j >= 0 and x+j<len(gameboard[0]):
        
                if gameboard[y+i][x+j] == bomb_symbol:
                  if not (i==0 and j==0):
                    c += 1                
        gameboard[y][x] = str(c)

  return gameboard



def run(width,height):

  #create game data    
  gameboard = create_board("0", width, height)
  userboard = create_board("?", width, height)
  bury_mines(gameboard, 9)
 
  get_mine_count(gameboard)

  #create GUI widgets
  master = Tk()
  master.wm_title("Minesweeper")

  cell_height = 45
  cell_width = 45
  heightpxls = cell_height*height
  widthpxls = cell_width*width
 
  
  canvas = Canvas(master, width=widthpxls,height=heightpxls)
  canvas.pack()
  
 #makes the board look pretty

  def display_board(canvas):
    for x in range(len(userboard[0])):
      for y in range(len(userboard)):
        x1 = cell_width * x
        y1 = cell_height * y
        x2 = cell_width * (x+1)
        y2 = cell_height * (y+1)
          
        if userboard[y][x] != "?":
          canvas.create_rectangle(x1,y1,x2,y2, fill = "white")  
          xpxls = (x1+x2)//2
          ypxls = (y1+y2)//2
          canvas.create_text(xpxls, ypxls, text=str(userboard[y][x]), font = "arial 20")
        else:
          canvas.create_rectangle(x1,y1,x2,y2, fill = "green")

  def display_end(canvas):
    for x in range(len(userboard[0])):
      for y in range(len(userboard)):
        x1 = cell_width * x
        y1 = cell_height * y
        x2 = cell_width * (x+1)
        y2 = cell_height * (y+1)

        if gameboard[y][x] == "b":
          canvas.create_rectangle(x1,y1,x2,y2, fill = "yellow")
        elif userboard[y][x] != "?":
          canvas.create_rectangle(x1,y1,x2,y2, fill = "white")  
          xpxls = (x1+x2)//2
          ypxls = (y1+y2)//2
          canvas.create_text(xpxls, ypxls, text=str(userboard[y][x]), font = "arial 20")
        else:
          canvas.create_rectangle(x1,y1,x2,y2, fill = "green")

  display_board(canvas)  
  def uncover_board(gameboard, user, column, row):
    y = int(row) 
    x = int(column) 

    #if space has already been uncovered by the user

    if gameboard[y][x] != bomb_symbol:

      if user[y][x].isnumeric():
        return

      #if space has a mine count value

      if gameboard[y][x].isnumeric():
        user[y][x] = gameboard[y][x]
        if int(user[y][x]) > 0:
          return

      #recursively uncovers spaces where mine count is 0

      for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
          if x+j >= 0 and x+j<len(gameboard[0]) \
            and y+i >= 0 and y+i < len(gameboard):
            # can throw an index error
              if not (i==0 and j==0):
                uncover_board(gameboard, user, x + j, y + i)
      
  #checks to see if the game has been won

  def check_won(gameboard, userboard):
    b = 0
    c = 0
    for i in range(len(gameboard)):
      for j in range(len(gameboard[0])):
        if gameboard[i][j] == bomb_symbol:
          b += 1
        if userboard[i][j] == "?":
          c+=1
    if c == b:
      win = True
      print("You won!")
      canvas.create_text(180,180, text = "YOU WON!", fill="blue", justify="center", font = "arial 30")
      canvas.unbind("<Button-1>")
    else:
      win = False
      
    return win
  
  #event handler for when canvas is clicked
  
  def handle_click(event):
    x1 = event.x
    y1 = event.y
    x = x1 // cell_width
    y = y1 // cell_height
  
    uncover_board(gameboard,userboard, x,y) 
    display_board(canvas)
    if gameboard[y][x] == "b":
      display_end(canvas)
      canvas.create_text(180,180, text="YOU LOSE!", fill="red", font="arial 30", justify = "center")
      canvas.unbind("<Button-1>")
     
    else: 
      check_won(gameboard, userboard)

  canvas.bind("<Button-1>", handle_click)
  master.mainloop()

run(8,8)
