
# this is my first time to i am using a python code
# i try to practice python with common sample
# pushman - boxman
# 09/04/2022 
# use and develop this code is free but please write my name
# mr.rajjaei@gmail.com (Masoud Rajaei) on youtube.com or linkedin.com 

from enum import Enum
import string
from tkinter import *
from tkinter import messagebox

class KeyCodes(Enum):
      UP=38
      DOWN=40
      LEFT=37 
      RIGHT=39
      ENTER=13
      
class Tile(Enum):
     FREE = 0
     BLOCK = 1
     WALL = 2
     BOX = 3
     PLACES = 4
     MAN = 5
     PUSHABLEBOX = 6


rows, cols = (28, 28)

ManPosition=[0,0]

Space = [['0' for i in range(0,100)] for j in range(0,100)]
images = [[None for i in range(0, 100)] for j in range(0, 100)]
pushableBoxLOC=[]
PlacesLOC=[]

filenames = [   r'Free.png',
                r'Block.png',
                r'Wall.png',
                r'Box.png',
                r'Places.png',
                r'Man.png',
                r'PushableBox.png',
                r'PushableBox.png',
          ]

# print(filenames)
root = Tk()
root.title('Boxman Masoud Rajaei')
root.geometry('500x500')
root.iconbitmap(default='icon.ico')

tileWidth = PhotoImage(file=filenames[0]).width()
tileHeight = PhotoImage(file=filenames[0]).height()
################################################################ Main function or procedure
def LoadMap(Level:int): 
        newLevel = False
        rowIndex = 0
        totalColsCount=0
        with open('Map.txt') as f:
            for x in f.readlines():
                #print(x)
                if x.__contains__("L"): 
                    newLevel=False

                if (x.__contains__("M") & newLevel):
                    idx=x.replace(' ',"").index('M')
                    print("ManLoc=",idx,rowIndex)
                    ManPosition[0]=idx
                    ManPosition[1]=rowIndex
                    #x.replace("M","0")
                    
                if (x.__contains__("L0")):
                    #print("Level found")
                    newLevel = True
                    rowIndex=0
                    continue
                if x.__contains__('P') & newLevel: # pushable box gathering 
                    test=[]
                    test.append([i for i,xc in enumerate(x.replace(' ', "")) if xc == 'P'])
                    for loc in test: pushableBoxLOC.append([loc[0],rowIndex])     
                 
                if x.__contains__('H') & newLevel: # holes for box gathering 
                    test=[]
                    test.append([i for i,xc in enumerate(x.replace(' ', "")) if xc == 'H'])
                    for loc in test: PlacesLOC.append([loc[0],rowIndex])  
                                              
                if newLevel:
                    Space[rowIndex] = [c for c in x.replace("M", "0").replace("P", "0").split(" ")]
                    #print(Space[0].__len__())
                    #print(Space[rowIndex])
                    if totalColsCount<Space[0].__len__(): 
                       totalColsCount=Space[0].__len__()
                       

                    rowIndex=rowIndex+1
                    
            f.close()
            rows=rowIndex
            cols=totalColsCount
            
            print("Map =>",rows,cols)

def initMap():

    Space[0]=['W']*100 

    for x in range(0, Space.__len__()):
        for y in range(0, Space[x].__len__()): 
             if x == 0:
                Space[x][y]='W'

             if x == (cols-1):
                Space[x][y] = 'W'

             if y == (rows-1):
                Space[x][y] = 'W'

             if y == 0:
                Space[x][y] = 'W'

    return

def Getnumber(para: string):
    result:int
    result = Tile.FREE.value
    match para:
        case 'M':
            result = Tile.MAN.value
        case 'F':
            result = Tile.FREE.value
        case 'B':
            result = Tile.BOX.value
        case 'W':
            result = Tile.WALL.value
        case 'H':
            result = Tile.PLACES.value
        case 'P':
            result = Tile.PUSHABLEBOX.value 
        case _:       
            result = Tile.FREE.value
    return result  

def PushableBoxRender():
        for p in pushableBoxLOC:
              r=p[1]
              c=p[0]
              y=r*tileWidth
              x=c*tileHeight
              images[r][c]=PhotoImage(file=filenames[Getnumber('P')])#(x=x,y=y)
              Label(root,image=images[r][c],padx=0,pady=0,borderwidth=0).place(x=x,y=y)
        return 

def SpaceRender():
    x=0
    y=0
    for c in range(0, cols):
        y=0
        for r in range(0, rows):       
            if r>=Space.__len__():
               continue
            if c>=Space[r].__len__():
               continue
           
            if  [c,r] not in pushableBoxLOC:
                images[r][c]=PhotoImage(file=filenames[Getnumber(Space[r][c])])#(x=x,y=y)
            else  :
                images[r][c]=PhotoImage(file=filenames[Getnumber('P')])#(x=x,y=y)
            
            Label(root,image=images[r][c],padx=0,pady=0,borderwidth=0).place(x=x,y=y)

            y=y+tileHeight            
        x=x+tileWidth
      
    print ("End Space Render")  
    return

