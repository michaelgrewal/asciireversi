# Michael Grewal
# 100 739 181
# COMP 1405 D2

''' DESCRIPTION & RULES:
This program is a game that consists of 5 levels which are unique gameboards read from files in 
the 'levels' folder. The gameboard is a 2D list of symbols ['@','&','#','%'] and the goal is to make
all the symbols on the gameboard the same in the fewest possible moves.
This player's moves consist of picking a symbol and location on the board. Then, that location and all
contiguous symbols are changed to the player's selected symbol. The player will keep making moves
until the entire gameboard is all the same symbol.'''

def readLevel(levelNum):
    ''' This function takes an integer as argument which represents the level #.
    It will open the corresponding level from file and return a 2D grid containing
    the symbols in the level each as separate elements.'''

    try:
        f = open(f'./levels/ascii_level{levelNum}.txt','r') #open the file
        grid = []                                           #initialize the grid
        allLines = f.readlines()                            #read each line of the file as a list of strings
        
        for i in range(len(allLines)):                      #grab each line one at a time
            allLines[i] = allLines[i].replace('\n','')      #remove trailing '\n' from each line

            #create the inner list with each symbol as an element
            innerList = []
            for c in allLines[i]:                       
                innerList.append(c)
            
            #append the inner list to the grid
            grid.append(innerList)

        f.close()       #close the file
        return grid     #return the grid

    except:
        print(f"Failed to read level {levelNum}. Game ending.")
        exit()



def displayBoard(grid):
    ''' This function takes a 2D grid as argument and prints the grid as a gameboard.'''

    columns = ''                    #initialize column label string

    for i in range(len(grid[0])):   #find the appropriate # of columns
        columns+=(str(i%10))        #only print single digit labels 0-9, e.g. 13 would be 3

    #print column labels and separator bar
    print('   '+columns)
    print('   '+'-'*len(columns))

    #print each row
    for i in range(len(grid)):          #grab a row (i.e. element from grid)
        output = f"{i:02}|"             #output initialized with row #

        for j in range(len(grid[i])):   #print every symbol in each row
            output+=grid[i][j]

        print(output)



def getUserAction(outer,inner):
    ''' This function takes two integers as arguments representing the height (length of outer list,
    also can be thought of as the y coordinate) and the width (length of inner list, also can be
    thought of as the x coordinate)
    This function returns a single data structure containing the user's inputs (symbol, row, and col),
    respectively.'''

    #ask user for their inputs and loop until inputs are valid:

    #symbol input
    while True:
        userSymbol = input("Enter a symbol: ")
        #ensure valid symbol choices
        validSymbols = ['&','@','#','%']
        if userSymbol in validSymbols:
            break
        elif userSymbol not in validSymbols:
            print("Sorry, please select one of: # & % @")
    
    #row input
    while True:
        userRow = input(f"Select a row: [0,{outer}]: ")
        #ensure valid user row choices
        if userRow.isdigit() == False:
            print(f"Your choice was not a number between 0 and {outer}.")
        if int(userRow)>outer or int(userRow)<0:
            print(f"Error bad row. Enter a number from 0 to {outer}.")
        else:
            break
            
    #column input
    while True:
        userCol = input(f"Select a col: [0,{inner}]: ")
        #ensure valid user column choices
        if userCol.isdigit() == False:
            print(f"Your choice was not a number between 0 and {inner}.")
        if int(userCol)>inner or int(userCol)<0:
            print(f"Error bad col. Enter a number from 0 to {inner}.")
        else:
            break
    
    #return the list containing user's inputs in order symbol, row, col.
    return [userSymbol,int(userRow),int(userCol)]


        
def fill(grid,target,userSymbol,row,col):
    ''' This function takes the 2D grid gameboard, a target symbol to be replaced, the user's 
    chosen symbol, a row index and a column index in order to mutate the symbols in the gameboard.
    It works recursively, and mutates one cell at a time.'''

    '''Check if the user's chosen symbol is different from the target symbol AND if the target 
    is the same symbol that was originally at the user's chosen row and column inputs.
    This will ensure the fill function fills only the appropriate cells.'''

    if userSymbol != target and target == grid[row][col]:

        #change the symbol at target location to user's input symbol
        grid[row][col] = userSymbol

        #keep the recursive calls within the boundaries of the gameboard               
        if row<len(grid)-1:
            fill(grid,target,userSymbol,row+1,col)
        if row>0:
            fill(grid,target,userSymbol,row-1,col)
        if col<len(grid[0])-1:
            fill(grid,target,userSymbol,row,col+1)
        if col>0:
            fill(grid,target,userSymbol,row,col-1)



def main():
    ''' This function orchestrates the core behaviour of the game. It calls all the other functions
    and gets them all communicating together so that the game can be executed properly.'''

    totalUserMoves = 0          #initialize a counter for total user moves made

    #create a loop for all 5 levels (1 to 5)
    for i in range(1,6):
        print("")               #blank space

        grid = readLevel(i)     #create the gameboard and call it grid
        displayBoard(grid)      #display the gameboard

        #initialize a list of all valid symbols
        symbols = ['&','@','#','%']

        #initialize a counter for number of moves the user has made this level   
        userMoves = 0

        '''Create another loop so the user can keep playing until the gameboard is complete
        the gameboard is only complete when every cell is the same symbol.'''

        runRound = True                 #flag
        while runRound:

            #get the user's input
            userActions = getUserAction(len(grid)-1,len(grid[0])-1)
            userMoves += 1                  #add 1 to moves made

            #give names to user's inputs
            userSymbol = userActions[0]
            userRow = userActions[1]
            userCol = userActions[2]

            #find the target symbol with user's input row and column
            target = grid[userRow][userCol]

            #call the fill() function to fill appropriate cells
            fill(grid,target,userSymbol,userRow,userCol)

            #display the gameboard again
            print("")                   #blank space
            displayBoard(grid)

            '''Check to see if user has won or still needs to play. This is accomplished by
            searching through every cell on the gameboard and checking if every cell is the
            same symbol. If they are all the same then the user has won the level. If there
            are at least 2 different types of symbols on the gameboard then the level keeps
            on running.'''
            
            for s in symbols:                   #check every possible symbol
                count = 0                       #initialize a counter at 0
                for j in range(len(grid)):      #count how many occurences of symbol are in each row
                    count+=grid[j].count(s)
                
                #if the count matches the number of cells on the gameboard then level complete!
                if count == len(grid)*len(grid[0]):
                    print(f"Level {i} Completed in {userMoves} moves!")
                    totalUserMoves += userMoves
                    runRound = False            #set flag to false to load the next level
    
    #closing print statements
    print("You win! Thanks for playing!")
    print(f"Total moves: {totalUserMoves}")

    #ask user if they want to play again
    while True:
        playAgain = input("Would you like to play again? (y/n): ")
        if playAgain == 'y':
            break
        if playAgain == 'n':
            exit()
        #catch invalid responses
        elif playAgain != 'y' and playAgain != 'n':
            print("")
            print("Invalid response. Please enter 'y' or 'n'.")
            print("")

    #run the main() function again if user enters 'y'
    main()



#call main() to start the game
main()