import random
import curses

"""I made all of this for fun so please dont judge me too hard :("""

#minesweeper class
#this class simulates a minesweeper board, it holds both the dynamic board
#that means the one the user will interact with, as well as the static board with
#answers, and a board use to compare the score of the user
level = [[8,8,10],[16,16,40],[16,30,40]]

class MineSweeper:
    global level

    #generate mined camp (without maked tiles)
    BOMB   = '*'
    ROUND  = 3
    NOBOMB = 0
    BLANK  = ' ' 
    FLAG   = '!' 
    EMPTY  = '#'

    def __init__(self, dif):

        sizex, sizey, bombs = level[dif][1],level[dif][0], level[dif][2]


        #dont no iif this is good 
        self.boardx = sizex 
        self.boardy = sizey 

        self.bombs = bombs
        self.ongoing = [[self.EMPTY for _ in range(sizex)] for _ in range(sizey)]
    
        self.gamestatus = 0

        self.mineGen(sizex, sizey, bombs)

    def mineGen(self, sizex, sizey, bombs):
        board = [[self.NOBOMB for _ in range(sizex)] for _ in range(sizey)]
        self.score  = board
        l = []
        while(bombs):
            bombx = random.randint(0,sizex-1)
            bomby = random.randint(0,sizey-1)

            if board[bomby][bombx] == self.NOBOMB:
                board[bomby][bombx] = self.BOMB
                l.append((bomby, bombx))
                bombs-=1

        self.static = board
        self.comp = board
        self.mineNum()

    #changes tiles around a bomb
    def mineCheck(self, y, x):
        x1 = x -1
        x -= 1
        y -= 1

        for i in range(self.ROUND):
            if y >= 0 and y < len(self.static):
                for j in range(self.ROUND):
                    if x >= 0 and x < len(self.static[j]):
                        if self.static[y][x] != self.BOMB:
                            self.static[y][x]+=1
                    x+=1
            x = x1
            y+=1

    #searces for bombs to change tiles around it 
    def mineNum(self):
        for i in range(len(self.static)):
            for j in range(len(self.static[i])):
                if self.static[i][j] == self.BOMB:
                     self.mineCheck(i, j)
    
    def compareScore(self):
        for i in range(len(self.score)):
            for j in range(len(self.score[0])):
                if self.score[i][j] != self.comp[i][j]:
                    return 1
        return 0 

    def flag(self, y, x):
        if self.ongoing[y][x] != self.FLAG:
            self.ongoing[y][x] = self.FLAG
            self.score[y][x] = self.BOMB
        else:
            self.ongoing[y][x] = self.EMPTY
            self.score[y][x] = self.NOBOMB

    def deflag(self, y, x):
        self.ongoing[y][x] = self.EMPTY
        self.score[y][x] = self.NOBOMB

    def reveal(self, y, x):
        if self.static[y][x] == self.BOMB:
            return -1

        elif self.static[y][x] > 0:
            self.ongoing[y][x] = self.static[y][x]
            return 0

        self.revealIter(y, x, [])
        return 0
    
    #reveal neighbouring tiles
    def revealIter(self, y, x, prev):
        max_y = range(len(self.static))
        max_x = range(len(self.static[0]))

        if y in max_y and x in max_x:
            y1, x1 = y-1, x-1
            for i in range(3):
                for j in range(3):
                    if y1+i in max_y and x1+j in max_x and [y1+i, x1+j] not in prev:
                        if self.static[y1+i][x1+j] == self.NOBOMB:
                            self.ongoing[y1+i][x1+j] = self.BLANK
                            prev.append([y1+i, x1+j])
                            self.revealIter(y1+i, x1+j, prev)

                        elif self.static[y1+i][x1+j] == self.BOMB:
                            prev.append([y1+i, x1+j])

                        else:
                            self.ongoing[y1+i][x1+j] = self.static[y1+i][x1+j] 
                            prev.append([y1+i, x1+j])
                            
def position(index, maxi, m):
    index += m
    if index < 0:
        index = maxi + index
    elif index >= maxi:
        index = index - maxi 
    return index