def Fitness():
    result=True
    for i in pushableBoxLOC:
        if i not in PlacesLOC: result=False
    return result

def CanMoveMan(keycode):
    print("P",Space[ManPosition[1]-1][ManPosition[0]])
    match keycode:
        case KeyCodes.UP.value :#|  KeyCodes.ENTER.value:
          if Getnumber(Space[ManPosition[1]-1][ManPosition[0]]) in [Tile.FREE.value,Tile.PUSHABLEBOX.value,Tile.PLACES.value]:
             return True  
        case KeyCodes.DOWN.value :#|  KeyCodes.ENTER.value:
          if Getnumber(Space[ManPosition[1]+1][ManPosition[0]]) in [Tile.FREE.value,Tile.PUSHABLEBOX.value,Tile.PLACES.value]:
             return True     
        case KeyCodes.RIGHT.value :#|  KeyCodes.ENTER.value:
          if Getnumber(Space[ManPosition[1]][ManPosition[0]+1]) in [Tile.FREE.value,Tile.PUSHABLEBOX.value,Tile.PLACES.value]:
             return True    
        case KeyCodes.LEFT.value :#|  KeyCodes.ENTER.value:
          if Getnumber(Space[ManPosition[1]][ManPosition[0]-1]) in [Tile.FREE.value,Tile.PUSHABLEBOX.value,Tile.PLACES.value]:
             return True   
    return False
    
def handle_keypress(event):
    #print(event.keycode)
    isMoveValidation=CanMoveMan(event.keycode)
    print("Can Move:",isMoveValidation)
    lastScreenValue=Getnumber(Space[ManPosition[1]][ManPosition[0]])
    match event.keycode:
        case KeyCodes.UP.value:
            if isMoveValidation:
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[lastScreenValue])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)  
               ManPosition[1]=ManPosition[1]-1
               if [ManPosition[0],ManPosition[1]] in pushableBoxLOC:
                   pp=pushableBoxLOC.index([ManPosition[0],ManPosition[1]])
                   pushableBoxLOC[pp][1]=pushableBoxLOC[pp][1]-1                   
                   
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[Getnumber('M')])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)

            
        case KeyCodes.DOWN.value:
            if isMoveValidation:
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[lastScreenValue])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)
               ManPosition[1]=ManPosition[1]+1
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[Getnumber('M')])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)
               if [ManPosition[0],ManPosition[1]] in pushableBoxLOC:
                   pp=pushableBoxLOC.index([ManPosition[0],ManPosition[1]])
                   pushableBoxLOC[pp][1]=pushableBoxLOC[pp][1]+1                   
            
        case KeyCodes.LEFT.value:
            if isMoveValidation:
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[lastScreenValue])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)
               ManPosition[0]=ManPosition[0]-1
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[Getnumber('M')])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)
               if [ManPosition[0],ManPosition[1]] in pushableBoxLOC:
                   pp=pushableBoxLOC.index([ManPosition[0],ManPosition[1]])
                   pushableBoxLOC[pp][0]=pushableBoxLOC[pp][0]-1                   
           
        case KeyCodes.RIGHT.value:
            if isMoveValidation:
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[lastScreenValue])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)
               ManPosition[0]=ManPosition[0]+1
               images[ManPosition[1]][ManPosition[0]]=PhotoImage(file=filenames[Getnumber('M')])#(x=x,y=y)
               Label(root,image=images[ManPosition[1]][ManPosition[0]],padx=0,pady=0,borderwidth=0).place(x=ManPosition[0]*tileWidth,y=ManPosition[1]*tileHeight)
               if [ManPosition[0],ManPosition[1]] in pushableBoxLOC:
                   pp=pushableBoxLOC.index([ManPosition[0],ManPosition[1]])
                   pushableBoxLOC[pp][0]=pushableBoxLOC[pp][0]+1                   
           
        case KeyCodes.ENTER.value:
             print('Space=',Space[ManPosition[1]][ManPosition[0]])
            
    PushableBoxRender()
    print("ManPosition=>",ManPosition)
    gameResult=Fitness()
    print("Ressssssssssssssssssult:=>",gameResult)
    if gameResult:
       messagebox.showinfo (title="Game Result", message="You win!!!!")


################################################################ Main code
LoadMap(0)
initMap()
SpaceRender()         

root.bind("<Key>", handle_keypress)
root.mainloop()

