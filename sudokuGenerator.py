
import math, random, pygame

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:

    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = []
        for row_index in range(row_length):
            row = [0] * row_length
            self.board.append(row)
        self.box_length = int(math.sqrt(row_length))

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        found = False
        for value in self.board[row]:
            if value == num:
                found = True

        if found:
            return False
        else:
            return True

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        found = False

        for row in range(self.row_length):
            value = self.board[row][col]
            if value == num:
                found = True
                break

        if found:
            return False
        else:
            return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num):
            return False

        if not self.valid_in_col(col, num):
            return False
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        if not self.valid_in_box(row_start, col_start, num):
            return False

        return True

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        used_numbers = set()

        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                num = random.randint(1, 9)

                while num in used_numbers:
                    num = random.randint(1, 9)

                self.board[i][j] = num

                used_numbers.add(num)

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        # Remove cells randomly from the board
        removed_count = 0
        while removed_count < self.removed_cells:
            row_index = random.randint(0, self.row_length - 1)
            col_index = random.randint(0, self.row_length - 1)
            if self.board[row_index][col_index] != 0:
                self.board[row_index][col_index] = 0
                removed_count += 1


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

class Cell: #represents a single cell in a Sudoku board
    def __init__(self, value, row, col, screen): #constructor for the Cell class
        self.value = value
        self. row = row
        self.col = col
        self.screen = screen
        self.cell_size = 60 #540x540 pixel board
        self.sketched_value = 0
        self.x = col * self.cell_size
        self.y = row * self.cell_size
        self.selected = False #whether this cell is selected by the user

    def set_cell_value(self, value): #setter for this cell's value
        self.value = value

    def set_sketched_value(self, value): #setter for this cell's sketched value
        self.sketched_value = value

    def draw(self): #draws this cell
        main_font = pygame.font.Font(None, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.cell_size, self.cell_size)) #white cell
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.cell_size, self.cell_size), 2)  # a black border

        # If the cell is selected, the cell is outlined red
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.cell_size, self.cell_size), 3)

        # Display the value in the cell if it's not zero, otherwise show the sketched value
        if self.value != 0:
            num_text = main_font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(num_text, (self.x + self.cell_size // 3, self.y + self.cell_size // 4))
        elif self.sketched_value is not None:
            num_text = main_font.render(str(self.sketched_value), True, (128, 128, 128)) #gray
            self.screen.blit(num_text, (self.x + self.cell_size // 3, self.y + self.cell_size // 4))

class Board: #represents an entire Sudoku board
    def __init__(self, width, height, screen, difficulty): #constructor for the Board class; screen is a window from pygame; difficulty is a variable to indicate if the user selected easy, medium, or hard
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [] #2D list to hold all the Cell's objects
        self.selected_cell = None #keeps track of the currently selected cell
        self.cell_size = 60

    def draw(self): #draws an outline of the sudoku grid, with bold lines to delineate the 3x3 boxes; draws every cell on this board
        for row in range(10):  # Draw 9 vertical and 9 horizontal lines
            pygame.draw.line(self.screen, (0, 0, 0), (row * self.cell_size, 0),
                             (row * self.cell_size, self.height))
            pygame.draw.line(self.screen, (0, 0, 0), (0, row * self.cell_size),
                             (self.width, row * self.cell_size))
        for row in range(0, 10, 3): #the bold lines to differentiate the 3x3 grids
            pygame.draw.line(self.screen, (0, 0, 0), (row * self.cell_size, 0), (row * self.cell_size, self.height), 4)
        for col in range(0, 10, 3): #the bold lines to differentiate the 3x3 grids
            pygame.draw.line(self.screen, (0, 0, 0), (0, col * self.cell_size), (self.width, col * self.cell_size), 4)
        for row in range(9): #draws each individual cell on the board
            for col in range(9):
                self.cells[row][col].draw()

    def select(self, row, col):
        #Marks the cell at (row, col) in the board as the current selected cell.
	    #Once a cell has been selected, the user can edit its value or sketched value.
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, row, col):
        #If a tuple of (x,y) coordinates is within the displayed board,
        #this function returns a tuple of the (row, col) of the cell which was clicked.
        #Otherwise, this function returns None.
        if 0 <= row < 9 and 0 <= col < 9:
            selected_cell = self.cells[row][col]
            selected_cell.selected = True

    def clear(self):
        #Clears the value cell.
        #Note that the user can only remove the cell values and sketched values that are filled by themselves.
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.sketch_value = None

    def sketch(self, value):
        #Sets the sketched value of the current selected cell equal to the user entered value.
	    #It will be displayed at the top left corner of the cell using the draw() function.
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        #Sets the value of the current selected cell equal to the user entered value.
        #Called when the user presses the Enter key.
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.sketch_value = None

    def reset_to_original(self):
        #Resets all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                if cell.value != 0:
                    cell.sketch_value = None

    def is_full(self):
        #Returns a Boolean value indicating whether the board is full or not.
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return False
        return True

    def update_board(self):
        #Updates the underlying 2D board with the values in all cells.
        board_values = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                board_values[row][col] = self.cells[row][col].value
        return board_values

    def find_empty(self):
        #Finds an empty cell and returns its row and col as a tuple (x,y).
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return row, col
        return None

    def check_board(self): #Check whether the Sudoku board is solved correctly.
        for row in range(9): #checks each row for any duplicates
            if len(set(self.cells[row])) != 9:
                return False
        for col in range(9): #checks column for any duplicates
            column = [self.cells[row][col].value for row in range(9)]
            if len(set(column)) != 9:
                return False
        for row_start in range(0, 9, 3): #finally checks each 3x3 grid for any duplicates
            for col_start in range(0, 9, 3):
                box = []
                for row in range(row_start, row_start + 3):
                    for col in range(col_start, col_start + 3):
                        box.append(self.cells[row][col].value)
                if len(set(box)) != 9:
                    return False
        return True
