import random
import time
import curses 

#minesweeper class
level = [[8,8,10],[16,16,40],[16,30, 40]]
class MineSweeper:
    global level

    #generate mined camp (without maked tiles)
    BOMB   = '*'
    ROUND  = 3
    NOBOMB = 0
    BLANK  = ' ' 
    FLAG   = '!' 
    EMPTY  = '#'

    def __init__(self, dif, change=None):

        sizex, sizey, bombs = 0,0,0

        if dif <= 2 and dif >=0:
            sizex, sizey, bombs = level[dif][1],level[dif][0], level[dif][2]

        if change is not None: 
            sizex, sizey, bombs = change[1],change[0],change[2]
        
        self.bombs = bombs
        self.ongoing = [[self.EMPTY for _ in range(sizex)] for _ in range(sizey)]
    
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
        self.ongoing[y][x] = self.FLAG
        self.score[y][x] = self.BOMB

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
                            

    #print board

class Game:

    global level

    menu_strs = ["new game", "resume", "exit"]
    menu_nw = ["easy", "medium", "hard", "user defined"]

    def __init__(self, screen):

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        self.cursor = [0,0]
        self.stdscr = screen
        self.pair = 0
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.mine = None
        self.gamestatus = 0

    def printBoard(self):
        for i in range(len(self.mine.ongoing)):
            for j in range(len(self.mine.ongoing[i])):

                y, x = self.max_y//2+i, self.max_x//3+j
                c = self.mine.ongoing[i][j]
                p = 0

                if [i , j] == self.cursor:
                    p = self.pair

                self.stdscr.addstr(y, x, str(c), curses.color_pair(p))


    def position(self, index, maxi, m):
        index += m
        if index < 0:
            index = maxi + index
        elif index >= maxi:
            index = index - maxi 
        return index

    def printScrLoop(self, arr):

        for i in range(len(arr)):
            p = 0
            y, x = self.max_y//2+i, self.max_x//2 - len(arr[i])//2
            if self.cursor[0] == i:

                p = self.pair

            self.stdscr.addstr(y, x, arr[i], curses.color_pair(p))
        self.stdscr.refresh()

    def makeMove(self, y, x):
        self.gamestatus = self.mine.reveal(y, x)
    
    def gameOver(self):

        self.stdscr.clear()

        lost = "LOOKS LIKE YOU LOST YOU PIECE OF SHIT"
        press = "PRESS ANY KEY TO GO BACK TO THE MENU"

        y, x = self.max_y//6, self.max_x//2
        self.stdscr.addstr(y, x, lost, curses.color_pair(2))
        self.stdscr.addstr(y+1, x, lost, curses.color_pair(2))

        c = self.stdscr.getch()
    def gameWon(self):

        self.stdscr.clear()
        lost = "LOOKS LIKE YOU WON YOU PIECE OF SHIT"
        press = "PRESS ANY KEY TO GO BACK TO THE MENU"

        y, x = self.max_y//2, self.max_x//2
        self.stdscr.addstr(y, x, lost, curses.color_pair(2))
        self.stdscr.addstr(y+1, x, lost, curses.color_pair(2))

        c = self.stdscr.getch()

    def mineSweeper(self, dif, change=None):

        self.stdscr.clear()
        self.mine = MineSweeper(dif, change)

        self.cursor = [0,0]

        while self.gamestatus == 0:

            self.gamestatus = self.mine.compareScore()

            y, x = 0, self.max_x//4
            self.stdscr.addstr(y, x, "YOU ARE PLAYING MINESWEEPER", curses.color_pair(3))

            self.pair = 1
            self.printBoard()

            c = self.stdscr.getch()

            if c == curses.KEY_UP:
                self.cursor[0] = self.position(self.cursor[0], len(self.mine.static), -1)
            elif c == curses.KEY_DOWN:
                self.cursor[0] = self.position(self.cursor[0], len(self.mine.static), 1)
            elif c == curses.KEY_LEFT:
                self.cursor[1] = self.position(self.cursor[1], len(self.mine.static[self.cursor[0]]), -1)
            elif c == curses.KEY_RIGHT:
                self.cursor[1] = self.position(self.cursor[1], len(self.mine.static[self.cursor[0]]), 1)
            elif c == ord('s'):
                y, x = self.cursor[0], self.cursor[1]
                self.makeMove(y, x)
                
            elif c == ord('f'):
                self.mine.flag(self.cursor[0], self.cursor[1])
            elif c == ord('q'):
                return 0


        #gameover  
        if self.gamestatus == -1:
            self.gameOver()
        #win
        elif self.gamestatus == 1:
            self.gameWon() 

    def menuNewGame(self):


        self.stdscr.clear()
        difficulty = "select difficulty"
        y,x = self.max_y//2-3, self.max_x//2 - len(difficulty)//2

        y = 0
        self.cursor = [0,0]

        self.stdscr.addstr(y, x, difficulty, curses.color_pair(2))
         
        while True:
            
            self.stdscr.clear()
            self.printScrLoop(self.menu_nw)

            c = self.stdscr.getch()

            if c == curses.KEY_UP:
                self.cursor[0] = self.position(self.cursor[0], len(self.menu_nw), -1)
            elif c == curses.KEY_DOWN:
                self.cursor[0] = self.position(self.cursor[0], len(self.menu_nw), 1)

            elif c == ord('s'):
                if self.cursor[0] in  range(3):
                    self.mineSweeper(self.cursor[0])
                    break

                else:
                    pass

            elif c == ord('q'):
                return 0

    def menuStart(self):
    
        self.cursor = [0,0]
        

        while True:

            #prints menu stuff on  
            self.pair = 1
            self.stdscr.clear()
            self.printScrLoop(self.menu_strs)

            c = self.stdscr.getch()

            if c == curses.KEY_UP:
                self.cursor[0] = self.position(self.cursor[0], len(self.menu_strs), -1)
            elif c == curses.KEY_DOWN:
                self.cursor[0] = self.position(self.cursor[0], len(self.menu_strs), 1)

            elif c == ord('s'):
                if self.menu_strs[self.cursor[0]] == "new game":
                    self.menuNewGame()
                elif self.menu_strs[self.cursor[0]] == "resume":
                    pass
                elif self.menu_strs[self.cursor[0]] == "exit":
                    break

            elif c == ord('q'):
                return 0

def main(stdscr):

    stdscr.clear()
    stdscr.keypad(1)
    game = Game(stdscr)
    game.menuStart()

    #mine.printb()

curses.wrapper(main)

