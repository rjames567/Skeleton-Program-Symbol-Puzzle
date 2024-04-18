# Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9.4 programming environment

import random
import os


def Main():
	Again = "y"
	Score = 0
	while Again == "y":
		Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
		if len(Filename) > 0:
			MyPuzzle = Puzzle(Filename + ".txt")
		else:
			MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
		Score = MyPuzzle.AttemptPuzzle()
		print("Puzzle finished. Your score was: " + str(Score))
		Again = input("Do another puzzle? ").lower()


class Puzzle():
	def __init__(self, *args):
		if len(args) == 1:
			self.__Score = 0
			self.__SymbolsLeft = 0
			self.__GridSize = 0
			self.__Grid = []
			self.__AllowedPatterns = []
			self.__AllowedSymbols = []
			self.__LoadPuzzle(args[0])
		else:
			self.__Score = 0
			self.__SymbolsLeft = args[1]
			self.__GridSize = args[0]
			self.__Grid = []
			for Count in range(1, self.__GridSize * self.__GridSize + 1):
				if random.randrange(1, 101) < 90:
					C = Cell()
				else:
					C = BlockedCell()
				self.__Grid.append(C)
			self.__AllowedPatterns = []
			self.__AllowedSymbols = []
			QPattern = Pattern("Q", "QQ**Q**QQ")
			self.__AllowedPatterns.append(QPattern)
			self.__AllowedSymbols.append("Q")
			XPattern = Pattern("X", "X*X*X*X*X")
			self.__AllowedPatterns.append(XPattern)
			self.__AllowedSymbols.append("X")
			TPattern = Pattern("T", "TTT**T**T")
			self.__AllowedPatterns.append(TPattern)
			self.__AllowedSymbols.append("T")

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
		self._WildCardsRemaining = 2
		while not Finished:
			self.DisplayPuzzle()
			print("Current score: " + str(self.__Score))
			print("Remaining wildcards: " + str(self._WildCardsRemaining))
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
					Cells = [
						self.__GetCell(StartRow, StartColumn),
						self.__GetCell(StartRow, StartColumn + 1),
						self.__GetCell(StartRow, StartColumn + 2),
						self.__GetCell(StartRow - 1, StartColumn + 2),
						self.__GetCell(StartRow - 2, StartColumn + 2),
						self.__GetCell(StartRow - 2, StartColumn + 1),
						self.__GetCell(StartRow - 2, StartColumn),
						self.__GetCell(StartRow - 1, StartColumn),
						self.__GetCell(StartRow - 1, StartColumn + 1)
					]
					PatternString = "".join(i.GetSymbol() for i in Cells)
					for P in self.__AllowedPatterns:
						Cell = self.__GetCell(Row, Column)
						CurrentSymbol = Cell.GetSymbol()
						if Cell.GetInPattern():
							print("In pattern")
							print(Row, Column)
							
							self._WildCardsRemaining -= 1
							location = self.__Grid.index(Cell)
							CurrentSymbol = "W"
							self.__Grid[location] = WildCardCell()
							Score = 15
							print(P.MatchesPattern(PatternString, CurrentSymbol))
							print("One wildcard used this turn.", end=" ")
							if self._WildCardsRemaining == 0:
								print("No more remaining.")
						else:
							Score = 0

						# print(CurrentSymbol)
						if P.MatchesPattern(PatternString, CurrentSymbol):
							print("hit")
							if Score == 0:
								Score = 10
							for i in Cells:
								i.AddToNotAllowedSymbols(CurrentSymbol)
							return Score
						return 0
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
		if SymbolPlaced == "W":
			SymbolPlaced = self.__Symbol
		PatternString = PatternString.replace("W", self.__Symbol)
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
		self._InPattern = False

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
		self._InPattern = True if self._Symbol != "" else False # Only added when in a pattern
		self.__SymbolsNotAllowed.append(SymbolToAdd)

	def UpdateCell(self):
		pass

	def IsWildCard(self):
		return self._Symbol == "W"

	def GetInPattern(self):
		return self._InPattern


class BlockedCell(Cell):
	def __init__(self):
		super(BlockedCell, self).__init__()
		self._Symbol = "@"

	def CheckSymbolAllowed(self, SymbolToCheck):
		return False

class WildCardCell(Cell):
	def __init__(self):
		super().__init__()
		self._Symbol = "W"

if __name__ == "__main__":
	# Pattern.MatchesPattern(Pattern.GetPatternSequence(), "W")
	Main()