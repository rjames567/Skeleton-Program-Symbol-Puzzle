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
        if len(args) == 1:  # If args has one item it is is the filename for a game from a text file to open.
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
            # *args: 2 items (expected,, not enforced)
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
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())
                for Count in range(1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                self.__GridSize = int(f.readline().rstrip())
                for Count in range(1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
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