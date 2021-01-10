import heapq
import sys

class Board(object):
    # create a board from an n-by-n array of tiles,
    # where tiles[row][col] = tile at (row, col)
    def __init__(self, tiles):
        self.n = len(tiles)
        rows, cols = (self.n, self.n) 
        self.tilescopy = [[0 for i in range(cols)] for j in range(rows)] 
        self.hamming = 0
        self.manhattan = 0

        for i in range(self.n):
            for j in range(self.n):
                self.tilescopy[i][j] = int(tiles[i][j])
                if self.tilescopy[i][j] == 0:
                    self.zerorow = i
                    self.zerocol = j
                elif (self.n * i) + j + 1 != self.tilescopy[i][j]:
                    self.hamming += 1
                    targetrow = (self.tilescopy[i][j] - 1) // self.n
                    targetcol = (self.tilescopy[i][j] - 1) % self.n
                    self.manhattan += abs(i - targetrow)
                    self.manhattan += abs(j - targetcol)

    # tile at (row, col) or 0 if blank
    def tileAt(self, row, col): 
        if row < 0 or row > self.n - 1 or col < 0 or col > self.n - 1:
            print("Invalid dimensions for this board!")
        else:
            return self.tilescopy[row][col]

    # board size n
    def size(self):
        return self.n

    # number of tiles out of place
    def givehamming(self):
        return self.hamming

    # sum of Manhattan distances between tiles and goal
    def givemanhattan(self):
        return self.manhattan
    
    # is this board the goal board?
    def isGoal(self):
        return self.hamming == 0

    # does this board equal y?
    def equals(self, y):
        if y is None:
            return False
        if y.n != self.n:
            return False
        for i in range(self.n):
            for j in range(self.n):
                if self.tileAt(i, j) != y.tileAt(i, j):
                    return False
        return True

    # all neighboring boards
    def neighbors(self):
        neighborqueue = []
        if self.zerocol > 0:
            rows, cols = (self.n, self.n) 
            copy = [[0 for i in range(cols)] for j in range(rows)]
            for i in range(self.n):
                for j in range(self.n):
                    copy[i][j] = self.tilescopy[i][j]
            copy[self.zerorow][self.zerocol] = copy[self.zerorow][self.zerocol - 1]
            copy[self.zerorow][self.zerocol - 1] = 0
            neighborqueue.append(Board(copy))
        
        # check what adjacent sides of blank tile are in bounds
        if self.zerorow > 0:
            rows, cols = (self.n, self.n) 
            copy = [[0 for i in range(cols)] for j in range(rows)]
            for i in range(self.n):
                for j in range(self.n):
                    copy[i][j] = self.tilescopy[i][j]
            copy[self.zerorow][self.zerocol] = copy[self.zerorow - 1][self.zerocol]
            copy[self.zerorow - 1][self.zerocol] = 0
            neighborqueue.append(Board(copy))
        
        if self.zerocol + 1 < self.n:
            rows, cols = (self.n, self.n) 
            copy = [[0 for i in range(cols)] for j in range(rows)]
            for i in range(self.n):
                for j in range(self.n):
                    copy[i][j] = self.tilescopy[i][j]
            copy[self.zerorow][self.zerocol] = copy[self.zerorow][self.zerocol + 1]
            copy[self.zerorow][self.zerocol + 1] = 0
            neighborqueue.append(Board(copy))
        
        if self.zerorow + 1 < self.n:
            rows, cols = (self.n, self.n) 
            copy = [[0 for i in range(cols)] for j in range(rows)]
            for i in range(self.n):
                for j in range(self.n):
                    copy[i][j] = self.tilescopy[i][j]
            copy[self.zerorow][self.zerocol] = copy[self.zerorow + 1][self.zerocol]
            copy[self.zerorow + 1][self.zerocol] = 0
            neighborqueue.append(Board(copy))
        
        return neighborqueue

    # checks to see if the board is solvable
    def isSolvable(self):
        inversions = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.tileAt(i, j) == 0:
                    continue
                for k in range(i, self.n):
                    m = j + 1
                    if k != i:
                        m = 0
                    while m < self.n:
                        if self.tileAt(i, j) > self.tileAt(k, m) and self.tileAt(k, m) != 0:
                            inversions += 1
                        m += 1

        # determines solvability based on if n is even or odd and the number of
        # inversions

        if self.n % 2 == 0:
            if (self.zerorow + inversions) % 2 != 0:
                return True
        
        else: 
            if inversions % 2 == 0:
                return True
        
        return False

    # string representation of this board
    def toString(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.tileAt(i, j), end = " ")
            print()
            print()

class SearchNode(object):
    def __init__(self, board, parent, numMoves, algorithm):
        self.board = board
        self.parent = parent
        self.numMoves = numMoves
        self.algorithm = algorithm

    def __lt__(self, other):
        if self.algorithm == "A*" and other.algorithm == "A*":
            return self.board.givemanhattan() + self.numMoves < other.board.givemanhattan() + other.numMoves
        elif self.algorithm == "GreedyBest" and other.algorithm == "GreedyBest":
            return self.board.givemanhattan() < other.board.givemanhattan()
        else:
            return self.numMoves < other.numMoves
        
