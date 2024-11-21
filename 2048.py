import random,sys
import numpy as np
from colorama import Fore,Back,Style

empty = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
test=[[0,8,2,512],[4,256,32,128],[16,64,4,32],[2,4,16,2]]

''' TO DO:
change display, range of colours
display might break at >4 length numbers
move to tkinter?
new scoring system - fusing numbers adds to your score
add easter egg

'''

colours={0:Style.RESET_ALL + Fore.RESET + Style.DIM,2:Style.RESET_ALL + Fore.RED + Style.NORMAL,4:Style.RESET_ALL + Fore.GREEN + Style.NORMAL,8:Style.RESET_ALL + Fore.YELLOW + Style.NORMAL,
         16:Style.RESET_ALL + Fore.BLUE + Style.NORMAL,32:Style.RESET_ALL + Fore.MAGENTA + Style.NORMAL ,64:Style.RESET_ALL + Fore.CYAN + Style.NORMAL,128:Style.RESET_ALL + Fore.RED + Style.BRIGHT,
         256:Style.RESET_ALL + Fore.GREEN + Style.BRIGHT,512:Style.RESET_ALL + Fore.WHITE + Style.BRIGHT,1024:Style.RESET_ALL + Fore.BLUE + Style.BRIGHT,2048:Style.RESET_ALL + Fore.MAGENTA + Style.BRIGHT,
         4096:Style.RESET_ALL + Fore.CYAN + Style.BRIGHT,8192:Style.RESET_ALL + Fore.BLUE + Style.BRIGHT}


def new(array): #finds empty spaces, chooses one at random and places a 2 or 4
    places = [[a,x] for a in range(4) for x in range(4) if array[a][x]==0]
    a,b = places[np.random.randint(len(places))]
    array[a][b] = random.choices([2,4],weights=[9,1],k=1)[0]
    return array
    
def display(array): # prints the grid in a nice format 
    print('\n\n\n')
    for i in range(4):
        print(Style.RESET_ALL + colours[array[i][0]] + f"{array[i][0]:4n}     " + colours[array[i][1]] + f"{array[i][1]:4n}     " + colours[array[i][2]] + f"{array[i][2]:4n}     " + colours[array[i][3]] + f"{array[i][3]:4n}" + Style.RESET_ALL)
    

def running(array): #tests to see if moves can be made on the board or not
    zeros= [[a,x] for a in range(4) for x in range(4) if array[a][x]==0]
    if len(zeros) == 0:
        tests=[horizontal(array,1),horizontal(array,-1),vertical(array,1),vertical(array,-1)]
        cases=any(True for x in tests if x!= array)
        if cases:
            return True
        else:
            return False
    return True

def horizontal(array,num): # does left-side reduction for each line in array
    output=[]
    for line in array:
        line=line[::num]
        if len(set(line)) == 1 and line.count(0) == 0:
            output.append([2*line[0],2*line[0],0,0][::num])
        else:
            for _ in range(2):
                line=[x for x in line if x != 0]
                for i in range(1,len(line)):
                    if line[i] == line[i-1]:
                        line[i-1] = str(2*line[i-1])
                        line[i] = 0
            answer=[int(x) for x in line] + [0]*(4-len(line))
            output.append(answer[::num])
    return output

def rotate(array,num): # rotates array so reduction can be done to the left
    output=[]
    for i in range(4):  
        output.append([array[x][3-i] for x in range(4)][::num])

    return output[::num]

def vertical(array,num): # rotates array, does logic, and rotates it back
    return rotate(horizontal(rotate(array,num),1),num*(-1))

def score(array): # finds total, this isn't how normaLl 2048 is scored, but it works for now
    return sum([a for x in array for a in x])

def scoreboard(name=None,value=0,yes=False): # opens '2048_scores.txt', which has all names and scores, and adds the players score if wanted
    colour_list=list(colours.values())[1:]

    with open('D:/Python/scripts/2048/2048_scores.txt','r+') as f:
        scores = [a.split(',') for x in f.readlines() for a in x.split('\n') if a]
        names = [scores[i][0] for i in range(len(scores))]

    if yes:
        if name in names:
            if value> int(scores[names.index(name)][1]):
                scores[names.index(name)][1] = str(value)
        
        elif name not in names:
            scores.append([name,str(value)])

    scores.sort(key=lambda x:int(x[1]), reverse=True)

    with open('D:/Python/scripts/2048/2048_scores.txt','w') as f:
        for i in scores:
            f.write(str(i[0]) + ',' + str(i[1]) + '\n')
    a=int(max(len(scores[i][0]) for i in range(len(scores))))
    b=len(scores[0][1])
    print('\n    ' + Back.LIGHTCYAN_EX + ' Scoreboard ' + Style.RESET_ALL,'\n')
    for place,person in enumerate(scores):
        print(colour_list[place%len(colour_list)] + f'    {person[0]:{a}} : {int(person[1]):{b}}   ' + Style.RESET_ALL)

def endgame(array): # when the game ends, handles opening the scoreboard
    print(Back.LIGHTCYAN_EX + f'Game Over, score = {score(array)}' + Style.RESET_ALL,'\n\n')
    appen = input('want to add your score to the leaderboard? (y/n):')
    if appen == 'y':
        name=input('Please input your name: ')
        print('\n')
        scoreboard(name,score(array),True)
        sys.exit()
    else:
        print('\n')
        scoreboard('woop',score(array),False)
        sys.exit()

def game(): # the main game loop
    array=new(new(empty))
    print('2048 started\nmoves are w,a,s,d \nq is quit, e is show scoreboard')
    display(array)
    while running(array):
        yes=True
        direction=input(' move: ')

        if direction == 'q':
            endgame(array)

        if direction == 'test':
            array=test
            yes=False

        if direction == 'e':
            scoreboard(None,None,False)
            yes=False

        if direction == 'a':
            out = horizontal(array,1)
            if out == array:
                print("can't move left any more")
                yes=False
            else:
                array=out

        if direction == 'd':
            out=horizontal(array,-1)
            if out == array:
                print("can't move right any more")
                yes=False
            else: 
                array=out

        if direction == 'w':
            out=vertical(array,1)
            if out == array:
                print("can't move up any more")
                yes=False
            else: 
                array=out

        if direction == 's':
            out=vertical(array,-1)
            if out == array:
                print("can't move down any more")
                yes=False
            else: 
                array=out

        if direction not in ['w','a','s','d','q','e','test']:
            print('Invalid output, dang')
            yes=False

        if yes:
            new(array)
        display(array)
        print('score: ',score(array),'\n\n')

    endgame(array)
    
game()
    
# display(test)
