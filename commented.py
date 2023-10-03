# Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9.4 programming environment

import random
import os


def Main():
    Again = "y"  # This sets again to "y", so the while loop will run at least once. This could be a different value, as
    # long as the condition for the while loop is true. If it were false, the game would never start, and give no option
    # to run again.
    Score = 0  # Initialises the variable. This does not serve a purpose, as it will be overwritten later. It is most
    # likely here because of C++ and other languages, where variables need to be declared before assignment.
    while Again == "y":  # Starts a new game if the user wishes. If not, the program will end.
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:  # Checks if the user has not just pressed enter only. If they have not, the puzzle can be
            # loaded from the file
            MyPuzzle = Puzzle(Filename + ".txt")  # This loads the puzzle from the file. It adds the file extension, so
            # the user does not need to remember it. This does catch all exceptions from loading the file, but does not
            # re-prompt the user, instead getting stuck in a loop of asking for a symbol (as there is not a list of valid
            # characters).
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6)) # Creates the default game. First argument is the grid size, and
            # the second is the number of remaining symbols (number of turns). It is grid size (x) * grid size (y) *
            # scale factor.
        Score = MyPuzzle.AttemptPuzzle()  # Runs the game. The function returns the user's score.
        print("Puzzle finished. Your score was: " + str(Score))  # Output the user's score from the game
        Again = input("Do another puzzle? ").lower()  # .lower method removes case sensitivity for the user input


