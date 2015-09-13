#!/usr/bin/python
# andrewID: kscharm
# author Kenny Scharm
# version 8/3/14
#------------------------


from random import randint
from Tkinter import *
import time
def init():
    canvas.data.emptyColor = "blue"
    rows = canvas.data.rows
    cols = canvas.data.cols
    canvas.data.score = 0 
    canvas.data.isGameOver = False
    canvas.data.board = [[canvas.data.emptyColor for x in xrange(cols)] for x in xrange(rows)]
    #Seven "standard" pieces (tetrominoes)
    iPiece = [
    [True,  True,  True,  True]
    ]
  
    jPiece = [
    [True, False, False],
    [True, True,  True]
    ]
  
    lPiece = [
    [False, False, True],
    [True,  True,  True]
    ]
  
    oPiece = [
    [True, True],
    [True, True]
    ]
  
    sPiece = [
    [False, True, True],
    [True,  True, False]
    ]
  
    tPiece = [
    [False, True, False],
    [True,  True, True]
    ]

    zPiece = [
    [True,  True, False],
    [False, True, True]
    ]
    
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    canvas.data.tetrisPieces = tetrisPieces
    canvas.data.tetrisPieceColors = tetrisPieceColors
    newFallingPiece()
    redrawAll()
def run(rows, cols):
    root = Tk()
    global canvas
    canvas = Canvas(root, width = 600, height = 850)
    canvas.pack()
    root.resizable(width = 0, height = 0)
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    init()
    drawGame()
    root.bind('<KeyPress>', keyPressed)
    timerFired()
    root.mainloop()
    
    
    
def drawGame():
        
    canvas.configure(background = "orange")
    drawBoard()
    drawFallingPiece()
    
def redrawAll():
    canvas.delete(ALL)
    drawGame()
    drawScore()
    if(canvas.data.isGameOver):
        canvas.create_rectangle(0, 0, 600, 850, fill = "orange")
        canvas.create_text(300, 325, font = ("Times New Roman", 80), text = "GAME OVER")
        canvas.create_text(300, 425, font = ("Times New Roman", 50), text = "Score: " + str(canvas.data.score))
        canvas.create_text(300, 525, font = ("Times New Roman", 50), text = "Press R to restart")
        
    
def drawBoard():
    canvas.create_rectangle(45, 45, 555, 805, fill = "black")
       
    for row in xrange(0, len(canvas.data.board)):
        for col in xrange(0, len(canvas.data.board[row])):
            drawCell(row, col, canvas.data.board[row][col])

            
def drawScore():
        t = "Score: " + str(canvas.data.score)
        canvas.create_text(20, 20, anchor = W, font = ("Times New Roman", 20), text = t) 
            
            
def drawCell(row, col, color):
    canvas.create_rectangle(55 + (50 * col), 55 + (50 * row), 95 + (50 * col), 95 + (50 * row), fill = color)
    
def newFallingPiece():
    fallingPiece = canvas.data.tetrisPieces[randint(0, 6)] 
    fallingPieceColor = canvas.data.tetrisPieceColors[randint(0,6)]
    canvas.data.fallingPiece = fallingPiece
    canvas.data.fallingPieceColor = fallingPieceColor
    canvas.data.fallingPieceRow = 0
    fallingPieceRow = 0
    fallingPieceCol = canvas.data.cols/2 - len(canvas.data.fallingPiece[0])/2
    canvas.data.fallingPieceRow = fallingPieceRow
    canvas.data.fallingPieceCol = fallingPieceCol
    if(fallingPieceIsLegal() == False):
            canvas.data.isGameOver = True
    
def drawFallingPiece():
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[row])):
            if(canvas.data.fallingPiece[row][col] == True):
                drawCell(canvas.data.fallingPieceRow + row, 
                canvas.data.fallingPieceCol + col, canvas.data.fallingPieceColor)


def moveFallingPiece(drow, dcol):
    fallingPieceRow = canvas.data.fallingPieceRow
    fallingPieceCol = canvas.data.fallingPieceCol
    canvas.data.fallingPieceRow = canvas.data.fallingPieceRow + drow
    canvas.data.fallingPieceCol = canvas.data.fallingPieceCol + dcol
    if(fallingPieceIsLegal() == False):
        canvas.data.fallingPieceRow = fallingPieceRow
        canvas.data.fallingPieceCol = fallingPieceCol
        return False
    return True 
    
            
