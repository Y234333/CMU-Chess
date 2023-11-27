import math

from cmu_graphics import *

#################################################################### 
## EACH PIECE CLASS IS BELOW ##
####################################################################

class ChessPiece:
    def __init__(self, color, piece_type, position):
        self.color = color
        self.piece_type = piece_type
        self.position = position

    def get_color(self):
        return self.color

    def get_piece_type(self):
        return self.piece_type
        
    def get_position(self):
        return self.position
    
    def __str__(self):
        return f"""{self.piece_type}('{self.color}', {self.position})"""

    def __repr__(self):
        return self.__str__()
    
    def set_position(self, position):
        self.position = position

    def can_move(self, new_position):
        pass
    
    def get_valid_moves(self, pieces):
        pass
    
    # def getValidMoves(self, all_positions):
    #     pass


class Pawn(ChessPiece):
    def __init__(self, color, position):
        # self.name = name
        super().__init__(color, 'pawn', position)

    def can_move(self, new_position, all_positions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position

        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False

        if start_x == end_x and start_y == end_y:
            return False

        if new_position in all_positions:
            return False

        if self.get_color() == 'black':
            if start_y == 3 and end_y == start_y + 2 and end_x == start_x:
                self.set_position((end_x, end_y))
                return True
            if end_y == start_y + 1 and end_x == start_x:
                self.set_position((end_x, end_y))
                return True
        elif self.get_color() == 'white':
            if start_y == 8 and end_y == start_y - 2 and end_x == start_x:
                self.set_position((end_x, end_y))
                return True
            if end_y == start_y - 1 and end_x == start_x:
                self.set_position((end_x, end_y))
                return True

        return False
    
    def can_capture(self, new_position, pieces):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position

        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        if self.get_color() == 'white':
            if dx == 1 and dy == 1:
                for piece in pieces:
                    if piece.get_position() == new_position:
                        return True
        elif self.get_color() == 'black':
            if ((start_x == end_x + 1) and (start_y == end_y - 1)) or ((start_x == end_x - 1) and (start_y == end_y - 1)):
                for piece in pieces:
                    if piece.get_position() == new_position:
                        return True

        return False
    
    def can_moveHelper(self, new_position, whitePositions, blackPositions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position

        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False

        if start_x == end_x and start_y == end_y:
            return False

        if self.get_color() == 'black':
            if start_y == 3 and end_y == start_y + 2 and end_x == start_x and new_position not in (blackPositions and whitePositions):
                return True
            if end_y == start_y + 1 and end_x == start_x and new_position not in (blackPositions and whitePositions):
                return True
        elif self.get_color() == 'white':
            if start_y == 8 and end_y == start_y - 2 and end_x == start_x and new_position not in (blackPositions and whitePositions):
                return True
            if end_y == start_y - 1 and end_x == start_x and new_position not in (blackPositions and whitePositions):
                return True

        return False
    
    def can_captureHelper(self, new_position, whitePositions, blackPositions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position

        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        if self.get_color() == 'white':
            if dx == 1 and dy == 1 and new_position not in whitePositions:
                return True
        elif self.get_color() == 'black':
            if (((start_x == end_x + 1) and (start_y == end_y - 1)) or ((start_x == end_x - 1) and (start_y == end_y - 1))) and new_position not in blackPositions:
                return True

        return False    

    def get_valid_moves(self, pieces, all_positions, whitePositions, blackPositions):
        valid_moves = []
        moves = [
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
        (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
        (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)
        ]
        
        for move in moves:
            if self.can_moveHelper(move, whitePositions, blackPositions):
                valid_moves.append(move)
            elif self.can_captureHelper(move, whitePositions, blackPositions):
                for piece in pieces:
                    if piece.get_position() == move:
                        valid_moves.append(move)
                        break

        return valid_moves[:-2] if len(valid_moves) > 2 else valid_moves

class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, 'knight', position)
    
    def can_move(self, new_position, all_positions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if start_x == end_x and start_y == end_y:
            return False

        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if ((end_x == start_x + 1) or (end_x == start_x - 1)) and ((end_y == start_y + 2) or (end_y == start_y -2)):
            self.set_position((end_x, end_y))
            return True
        elif ((end_y == start_y + 1) or (end_y == start_y - 1)) and ((end_x == start_x + 2) or (end_x == start_x - 2)):
            self.set_position((end_x, end_y))
            return True
        else:
            return False
        
        
    def can_moveHelper(self, new_position, whitePositions, blackPositions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if start_x == end_x and start_y == end_y:
            return False

        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if (((end_x == start_x + 1) or (end_x == start_x - 1)) and ((end_y == start_y + 2) or (end_y == start_y -2))):
            if self.get_color() == 'white' and new_position not in whitePositions:
                return True
            elif self.get_color() == 'black' and new_position not in blackPositions:
                return True
        elif ((end_y == start_y + 1) or (end_y == start_y - 1)) and ((end_x == start_x + 2) or (end_x == start_x - 2)):
            if self.get_color() == 'white' and new_position not in whitePositions:
                return True
            elif self.get_color() == 'black' and new_position not in blackPositions:
                return True
        else:
            return False        
   
    def get_valid_moves(self, pieces, all_positions, whitePositions, blackPositions):
        valid_moves = []
        moves = [
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
        (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
        (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)
        ]
        
        for move in moves:
            if self.can_moveHelper(move, whitePositions, blackPositions):
                valid_moves.append(move)
        
        return valid_moves
        
class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, 'queen', position)
    
    def can_move(self, new_position, all_positions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if start_x == end_x and start_y == end_y:
            return False
        
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        
        if dx == dy or start_x == end_x or start_y == end_y:
            if dx == dy:
                step_x = 1 if end_x > start_x else -1
                step_y = 1 if end_y > start_y else -1
                for i in range(1, dx):
                    if (start_x + i * step_x, start_y + i * step_y) in all_positions:
                        return False
            elif start_x == end_x:
                step_y = 1 if end_y > start_y else -1
                for i in range(1, dy):
                    if (start_x, start_y + i * step_y) in all_positions:
                        return False
            else: 
                step_x = 1 if end_x > start_x else -1
                for i in range(1, dx):
                    if (start_x + i * step_x, start_y) in all_positions:
                        return False
            
            self.set_position((end_x, end_y))
            return True
        else:
            return False

    def can_moveHelper(self, new_position, all_positions, whitePositions, blackPositions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if start_x == end_x and start_y == end_y:
            return False
        
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        
        if dx == dy or start_x == end_x or start_y == end_y:
            if dx == dy:
                step_x = 1 if end_x > start_x else -1
                step_y = 1 if end_y > start_y else -1
                for i in range(1, dx):
                    if (start_x + i * step_x, start_y + i * step_y) in all_positions:
                        return False
            elif start_x == end_x:
                step_y = 1 if end_y > start_y else -1
                for i in range(1, dy):
                    if (start_x, start_y + i * step_y) in all_positions:
                        return False
            else: 
                step_x = 1 if end_x > start_x else -1
                for i in range(1, dx):
                    if (start_x + i * step_x, start_y) in all_positions:
                        return False
        
            if self.get_color() == 'white':
                if new_position in whitePositions:
                    return False
            elif self.get_color() == 'black':
                if new_position in blackPositions:
                    return False
        
            return True
        else:
            return False

    def get_valid_moves(self, pieces, all_positions, whitePositions, blackPositions):
        valid_moves = []
        moves = [
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
        (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
        (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)
        ]
        
        for move in moves:
            if self.can_moveHelper(move, all_positions, whitePositions, blackPositions):
                valid_moves.append(move) 
        return valid_moves

class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, 'king', position)
    
    def can_move(self, new_position, all_positions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        if start_x == end_x and start_y == end_y:
            return False

        if dx <= 1 and dy <= 1:
            self.set_position((end_x, end_y))
            return True
        else:
            return False
     
    def can_moveHelper(self, new_position, whitePositions, blackPositions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        if start_x == end_x and start_y == end_y:
            return False

        if dx <= 1 and dy <= 1:
            if self.get_color() == 'white' and new_position not in whitePositions:
                return True
            elif self.get_color() == 'black' and new_position not in blackPositions:
                return True
        else:
            return False
        
    def get_valid_moves(self, pieces, all_positions, whitePositions, blackPositions):
        valid_moves = []
        moves = [
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
        (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
        (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)
        ]
        
        for move in moves:
            if self.can_moveHelper(move, whitePositions, blackPositions):
                valid_moves.append(move)
        
        return valid_moves

class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, 'bishop', position)
    
    def can_move(self, new_position, all_positions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if start_x == end_x and start_y == end_y:
            return False
        
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        if dx == dy:
            step_x = 1 if end_x > start_x else -1
            step_y = 1 if end_y > start_y else -1
            for i in range(1, dx):
                if (start_x + i * step_x, start_y + i * step_y) in all_positions:
                    return False
            
            self.set_position((end_x, end_y))
            return True
        else:
            return False
        
    def can_moveHelper(self, new_position, all_positions, whitePositions, blackPositions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if start_x == end_x and start_y == end_y:
            return False
        
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        if dx == dy:
            step_x = 1 if end_x > start_x else -1
            step_y = 1 if end_y > start_y else -1
            for i in range(1, dx):
                if (start_x + i * step_x, start_y + i * step_y) in all_positions:
                    return False
            
            if self.get_color() == 'white' and new_position not in whitePositions:
                return True
            elif self.get_color() == 'black' and new_position not in blackPositions:
                return True
        else:
            return False
        
    def get_valid_moves(self, pieces, all_positions, whitePositions, blackPositions):
        valid_moves = []
        moves = [
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
        (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
        (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)
        ]
        
        for move in moves:
            if self.can_moveHelper(move, all_positions, whitePositions, blackPositions):
                valid_moves.append(move)
        
        return valid_moves

class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, 'rook', position)
    
    def can_move(self, new_position, all_positions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if start_x == end_x and start_y == end_y:
            return False
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if end_x == start_x and start_y != end_y:
            step = 1 if end_y > start_y else -1
            for y in range(start_y + step, end_y, step):
                if (end_x, y) in all_positions:
                    return False
            self.set_position((end_x, end_y))
            return True

        elif end_y == start_y and start_x != end_x:
            step = 1 if end_x > start_x else -1
            for x in range(start_x + step, end_x, step):
                if (x, end_y) in all_positions:
                    return False
            self.set_position((end_x, end_y))
            return True

        else:
            return False
        
        
    def can_moveHelper(self, new_position, all_positions, whitePositions, blackPositions):
        start_x, start_y = self.get_position()
        end_x, end_y = new_position
        
        if start_x == end_x and start_y == end_y:
            return False
        
        if end_x <= 1 or end_x >= 10 or end_y <= 1 or end_y >= 10:
            return False
        
        if end_x == start_x and start_y != end_y:
            step = 1 if end_y > start_y else -1
            for y in range(start_y + step, end_y, step):
                if (end_x, y) in all_positions:
                    return False
            if self.get_color() == 'white' and new_position not in whitePositions:
                return True
            elif self.get_color() == 'black' and new_position not in blackPositions:
                return True

        elif end_y == start_y and start_x != end_x:
            step = 1 if end_x > start_x else -1
            for x in range(start_x + step, end_x, step):
                if (x, end_y) in all_positions:
                    return False
            if self.get_color() == 'white' and new_position not in whitePositions:
                return True
            elif self.get_color() == 'black' and new_position not in blackPositions:
                return True

        else:
            return False

    def get_valid_moves(self, pieces, all_positions, whitePositions, blackPositions):
        valid_moves = []
        moves = [
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
        (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
        (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)
        ]
        
        for move in moves:
            if self.can_moveHelper(move, all_positions, whitePositions, blackPositions):
                valid_moves.append(move)
        
        return valid_moves