class Puzzle():  # Create Puzzle Class. Does not inherit from another class
    def __init__(self, *args):
        if len(args) == 1:  # If args has one item it is the filename for a game from a text file to open.
            # *args: 1 item
            #   args[0] -> puzzle file name.
            self.__Score = 0  # Set the user's score to 0.
            self.__SymbolsLeft = 0  # Declare the number of Symbols Left (number of moves for the user) - this is
            # overwritten by the __LoadPuzzle method call.
            self.__GridSize = 0  # Declare the grid size. This is again overwritten inn the __LoadPuzzle method call
            self.__Grid = []  # Declare and assign the Grid variable to an empty array. This is used, and appended to
            # in the __LoadPuzzle method, so MUST be declared here as an empty list.
            self.__AllowedPatterns = []  # Declare and assign the allowed patterns variable to an empty array. This is
            # again added to when the __LoadPuzzle method is called. It uses append, so this MUST be assigned here.
            self.__AllowedSymbols = []  # Declare and assign the allowed symbols variable to an empty list. This is
            # then appended to in the __LoadPuzzle method call, so must be assigned to an empty list here.
            self.__LoadPuzzle(args[0])  # Loads the puzzle from the text file. args[0] is the filename.txt of the puzzle
            # to load.
        else:  # This expects args to have two elements.
            # *args: 2 items (expected, not enforced)
            #   args[0] -> Grid Size (Grid is square, so this is for both x * y)
            #   args[1] -> Number of Symbols remaining (
            self.__Score = 0  # Sets the score to 0.
            self.__SymbolsLeft = args[1]  # Set the number of remaining symbols to the second argument.
            # __SymbolsLeft acts as counter for the number of remaining moves the user has. According to the default
            # game, the recommended value is GridSize^2 * 0.6
            self.__GridSize = args[0]  # Sets the grid size for the user board. The board is square, so this is for both
            # the sides. For the default game, this is 8.
            self.__Grid = []  # Declares the cell variable, with an empty list. This must be performed, as it is
            # appended to, to add the Cell and Blocked Cell instances to the board
            for Count in range(1, self.__GridSize * self.__GridSize + 1):  # Iterates through all tiles that should be
                # in the grid (grid size squared). This is done as one loop, as the grid is stored as a single-dimension
                # list. The increment by 1, is because the range runs from 1 -> GridSize^2 + 1, inclusive, then
                # exclusive. Removing the 1 as first parameter, and removing the increment would also work, and may be
                # faster.
                if random.randrange(1, 101) < 90:  # Generate a random number between 1 and 100 (inclusive).
                    # This gives an 89% chance of a cell being unblocked. It is 89% not 90%, as it is less than 90, not
                    # inclusive.
                    C = Cell()  # Create an empty cell instance (indicated by a space)
                else:  # 11% chance of being a blocked cell.
                    C = BlockedCell()  # Create a blocked cell instance (represented by an @ symbol)
                self.__Grid.append(C)  # Add the created class instance the grid list
            self.__AllowedPatterns = []  # Create an empty list for the valid patterns. It needs to be done, as it is
            # appended to.
            self.__AllowedSymbols = []  # Create an empty list for the valid symbols that can be entered by the user.
            # This needs to be done here, as it is appended to later.
            QPattern = Pattern("Q", "QQ**Q**QQ")  # Adds the pattern for the Q shape to the
            # allowed patterns list. * means any value. Symbols are read in a spiral.
            # Q Q *
            # Q Q *
            # * * Q
            self.__AllowedPatterns.append(QPattern)  # Adds the pattern to the list
            self.__AllowedSymbols.append("Q")  # Adds the new allowed symbol to the AllowedSymbols list
            XPattern = Pattern("X", "X*X*X*X*X")  # Create the pattern for the X symbol.
            # X * X
            # * X *
            # X * X
            self.__AllowedPatterns.append(XPattern)  # Adds the pattern to the list off allowed patterns
            self.__AllowedSymbols.append("X")  # Add the symbols to the AllowedSymbols list.
            TPattern = Pattern("T", "TTT**T**T")  # Create a new pattern for the T symbol
            # T T T
            # * T *
            # * T *
            self.__AllowedPatterns.append(TPattern)  # Adds the new pattern to the AllowedPatterns list.
            self.__AllowedSymbols.append("T")  # Add the new symbol to the allowed symbols list.

            # This segment could be simplified as:
            # self.__AllowedPatterns = [
            #     Pattern("Q", "QQ**Q**QQ"),
            #     Pattern("X", "X*X*X*X*X"),
            #     Pattern("T", "TTT**T**T")
            # ]
            # self.__AllowedSymbols = ["Q", "X", "T"]

    def __LoadPuzzle(self, Filename):
        # The parameter Filename needs to include the file extension.
        try:
            with open(Filename) as f:  # Open the text file. The mode is not specified, so it is opened as read only.
                # with open() as f:... opens the file with the object assigned to f. When the code inside the with has
                # executed, the file is automatically closed.
                # f.readline reads the current line of the text file. After it has been called, it moves to the next
                # line, so the next time f.readline() is called, it gives the value of the next line. It also returns a
                # string, regardless of the datatype in the line. .readline() also includes all trailing whitespace,
                # including line endings.
                NoOfSymbols = int(f.readline().rstrip())  # Gets the number from the first line of the text file, and
                # assigns it to the number of symbols. .rstrip() removes the trailing whitespace from the line,
                # including the "\n".
                for Count in range(1, NoOfSymbols + 1):  # This runs NoOfSymbols times.
                    self.__AllowedSymbols.append(f.readline().rstrip())  # Reads each line, removes the trailing
                    # whitespace, and adds to the AllowedSymbols list. The line should only contain a single character.
                NoOfPatterns = int(f.readline().rstrip())  # Gets the next line, which is a number. It casts to an int,
                # so it can be iterated over using range. This should be the same as NoOfSymbols, as each symbol should
                # have a corresponding pattern
                for Count in range(1, NoOfPatterns + 1):  # Iterate NoOfPatterns times. The count variable isn't needed.
                    Items = f.readline().rstrip().split(",")  # Reads the line, then removes the trailing whitespace,
                    # then splits into a list on the comma. The first item is the symbol, and the second is the pattern.
                    P = Pattern(Items[0], Items[1])  # Create a new pattern instance, using the read values.
                    self.__AllowedPatterns.append(P)  # Add the new pattern to the AllowedPatterns list.
                self.__GridSize = int(f.readline().rstrip())  # Read the next line from the file, and remove the
                # trailing whitespace. It is then cast to an integer, so it can be used as the GridSize, and be used
                # with range for a FOR loop.
                for Count in range(1, self.__GridSize * self.__GridSize + 1):  # Iterate from 1 to GridSize^2
                    # (inclusive), which is every available cell in the grid. The count variable is not used.
                    Items = f.readline().rstrip().split(",")  # Read the next line from the file, remove the trailing
                    # whitespace, and split on commas. The first value is the current value in the tile, where an empty
                    # string means the cell is blank. The values after that are the values that cannot be placed in that
                    # cell.

                    # Note that for blocked tiles, instance.CheckSymbolAllowed() is always false, so the all the symbols
                    # the user can place do NOT need to be added after it.

                    # Items: length>=2
                    #   Items[0]: current value in tile ('@' is blocked, '' is empty)
                    #   Items[1:]: invalid values for tile
                    if Items[0] == "@":  # Checks whether the cell is blocked
                        C = BlockedCell()  # Create a new blocked cell instance.
                        self.__Grid.append(C)  # Add the new cell instance to the grid. The order that they are added
                        # are the order that they appear on the grid. .append() adds the instance to the end, so it
                        # fills in the grid from the left to right, each row at a time, from top to bottom.
                    else:
                        C = Cell()  # Create a new cell instance.
                        C.ChangeSymbolInCell(Items[0])  # Change the symbol in the cell to that specified by Items[0].
                        # Note if Items[0] is an empty string, it does not affect the output. It appears as a space, and
                        # with no difference to not running this statement.
                        for CurrentSymbol in range(1, len(Items)):  # Runs len(Items) - 1 times. It needs to run one
                            # fewer times than the length of Items, as it should not include Items[0], as that is the
                            # current symbol in the cell.
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])  # Adds the current symbol in Items to the
                            # list of not allowed symbols. This can add a second space when there is a trailing comma on
                            # the line. This is good as it prevents the user replacing a piece they have placed with a
                            # space.
                        self.__Grid.append(C)  # Adds the new class instance to the grid. Again, this appends it to the
                        # end, so it is done in order, left-right.
                self.__Score = int(f.readline().rstrip())  # Reads the next line from the file, and casts it to an
                # integer, so it can be added easily. This is the user's starting score.
                self.__SymbolsLeft = int(f.readline().rstrip())  # This reads the final line of the file and removes the
                # trailing whitespace. It then casts it to an integer, so it can be decremented easily, as it is the
                # number of remaining symbols (the number of moves the user can perform).
        except:  # Catches all exceptions. This is assumed to be that the file is not found. This is bad practice, as
            # the error is not specified. It should catch FileNotFoundError. This can be an issue, as it prevents
            # KeyboardInterrupts, as they are included within this. Furthermore, if the file is not found, it will say
            # file not found, but will not prompt the user for a new one. The game continues, but without a board,
            # prompting for a row then a column from the user. Once this has happened, it asks for the symbol to be
            # entered, but the list of valid characters is empty, and therefore, any entered symbol is invalid, so it
            # re-prompts for another. This means the program gets stuck in an endless loop of asking for a symbol to be
            # entered. This could be solved by not catching the error here, but instead catching it when the user is
            # initially prompted for the filename. If it is not valid, it can easily loop around again until a valid
            # filename is entered found.
            print("Puzzle not loaded")  # Output to the user that the file has not been loaded successfully.

    def AttemptPuzzle(self):
        Finished = False  # Assign Finished to False. This means the subsequent while loop will run at least once. This
        # does prevent SymbolsLeft being 0, as it will still allow the user to place one.

        # The while clause could be replaced with:
        # while not self.__SymbolsRemaining:
        # This has the benefit of removing one variable and an if statement, which would be more time and space
        # efficient.
        while not Finished:  # While the user still has remaining symbols, the loop will continue.
            self.DisplayPuzzle()  # Display the puzzle grid
            print("Current score: " + str(self.__Score))  # Display the current user's score. The score needs to be cast
            # to a string, as integers cannot be concatenated to strings.
            Row = -1  # Declare the Row variable. This is likely from other programming languages where variables need
            # to be declared before they can be assigned.
            Valid = False  # Ensures that the while loop will run at least once.
            while not Valid:  # Runs until the user enters a valid row number.
                try:
                    Row = int(input("Enter row number: "))  # Gets an input from the user. If it can be converted to an
                    # integer it is then valid, and the loop stops. If it cannot, the except clause runs, and the user
                    # is prompted again.

                    # This does not check whether the value entered is within the grid. If it is not, it is still
                    # treated as valid, and can then cause IndexError, when it tries to access a cell outside of this
                    # range
                    Valid = True  # Stops the iteration. This does not run if there is an error in the previous line.
                except:  # This is bad practice, as it stops all errors, including KeyboardInterrupts, so it is
                    # difficult to stop the program. It should catch ValueError
                    pass
            Column = -1
            Valid = False  # Ensures that the while loop will run at least once.
            while not Valid:  # Runs until the user enters a valid row number.
                try:
                    Column = int(input("Enter column number: "))  # Gets an input from the user. If it can be converted
                    # to an integer it is then valid, and the loop stops. If it cannot, the except clause runs, and the
                    # user is prompted again.

                    # This does not check whether the value entered is within the grid. If it is not, it is still
                    # treated as valid, and can then cause IndexError, when it tries to access a cell outside of this
                    # range
                    Valid = True  # Stops the iteration. This does not run if there is an error in the previous line.
                except:  # This is bad practice, as it stops all errors, including KeyboardInterrupts, so it is
                    # difficult to stop the program. It should catch ValueError
                    pass
            Symbol = self.__GetSymbolFromUser()  # This prompts the user to input a value. This handles the inputted
            # symbol not being a valid symbol in the game only. This does not check whether it is allowed for the
            # specific cell.
            self.__SymbolsLeft -= 1  # This reduces the number of symbols they have left by one, and, consequently, the
            # number of remaining turns they have. This runs regardless of whether the entered cell is valid in the
            # selected tile.
            CurrentCell = self.__GetCell(Row, Column)  # Get value of the cell entered by the user. If it is not a valid
            # cell it raises IndexError
            if CurrentCell.CheckSymbolAllowed(Symbol):  # This checks that the symbol that the user entered can be
                # placed in the selected cell.
                CurrentCell.ChangeSymbolInCell(Symbol)  # If the symbol is valid, it changes the symbol in the cell to
                # the one that was entered.
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)  # Check whether the new symbol created
                # a pattern. If it did, CheckforMatchWithPattern() returns 10 (hard-coded), and if it did not, it
                # returns 0. This then increases the user's score by this amount, so a pattern increases by 10, and no
                # match has not effect.
                if AmountToAddToScore > 0:  # This then increases the score by the amount. The if doesn't achieve
                    # anything, as adding 0 would not have an effect, which would be more space and time efficient.
                    self.__Score += AmountToAddToScore
            if self.__SymbolsLeft == 0:  # If the number of symbols left is 0, the user can not place any more cells, so
                # this is the end of the game.
                Finished = True  # This stops the game from looping again
        print()  # Just for formatting
        self.DisplayPuzzle()
        print()
        return self.__Score  # Returns the user's score to be displayed in the main function.

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:  # This does not achieve anything, as the previous line would raise the same error if the clause was not
            # met.
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())


class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def MatchesPattern(self, PatternString, SymbolPlaced):
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
        return self.__PatternSequence


class Cell():
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        if self.IsEmpty():
            return "-"
        else:
            return self._Symbol

    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass


class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        return False


if __name__ == "__main__":
    Main()