class Menu:

    menu_strs = ["    play    ", "    exit    "]
    menu_nw = ["easy", "medium", "hard"]

    inst = [
        "- Use arrow keys to move around the board", 
        "- Press d to detonate, and f to flag or deflag a possible bomb"]
   
    def __init__(self, screen):
        self.stdscr = screen
        self.max_y, self.max_x = self.stdscr.getmaxyx()

        #cursor position for the menu only
        self.cursor = 0
        self.saved = None
        self.mine = None


    #prints the content of the array in the screen, one item on top of the other
    #if cursor matches the index, it will be printed with the color in self.pair
    def printScrLoop(self, arr, color=1):

        for i in range(len(arr)):
            p = 0
            y, x = self.max_y//2+i, self.max_x//2 - len(arr[i])//2
            if self.cursor == i:

                p = color

            self.stdscr.addstr(y, x, arr[i], curses.color_pair(p))
        self.stdscr.refresh()

    def instructions(self):
        self.stdscr.clear()

        h = "Happy playing!"
        press = "Press any key to continue"

        y, x = self.max_y//2+3, self.max_x//2 - len(press)//2
        self.stdscr.addstr(y-5, x, h, curses.color_pair(4))
        self.stdscr.addstr(y, x-2, press, curses.color_pair(3))

        self.printScrLoop(self.inst, 0)
        
        c = self.stdscr.getch()

    def menuNewGame(self):
        self.stdscr.clear()
        difficulty = "select difficulty"

        y,x = self.max_y//2-3, self.max_x//2 - len(difficulty)//2

        y = 0

        self.stdscr.addstr(y, x, difficulty, curses.color_pair(2))
      
        while True:
            
            self.stdscr.clear()
            self.printScrLoop(self.menu_nw)

            c = self.stdscr.getch()

            if c == curses.KEY_UP:
                self.cursor = position(self.cursor, len(self.menu_nw), -1)
            elif c == curses.KEY_DOWN:
                self.cursor = position(self.cursor, len(self.menu_nw), 1)

            elif c == ord('s'):
                self.mine = Game(self.stdscr, self.cursor)
                self.mine.mineSweeper()

            elif c == ord('q'):
                return 0

    def menuStart(self):

        w = "Welcome to mine minesweeper, enjoy! :)"
        cre = "Made by Clemens Schrage aka skreije"
        press = "Press s to select something and q to quit "

        while True:

            #prints menu stuff on  
            self.stdscr.clear()

            y, x = self.max_y//2, self.max_x//2 - len(w)//2
            self.stdscr.addstr(y-7, x, w, curses.color_pair(3))
            x = self.max_x//2 - len(cre)//2
            self.stdscr.addstr(y-6, x, cre, curses.color_pair(0))
            x = self.max_x//2 - len(press)//2
            self.stdscr.addstr(y-4, x, press, curses.color_pair(0))


            self.printScrLoop(self.menu_strs)

            c = self.stdscr.getch()

            if c == curses.KEY_UP:
                self.cursor = position(self.cursor, len(self.menu_strs), -1)
            elif c == curses.KEY_DOWN:
                self.cursor = position(self.cursor, len(self.menu_strs), 1)

            elif c == ord('s'):
                if self.menu_strs[self.cursor] == "    play    ":
                    self.instructions()
                    self.menuNewGame() 
                else:
                    break

            elif c == ord('q'):
                return 0


class Game:

    global level


    def __init__(self, screen, dif):

        #cursor for game only
        self.cursor = [0,0]
        self.stdscr = screen
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.dif = dif

    #this method prints the minesweeper board onto the terminal
    #if cursor matches the index, it will be printed with the color in self.pair

    def printBoard(self):
        #this certers the board rendering in the middle of the screen so it doesnt die

        init_y = 1 
        init_x = self.max_x//2 - self.mine.boardx//2

        if init_x < 0: 
            init_x = 3 
        else:
            pass

        for i in range(self.mine.boardy):
            for j in range(self.mine.boardx):

                y, x = init_y+i, init_x+j
                c = self.mine.ongoing[i][j]
                p = 0
                #if cursor then color is choosen
                if [i , j] == self.cursor:
                    p = 1
                if y < self.max_y and x < self.max_x :
                    self.stdscr.addstr(y, x, str(c), curses.color_pair(p))

    #calculates a number based on the maxi(max of the total array length) 
    #an index which will be modified by the quantity m 
        #makes a move inside the minesweeper board
    def makeMove(self, y, x):
        self.mine.gamestatus = self.mine.reveal(y, x)
    
    def gameOver(self):

        lost = "LOOKS LIKE YOU LOST YOU PIECE OF SHIT"
        press = "PRESS ANY KEY TO GO BACK TO THE MENU"

        y, x = self.max_y//6, self.max_x//2
        self.stdscr.addstr(y, x, lost, curses.color_pair(2))
        self.stdscr.addstr(y+1, x, press, curses.color_pair(2))

        c = self.stdscr.getch()
        
    def gameWon(self):

        lost = "LOOKS LIKE YOU WON YOU PIECE OF SHIT"
        press = "PRESS ANY KEY TO GO BACK TO THE MENU"

        y, x = self.max_y//2, self.max_x//2
        self.stdscr.addstr(y, x, lost, curses.color_pair(2))
        self.stdscr.addstr(y+1, x, lost, curses.color_pair(2))

        c = self.stdscr.getch()

    def mineSweeper(self):

        self.stdscr.clear()
        self.mine = MineSweeper(self.dif)

        self.cursor = [0,0]

        while self.mine.gamestatus == 0:

            self.mine.gamestatus = self.mine.compareScore()

            y, x = 0, self.max_x//4
            self.stdscr.addstr(y, x, "YOU ARE PLAYING MINESWEEPER", curses.color_pair(3))

            self.pair = 1
            self.printBoard()

            c = self.stdscr.getch()

            if c == curses.KEY_UP:
                self.cursor[0] = position(self.cursor[0], len(self.mine.static), -1)
            elif c == curses.KEY_DOWN:
                self.cursor[0] = position(self.cursor[0], len(self.mine.static), 1)
            elif c == curses.KEY_LEFT:
                self.cursor[1] = position(self.cursor[1], len(self.mine.static[self.cursor[0]]), -1)
            elif c == curses.KEY_RIGHT:
                self.cursor[1] = position(self.cursor[1], len(self.mine.static[self.cursor[0]]), 1)
            elif c == ord('d'):
                y, x = self.cursor[0], self.cursor[1]
                self.makeMove(y, x)
                
            elif c == ord('f'):
                self.mine.flag(self.cursor[0], self.cursor[1])
            elif c == ord('q'):
                return 0


        #gameover  
        if self.mine.gamestatus == -1:
            self.gameOver()
        #win
        elif self.mine.gamestatus == 1:
            self.gameWon() 

def main(stdscr):

    stdscr.clear()
    stdscr.keypad(1)

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    menu = Menu(stdscr)
    menu.menuStart()

curses.wrapper(main)