def fallingPieceIsLegal():
    board = canvas.data.board
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[0])):
            x = row + canvas.data.fallingPieceRow
            y = col + canvas.data.fallingPieceCol 
            if(canvas.data.fallingPiece[row][col] == True):
                if(x > canvas.data.rows - 1 or y > canvas.data.cols - 1 or 
                y < 0 or x < 0 or
                board[canvas.data.fallingPieceRow + row][canvas.data.fallingPieceCol + col] != canvas.data.emptyColor):
                    return False
    return True  
    
def fallingPieceCenter():
    fallingPiece = canvas.data.fallingPiece
    fallingPieceRow = canvas.data.fallingPieceRow 
    fallingPieceCol = canvas.data.fallingPieceCol
    centerRow = fallingPieceRow + (len(fallingPiece)/2)
    centerCol = fallingPieceCol + (len(fallingPiece[0])/2)
    return (centerRow, centerCol)
    
def rotateFallingPiece():
    board = canvas.data.board
    fallingPiece = canvas.data.fallingPiece
    fallingPieceRow = canvas.data.fallingPieceRow 
    fallingPieceCol = canvas.data.fallingPieceCol
    oldRow = canvas.data.fallingPieceRow
    oldCol = canvas.data.fallingPieceCol
    oldCenterR = fallingPieceCenter()[0]
    oldCenterC = fallingPieceCenter()[1]
    newPiece = []
    
    for row in range(len(canvas.data.fallingPiece[0])):
        temp = []
        for col in range(len(canvas.data.fallingPiece)):
            temp.append("temp")
        newPiece.append(temp)
    for row in reversed(range(len(canvas.data.fallingPiece))):
        for col in range(len(canvas.data.fallingPiece[0])):
            newPiece[col][(len(canvas.data.fallingPiece) -1) - row] = canvas.data.fallingPiece[row][col] 
    canvas.data.fallingPiece = newPiece
    newCenterR = fallingPieceCenter()[0]
    newCenterC = fallingPieceCenter()[1]
    finalRow = fallingPieceRow + oldCenterR - newCenterR
    finalCol = fallingPieceCol + oldCenterC - newCenterC
    canvas.data.fallingPiece = newPiece
    canvas.data.fallingPieceRow = finalRow
    canvas.data.fallingPieceCol = finalCol
    if(fallingPieceIsLegal() == True):
        canvas.data.fallingPieceRow = finalRow
        canvas.data.fallingPieceCol = finalCol
        canvas.data.fallingPiece = newPiece
        drawFallingPiece()
    else:
        canvas.data.fallingPieceRow = oldRow
        canvas.data.fallingPieceCol = oldCol
        canvas.data.fallingPiece = fallingPiece
        
def timerFired():
    redrawAll()
    board =  canvas.data.board
    fallingPiece = canvas.data.fallingPiece
    fallingPieceRow = canvas.data.fallingPieceRow
    fallingPieceCol = canvas.data.fallingPieceCol
    delay = 500
    if(moveFallingPiece(1, 0) == False):
        placeFallingPiece()
        newFallingPiece()    
        removeFullRow()
    canvas.after(delay, timerFired)
    
    
def placeFallingPiece():
    fallingPieceRow = canvas.data.fallingPieceRow
    fallingPieceCol = canvas.data.fallingPieceCol
    fallingPieceColor = canvas.data.fallingPieceColor
    board = canvas.data.board
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[row])):
            if(canvas.data.fallingPiece[row][col] == True):
                board[fallingPieceRow + row][fallingPieceCol + col] = fallingPieceColor        
def rowIsFull(row):
    completedRow = len(canvas.data.board[0])
    count = 0
    for element in xrange(len(canvas.data.board[row])):
        if(canvas.data.board[row][element] != canvas.data.emptyColor):
            count+= 1
            if count == completedRow:
                return True
    return False
def removeFullRow():
    counter = 0
    score = canvas.data.score
    for row in range(len(canvas.data.board)):
        if(rowIsFull(row)):
            canvas.data.board.pop(row)
            canvas.data.board.insert(0, [canvas.data.emptyColor] * canvas.data.cols)
            counter +=  1
    if(counter > 0):
        score = score + (counter * counter)
    canvas.data.score = score
    counter = 0
        
            
def keyPressed(event):
    if(event.keysym == 'Right'):
        moveFallingPiece(0, 1)
    if(event.keysym == 'Left'):
        moveFallingPiece(0, -1)
    if(event.keysym == 'Down'):
        moveFallingPiece(1, 0)
    if(event.keysym == 'Up'):
        rotateFallingPiece()
    if(event.keysym == 'space'):
            while(moveFallingPiece(1,0)):
                continue            
    if(event.char == "r"):
        init()
    redrawAll()

run(15, 10)
