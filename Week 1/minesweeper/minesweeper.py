import itertools
from pickle import EMPTY_SET
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return None
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return None


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge.copy():
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge.copy():
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
               
            The function should add a new sentence to the AIs knowledge base, based on the value of cell and count, 
            to indicate that count of the cells neighbors are mines. Be sure to only include cells whose state is still undetermined in the sentence.
            
            If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.
            
            If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background), 
            then those sentences should be added to the knowledge base as well. Note that any time that you make any change to your AIs knowledge, 
            it may be possible to draw new inferences that werent possible before. 
            Be sure that those new inferences are added to the knowledge base if it is possible to do so.
        """
        
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # mark the cell as safe
        self.safes.add(cell)
        
        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        newSentence = self.add_new_sentence(cell, count)
        if newSentence is None or newSentence.cells is EMPTY_SET:
            return
        self.verify_if_safe_or_mine(newSentence)
        
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                
        self.add_inferred()
        
        return
        
    def add_inferred(self):
        # Compare each sentence, with each other
        for sentence in self.knowledge:
            sentenceCellCount = len(sentence.cells)
            otherSentences = self.knowledge.copy()
            otherSentences.remove(sentence) 
            for otherSentence in otherSentences:
                otherSentenceCellCount = len(otherSentence.cells)
                if not sentence.cells.issuperset(otherSentence.cells) or sentenceCellCount - otherSentenceCellCount < 1:
                    continue
                sentence.cells -= otherSentence.cells
                sentence.count -= otherSentence.count
                self.verify_if_safe_or_mine(sentence)
                
            self.verify_if_safe_or_mine(sentence)

                
    
    def verify_if_safe_or_mine(self, sentence):
        for cell in sentence.cells.copy():
            if cell in self.moves_made or cell in self.safes:
                self.mark_safe(cell)
            if cell in self.mines:
                self.mark_mine(cell)
        
        if sentence.known_safes():
            for sentenceCell in sentence.cells.copy():
                self.mark_safe(sentenceCell)
        elif sentence.known_mines():
            for sentenceCell in sentence.cells.copy():
                self.mark_mine(sentenceCell)
                
        if len(sentence.cells) == 0 and sentence in self.knowledge:
            self.knowledge.remove(sentence)
        
            
                
    def add_new_sentence(self, cell, count):
        cellAsList = list(cell)
        newCells = set()
        for i in range(3):
            for j in range(3):
                firstCoordinate = cellAsList[0] - 1 + i
                if firstCoordinate < 0 or firstCoordinate >= self.height:
                    continue
                
                secondCoordinate = cellAsList[1] - 1 + j
                if secondCoordinate < 0 or secondCoordinate >= self.width:
                    continue
                
                newCell = (firstCoordinate, secondCoordinate)
                if newCell not in self.moves_made:
                    newCells.add(newCell)
                
        newSentence = Sentence(newCells, count)
        if newSentence not in self.knowledge:
            self.knowledge.append(newSentence)
        return newSentence
    
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possibleMoves = self.safes - self.moves_made
        
        if len(possibleMoves) <= 0:
            return None
        safeCell = possibleMoves.pop()    
        self.moves_made.add(safeCell)
        print(f"safe cell: {safeCell}")
        return safeCell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for row in range(self.height):
            for column in range(self.width): 
                cell = (row,column)
                if cell in self.moves_made:
                    continue
                elif cell in self.mines:
                    continue
                print(f"random cell: {cell}")
                return cell
        return None        
