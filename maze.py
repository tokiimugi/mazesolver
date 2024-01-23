from cell import Cell
import random
import time

class Maze:
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win =None, seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_wall_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                col.append(Cell(self._win))
            self._cells.append(col)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i,j)
        


    def _draw_cell(self,i,j):
        if self._win is None:
            return
        self._cells[i][j].draw(self._x1 + self._cell_size_x * i, self._y1 + self._cell_size_y * j,self._x1 + self._cell_size_x * (i + 1), self._y1 + self._cell_size_y * (j+1))
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_wall(self,x1,y1,x2,y2):
        if x1 != x2:
            if x1 > x2:
                x1,x2 = x2,x1
            self._cells[x1][y1].has_right_wall = False
            self._cells[x2][y2].has_left_wall = False
        else:
            if y1 > y2:
                y1,y2 = y2, y1
            self._cells[x1][y1].has_bottom_wall = False
            self._cells[x2][y2].has_top_wall = False

    def _break_wall_r(self,i,j):
        self._cells[i][j].visited = True
        while(True):
            next = []
            if i > 0 and self._cells[i-1][j].visited == False:
                next.append((i-1,j))
            if i < self._num_cols -1 and self._cells[i+1][j].visited == False:
                next.append((i+1,j))
            if j > 0 and self._cells[i][j-1].visited == False:
                next.append((i,j-1))
            if j < self._num_rows -1 and self._cells[i][j+1].visited == False:
                next.append((i,j+1))
            
            if len(next) == 0:
                self._draw_cell(i,j)
                return

            x,y = random.choice(next)
            self._break_wall(i,j,x,y)

            self._break_wall_r(x,y)
    
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
    

    def solve(self):
        self._solve_r(0,0)

    def _solve_r(self,i,j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self._num_cols -1 and j == self._num_rows -1:
            return True
        if i > 0 and self._cells[i-1][j].visited == False and current_cell.has_left_wall == False:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if (self._solve_r(i-1,j)):
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j],True)

        if i < self._num_cols -1 and self._cells[i+1][j].visited == False and current_cell.has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if (self._solve_r(i+1,j)):
                return True
            self._cells[i][j].draw_move(self._cells[i+1][j],True)

        if j > 0 and self._cells[i][j-1].visited == False and current_cell.has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if (self._solve_r(i,j-1)):
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1],True)
       
        if j < self._num_rows -1 and self._cells[i][j+1].visited == False and current_cell.has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if (self._solve_r(i,j+1)):
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1],True)
       
        return False