class Solver(object):
    def __init__(self, initialBoard, algorithm, iterations):
        
        if algorithm == "A*" or algorithm == "UniformCost" or algorithm == "GreedyBest":
            gametree = []
            heapq.heapify(gametree)
            current = SearchNode(initialBoard, None, 0, algorithm)
            heapq.heappush(gametree, current)
            counter = 0

            while True:
                current = heapq.heappop(gametree)
                if current.board.isGoal() == True:
                    break
                for board in current.board.neighbors():
                    if counter == 0 or board.equals(current.parent.board) == False:
                        temp = SearchNode(board, current, current.numMoves + 1, algorithm)
                        heapq.heappush(gametree, temp)
                
                counter += 1
                if counter == iterations:
                    break

        elif algorithm == "BFS" or "DFS":
            gametree = []
            current = SearchNode(initialBoard, None, 0, algorithm)
            gametree.append(current)
            counter = 0

            while True:
                if algorithm == "BFS":
                    current = gametree.pop(0)
                else:
                    current = gametree.pop(-1)
                if current.board.isGoal() == True:
                    break
                for board in current.board.neighbors():
                    if counter == 0 or board.equals(current.parent.board) == False:
                        temp = SearchNode(board, current, current.numMoves + 1, algorithm)
                        gametree.append(temp)

                counter += 1
                if counter == iterations:
                    break

            self.goalNode = current

        else:
            depth = 0
            counter = 0
            while True:
                gametree = []
                current = SearchNode(initialBoard, None, 0, algorithm)
                gametree.append(current)
                
                while True:
                    current = gametree.pop(-1)
                    if current.board.isGoal() == True:
                        break
                    if current.numMoves == depth:
                        continue
                    for board in current.board.neighbors():
                        if current.numMoves == 0 or board.equals(current.parent.board) == False:
                            temp = SearchNode(board, current, current.numMoves + 1, algorithm)
                            gametree.append(temp)

                    counter += 1
                    if counter == iterations:
                        break
                
                depth += 1
            
        self.goalNode = current

    def moves(self):
        return self.goalNode.numMoves

    def solution(self):
        solutionstack = []
        temp = self.goalNode
        while temp is not None:
            solutionstack.insert(0, temp.board)
            temp = temp.parent
        return solutionstack
        
# main method
# def main():
#     print("Welcome to 8 Board Solver!")
    
#     while True:
#         try:
#             n = int(input("Please enter board size\n"))
#         except ValueError:
#             print("Invalid entry! Please enter an integer")
#         else:
#             if n > 0:
#                 break
#             else:
#                 print("Invalid board size. Please enter a positive integer")

#     numTiles = n**2

#     rows, cols = (n, n) 
#     board = [[0 for i in range(cols)] for j in range(rows)] 
    
#     numbers = []
#     for i in range(numTiles):
#         numbers.append(False)
    
#     print("Please enter all integer values for each tile. Enter 0 for blank tile")
#     for i in range(n):
#         for j in range(n):
#             while True:
#                 try:
#                     x = int(input())
#                 except ValueError:
#                     print("Invalid entry! Please enter an integer")
#                 else:
#                     if x >= 0 and x < numTiles and numbers[x] == False:
#                         board[i][j] = x
#                         numbers[x] = True
#                         print("Accepted. Please continue.")
#                         break
#                     else:
#                         print("Invalid input. Integers must be in the range of the number of available tiles and can not be repeated")

#     print("Please wait...")
    
#     board = Board(board)
#     if board.isSolvable() == False:
#         print("Sorry, board is not solvable!")
#         sys.exit()

#     print("""Please enter integer corresponding to your desired solving algorithm:
#     1 - A*
#     2 - Greedy Best
#     3 - Uniform Cost
#     4 - Iterative Deepening
#     5 - Breadth First Search (BFS)
#     6 - Depth First Search (DFS)""")

#     while True:
#         try:
#             choice = int(input())
#         except ValueError:
#             print("Invalid entry! Please enter an integer")
#         else:
#             if choice > 0 and choice < 7:
#                 break
#             else:
#                 print("Invalid entry. Please enter a listed integer")

#     if choice == 1:
#         algorithm = "A*"
#     elif choice == 2:
#         algorithm = "GreedyBest"
#     elif choice == 3:
#         algorithm = "UniformCost"
#     elif choice == 4:
#         algorithm = "IterativeDeepening"
#     elif choice == 5:
#         algorithm = "BFS"
#     elif choice == 6:
#         algorithm = "DFS"

#     while True:
#         try:
#             iterations = int(input("Enter iteration limit: "))
#         except ValueError:
#             print("Invalid entry! Please enter an integer")
#         else:
#             if iterations > 0:
#                 break
#             else:
#                 print("Invalid entry. Please enter a positive integer")

#     solution = Solver(board, algorithm, iterations)
#     print("Board Solved!")

#     boardTree = solution.solution()

#     counter = 0
#     for board in boardTree:
#         print("Move " + str(counter) + ":")
#         print()
#         board.toString()
#         print("----------")
#         counter += 1

#     if solution.goalNode.board.isGoal():
#         print("Board Successfully Solved!")
#     else:
#         print("Iteration limit reached. Board was not solved")

# main()
