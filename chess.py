from cmu_graphics import *
from achessPieces import ChessPiece, Pawn, Rook, Knight, Queen, King, Bishop
import random

# from network import Network as network

import time
from time import perf_counter
from datetime import timedelta

#################################################################### 
## BASIC INITIALIZATION ##
####################################################################

def moreVariables(app):
    app.capturedPieces = [] 
    app.validMoves = []
    app.validMovesWhite = {}
    app.validMovesBlack = {}
    
    app.returnbutton = False
    
    app.counter = 0
    
    app.gameState = 'start'
    app.previousState = ''
    
    app.currentPlayer = 'white'
    
    app.counter = 0
    
    app.stage = 0
    
    app.funMode = random.choice([1,2,3,4])
    app.initialized = False
    app.winner = ''
    
    app.hillPosition = ()

def onAppStart(app):
    app.width, app.height = 600, 600
    
    app.blackPieces = \
    [
        Pawn('black', (2, 3)), Pawn('black', (3, 3)),
        Pawn('black', (4, 3)), Pawn('black', (5, 3)),
        Pawn('black', (6, 3)), Pawn('black', (7, 3)),
        Pawn('black', (8, 3)), Pawn('black', (9, 3)),
        Rook('black', (2, 2)), Knight('black', (3, 2)),
        Bishop('black', (4, 2)), Queen('black', (5, 2)),
        King('black', (6, 2)), Bishop('black', (7, 2)),
        Knight('black', (8, 2)), Rook('black', (9, 2))
    ]
    app.whitePieces = \
    [ 
        Pawn('white', (2, 8)), Pawn('white', (3, 8)),
        Pawn('white', (4, 8)), Pawn('white', (5, 8)),
        Pawn('white', (6, 8)), Pawn('white', (7, 8)),
        Pawn('white', (8, 8)), Pawn('white', (9, 8)), 
        Rook('white', (2, 9)), Knight('white', (3, 9)),
        Bishop('white', (4, 9)), Queen('white', (5, 9)),
        King('white', (6, 9)), Bishop('white', (7, 9)),
        Knight('white', (8, 9)), Rook('white', (9, 9))
    ]
    
    app.pieceImages = {
    'black': {
        'pawn': 'Picture/blackpawn-removebg-preview (1).png',
        'rook': 'Picture/blackrook-removebg-preview.png',
        'bishop': 'Picture/blackbishop-removebg-preview.png',
        'queen': 'Picture/blackqueen-removebg-preview.png',
        'king': 'Picture/blackking-removebg-preview.png',
        'knight': 'Picture/blackhorse-removebg-preview.png'
    },
    'white': {
        'pawn': 'Picture/white_pawn-removebg-preview.png',
        'rook': 'Picture/whiterook-removebg-preview.png',
        'bishop': 'Picture/whitebishop-removebg-preview.png',
        'queen': 'Picture/whitequeen-removebg-preview.png',
        'king': 'Picture/whiteking-removebg-preview.png',
        'knight': 'Picture/whitehorse-removebg-preview.png'
    }
    }
    
    app.pieceList = [Pawn, Queen, King, Knight, Rook, Bishop]
    app.piecesInfo = []
    for piece in app.blackPieces + app.whitePieces:
        piece_x = 50 * piece.get_position()[0]
        piece_y = 50 * piece.get_position()[1]
        app.piecesInfo.append({"piece": piece, "x": piece_x, "y": piece_y, "width": 50, "height": 50})
    app.selectedPiece = None
    
    moreVariables(app)
    
    app.turn = 1
    
    app.whiteCheck = False
    app.blackCheck = False
    
    app.checkMate = False
    
    # app.net = network()
    
def onStep(app):
    app.counter += 1

#################################################################### 
## MORE INTIALIZATION (HELPER FUNCTIONS MOSTLY) ##
####################################################################

def currentPositions(blackPieces, whitePieces):
    black_positions = [(x, y) for x, y in (piece.get_position() for piece in blackPieces)]
    white_positions = [(x, y) for x, y in (piece.get_position() for piece in whitePieces)]
    allPositions = black_positions + white_positions
    return allPositions

def moveHelperFunction(app, newPosition):
        (cell_x, cell_y) = newPosition
        app.selectedPiece['x'] = cell_x * 50
        app.selectedPiece['y'] = cell_y * 50   
        for piece in app.blackPieces + app.whitePieces:
            if piece == app.selectedPiece['piece']:
                piece.set_position(newPosition)
                break
        app.selectedPiece = None
        return True

def selectedPiece(app,newPosition):
    for piece_info in app.piecesInfo:
        if piece_info is not None and 'piece' in piece_info:
            if piece_info['piece'].get_position() == newPosition and piece_info['piece'].get_color() == app.currentPlayer:
                app.selectedPiece = piece_info
                return

def gameStateSelector(app, x,y): 
    if app.gameState == 'multi' or app.gameState == 'single':
        if x>0 and x<100 and y>550 and y<600:
            app.gameState = app.previousState
    
    if app.gameState == 'start':
        if x>99 and x<505 and y>148 and y<254:
            app.gameState = 'single'
        elif x>101 and x<505 and y>300 and y<404:
            app.gameState = 'multi'
        elif x>99 and x<505 and y>440 and y<555:
            app.gameState = 'tutorial'
        app.previousState = 'start'
    elif app.gameState == 'multi':
        if x>99 and x<505 and y>148 and y<254:
            app.gameState = 'normal'
        elif x>101 and x<505 and y>300 and y<404:
            app.gameState = 'fun'
            app.funMode = random.choice([1,2,3,4])
        elif x>99 and x<505 and y>440 and y<555:
            app.gameState = 'normal2'
        app.previousState = 'multi'
    elif app.gameState == 'single':
        if x>99 and x<505 and y>148 and y<254:
            app.gameState = 'easy'
        elif x>101 and x<505 and y>300 and y<404:
            app.gameState = 'med'
        elif x>99 and x<505 and y>440 and y<555:
            app.gameState = 'hard'
        app.previousState = 'single'
    elif app.gameState == 'tutorial' and app.stage > 8:
        app.gameState = 'start'
        app.stage = 0
    
    # drawRect(100,450,405,105,fill='darkred')
    # drawRect(100,450,400,100,fill='red')
    # drawLabel('Hard', 300,500, fill='black', size=30)
    
    if app.winner or app.checkMate:
        app.initialized = False
        app.returnbutton = True
        app.winner = ''
        
    if app.returnbutton == True:
        if x>125 and x<425 and y>510 and y<575:
            app.gameState = 'start'
            app.returnbutton = False
        
    # drawRect(125,520,300,50,fill='blue')
    # drawLabel('Return Back', 290, 540, fill='black', size=20)

def removePiece(app, capturedPiece, newPosition, piece_info):
    moveHelperFunction(app, newPosition)
    app.capturedPieces.append(capturedPiece)
    app.piecesInfo.remove(piece_info)
    if capturedPiece in app.blackPieces:
        app.blackPieces.remove(capturedPiece)
    elif capturedPiece in app.whitePieces:
        app.whitePieces.remove(capturedPiece)

def getCapturedPiece(app, newPosition, piece):
    capturedPiece = None
    for piece_info in app.piecesInfo:
        if piece_info is not None and 'piece' in piece_info:
            if piece_info['piece'].get_position() == newPosition:
                if piece_info['piece'].get_color() == piece.get_color():
                    return False
                elif piece_info['piece'].get_color() != piece.get_color():
                    capturedPiece = piece_info['piece']
                    break
    if capturedPiece:
        removePiece(app, capturedPiece, newPosition, piece_info)

def promotion(app):
    for i in range(len(app.piecesInfo)):
        piece_info = app.piecesInfo[i]
        piece = piece_info["piece"]
        if piece.get_piece_type() == "pawn":
            _, y = piece.get_position()
            if piece.get_color() == "white" and y == 2:
                # Replace the pawn with a new queen
                new_queen = Queen('white', (piece.get_position()))
                app.piecesInfo[i] = {"piece": new_queen, "x": piece_info["x"], "y": piece_info["y"], "width": 50, "height": 50}
                # Add the new queen to the list of white pieces
                app.whitePieces.append(new_queen)
                # Remove the promoted pawn from the list of white pieces
                app.whitePieces.remove(piece)
            elif piece.get_color() == "black" and y == 9:
                # Replace the pawn with a new queen
                new_queen = Queen('black', (piece.get_position()))
                app.piecesInfo[i] = {"piece": new_queen, "x": piece_info["x"], "y": piece_info["y"], "width": 50, "height": 50}
                # Add the new queen to the list of black pieces
                app.blackPieces.append(new_queen)
                # Remove the promoted pawn from the list of black pieces
                app.blackPieces.remove(piece)
            
def onMousePress(app, x, y):
    gameStateSelector(app, x,y)
    if app.gameState == 'tutorial':
        skipbuttons(app,x,y)
        customPlaces(app)
        if app.stage >= 8:
            app.winner = 'b'
    if app.gameState == 'fun':
        if app.funMode == 1:
            onMousePress1(app, x, y)
        elif app.funMode == 2:
            onMousePress2(app,x,y)
        elif app.funMode == 3:
            onMousePress3(app,x,y)
        elif app.funMode == 4:
            onMousePress4(app,x,y)
    if app.gameState == 'easy': ##Random Moves (No logic)
        onMousePressSingle(app,x,y)
    if app.gameState == 'med': ##Moves Based on a Score Logic
        onMousePressSingle(app,x,y)
    if app.gameState == 'hard': ##Advanced Moves
        onMousePressSingle(app,x,y)
    if app.gameState == 'normal':
        normalOnMousePress(app,x,y)
    if app.gameState == 'normal2':
        pass
    else:
        pass

def returnNormalMode(app):
    app.blackPieces = \
    [
        Pawn('black', (2, 3)), Pawn('black', (3, 3)),
        Pawn('black', (4, 3)), Pawn('black', (5, 3)),
        Pawn('black', (6, 3)), Pawn('black', (7, 3)),
        Pawn('black', (8, 3)), Pawn('black', (9, 3)),
        Rook('black', (2, 2)), Knight('black', (3, 2)),
        Bishop('black', (4, 2)), Queen('black', (5, 2)),
        King('black', (6, 2)), Bishop('black', (7, 2)),
        Knight('black', (8, 2)), Rook('black', (9, 2))
    ]
    app.whitePieces = \
    [ 
        Pawn('white', (2, 8)), Pawn('white', (3, 8)),
        Pawn('white', (4, 8)), Pawn('white', (5, 8)),
        Pawn('white', (6, 8)), Pawn('white', (7, 8)),
        Pawn('white', (8, 8)), Pawn('white', (9, 8)), 
        Rook('white', (2, 9)), Knight('white', (3, 9)),
        Bishop('white', (4, 9)), Queen('white', (5, 9)),
        King('white', (6, 9)), Bishop('white', (7, 9)),
        Knight('white', (8, 9)), Rook('white', (9, 9))
    ]
    
    app.piecesInfo = []
    for piece in app.blackPieces + app.whitePieces:
        piece_x = 50 * piece.get_position()[0]
        piece_y = 50 * piece.get_position()[1]
        app.piecesInfo.append({"piece": piece, "x": piece_x, "y": piece_y, "width": 50, "height": 50})
    app.selectedPiece = None

#################################################################### 
## MULTIPLAYER IS BELOW ##
####################################################################
      
def normalOnMousePress(app,x,y):
    if app.initialized == False:
        returnNormalMode(app)
        app.initialized = True
    
    cellSize = 50
    cellx = 1 + (int((x - 0.5 * cellSize) // cellSize))
    celly = 1 + (int((y - 0.5 * cellSize) // cellSize))

    newPosition = (cellx, celly)
    if app.selectedPiece is None:
        selectedPiece(app, newPosition)

    else:
        for piece_info in app.piecesInfo:
            if piece_info is not None and 'piece' in piece_info:
                if piece_info['piece'].get_position() == newPosition and piece_info['piece'].get_color() == app.currentPlayer:
                    app.selectedPiece = piece_info
                    return
        
        if app.selectedPiece is not None and 'piece' in app.selectedPiece:
            piece = app.selectedPiece['piece']
            if piece is not None and piece.get_color() == app.currentPlayer:
                currentPosition = currentPositions(app.blackPieces, app.whitePieces)
                if newPosition in currentPosition:
                    if piece.get_piece_type() == 'pawn':
                        if piece.can_capture(newPosition, (app.blackPieces + app.whitePieces)):
                            capturedPiece = None
                            getCapturedPiece(app, newPosition, piece)
                            app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white' 
                            promotion(app)
                                            
                    else:
                        for piece_info in app.piecesInfo:
                            if piece_info is not None and 'piece' in piece_info:
                                if piece_info['piece'].get_position() == newPosition:
                                    if piece_info['piece'].get_color() == piece.get_color():
                                        return False
                                    elif piece_info['piece'].get_color() != piece.get_color():
                                        if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                            capturedPiece = piece_info['piece']
                                            removePiece(app, capturedPiece, newPosition, piece_info)
                                            app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'
                                            promotion(app)
                else:
                    if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                        old_position = piece.get_position()
                        piece.set_position(newPosition)

                        if not isCheck(app, piece.get_color()):
                            moveHelperFunction(app, newPosition)
                            app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'
                            promotion(app)
                        else:
                            piece.set_position(old_position)
    print('Mate:', isCheckMate(app))
    if isCheckMate(app):
        app.winner = 'white' if app.currentPlayer == 'black' else 'black'

def allValidMoves(app):
    valid_moves = {'black': [], 'white': []}

    for piece_info in app.piecesInfo:
        piece = piece_info['piece']
        piece_color = piece.get_color()

        piece_valid_moves = piece.get_valid_moves((app.blackPieces + app.whitePieces), currentPositions(app.blackPieces, app.whitePieces))

        # Extend the list of valid moves for the color, not append
        valid_moves[piece_color].extend(piece_valid_moves)

    return valid_moves

def isCheck(app, color):
    king = None
    for piece_info in app.piecesInfo:
        piece = piece_info['piece']
        if piece.get_color() == color and piece.get_piece_type() == 'king':
            king = piece

    moves = allValidMoves(app)
    opponent_color = 'black' if color == 'white' else 'white'

    if king.get_position() in moves[opponent_color]:
        return True

    return False

def checkIfCheck(app, color, position):
    moves = allValidMoves(app)
    opponent_color = 'black' if color == 'white' else 'white'

    if position in moves[opponent_color]:
        print('hi')
        return True
    
    ##IT WAS NEVER IN MOVES BECAUSE THERE IS A PIECE THERE WITH SAME COLOR U FUCKING IDIOT

    return False

def isCheckMate(app):
    blackKing = None
    whiteKing = None
    for piece_info in app.piecesInfo:
        piece = piece_info['piece']
        if piece.get_color() == 'black' and piece.get_piece_type() == 'king':
            blackKing = piece
        if piece.get_color() == 'white' and piece.get_piece_type() == 'king':
            whiteKing = piece

    moves = allValidMoves(app)

    if isCheck(app, 'black'):
        black_king_moves = blackKing.get_valid_moves((app.blackPieces + app.whitePieces), currentPositions(app.blackPieces, app.whitePieces))
        for move in black_king_moves:
            if not checkIfCheck(app, 'black', move):
                print('hi2')
                return False
            print('hi3')
        return True

    if isCheck(app, 'white'):
        white_king_moves = whiteKing.get_valid_moves((app.blackPieces + app.whitePieces), currentPositions(app.blackPieces, app.whitePieces))
        for move in white_king_moves:
            if not checkIfCheck(app, 'white', move):
                print('hi4')
                return False
            print('hi5')
        return True

    return False


#################################################################### 
## MUTLIPLAYER 2 DEVICE IS BELOW (NOT WORKING) ##
####################################################################

def normal2MousePress(app, x, y):
    if app.initialized == False:
        returnNormalMode(app)
        app.initialized = True
    
    
    cellSize = 50
    cellx = 1 + (int((x - 0.5 * cellSize) // cellSize))
    celly = 1 + (int((y - 0.5 * cellSize) // cellSize))

    newPosition = (cellx, celly)
    if app.selectedPiece is None:
        selectedPiece(app, newPosition)

#################################################################### 
## SINGLE PLAYER IS BELOW ##
####################################################################

def defaultMousePressIsh(app, newPosition):
    for piece_info in app.piecesInfo:
        if piece_info is not None and 'piece' in piece_info:
            if piece_info['piece'].get_position() == newPosition and piece_info['piece'].get_color() == app.currentPlayer:
                app.selectedPiece = piece_info
                return

    if app.selectedPiece is not None and 'piece' in app.selectedPiece:
        piece = app.selectedPiece['piece']
        if piece is not None and piece.get_color() == app.currentPlayer:
            currentPosition = currentPositions(app.blackPieces, app.whitePieces)
            if newPosition in currentPosition:
                if piece.get_piece_type() == 'pawn':
                    if piece.can_capture(newPosition, (app.blackPieces + app.whitePieces)):
                        capturedPiece = None
                        getCapturedPiece(app, newPosition, piece)
                        promotion(app)
                        app.currentPlayer = 'black' 
                                        
                else:
                    for piece_info in app.piecesInfo:
                        if piece_info is not None and 'piece' in piece_info:
                            if piece_info['piece'].get_position() == newPosition:
                                if piece_info['piece'].get_color() == piece.get_color():
                                    return False
                                elif piece_info['piece'].get_color() != piece.get_color():
                                    if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                        capturedPiece = piece_info['piece']
                                        removePiece(app, capturedPiece, newPosition, piece_info)
                                        promotion(app)
                                        app.currentPlayer = 'black' 
            else:
                if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                    moveHelperFunction(app, newPosition)
                    promotion(app)
                    app.currentPlayer = 'black'


def onMousePressSingle(app, x, y):
    if app.initialized == False:
        returnNormalMode(app)
        app.initialized = True
    
    if app.currentPlayer == 'black' and app.gameState == 'easy':
        EasySinglePlayer(app, x, y)
    elif app.currentPlayer == 'black' and app.gameState == 'hard':
        HardSinglePlayer(app, x, y)
    else:
        cellSize = 50
        cellx = 1 + (int((x - 0.5 * cellSize) // cellSize))
        celly = 1 + (int((y - 0.5 * cellSize) // cellSize))

        newPosition = (cellx, celly)
        if app.selectedPiece is None:
            selectedPiece(app, newPosition)

        else:
            defaultMousePressIsh(app, newPosition)
            
        
def allValidMovesBlack(app):
    valid_moves = {'pawn': [], 'rook': [], 'knight': [], 'bishop': [], 'queen': [], 'king': []}

    for piece_info in app.piecesInfo:
        piece = piece_info['piece']
        piece_color = piece.get_color()

        if piece_color == 'black':
            piece_type = piece.get_piece_type()
            piece_valid_moves = piece.get_valid_moves((app.blackPieces + app.whitePieces), currentPositions(app.blackPieces, app.whitePieces))

            # Extend the list of valid moves for the piece type
            valid_moves[piece_type].extend(piece_valid_moves)

    return valid_moves

## EASY

def EasySinglePlayer(app, x, y):
    if app.currentPlayer == 'black':
        
        moves = allValidMoves(app)
        moves2 = allValidMovesBlack(app)
        
        if moves['black']:
            move = random.choice(moves['black'])
            piece_type = None
            for key, value in moves2.items():
                if move in value:
                    piece_type = key
                    break

            for piece_info in app.piecesInfo:
                if piece_info['piece'].get_piece_type() == piece_type: 
                    for i in piece_info['piece'].get_valid_moves((app.blackPieces + app.whitePieces), currentPositions(app.blackPieces, app.whitePieces)):
                        if i == move:
                            app.selectedPiece = piece_info
                            break
            
            newPosition = move
            if app.selectedPiece is None:
                app.winner = 'white'
                return
                
            else:
                for piece_info in app.piecesInfo:
                    if piece_info is not None and 'piece' in piece_info:
                        if piece_info['piece'].get_position() == newPosition and piece_info['piece'].get_color() == app.currentPlayer:
                            app.selectedPiece = piece_info
                            return
                
                if app.selectedPiece is not None and 'piece' in app.selectedPiece:
                    piece = app.selectedPiece['piece']
                    if piece is not None and piece.get_color() == app.currentPlayer:
                        currentPosition = currentPositions(app.blackPieces, app.whitePieces)
                        if newPosition in currentPosition:
                            if piece.get_piece_type() == 'pawn':
                                if piece.can_capture(newPosition, (app.blackPieces + app.whitePieces)):
                                    capturedPiece = None
                                    getCapturedPiece(app, newPosition, piece)
                                    promotion(app)
                                    app.currentPlayer = 'white' 
                                                    
                            else:
                                for piece_info in app.piecesInfo:
                                    if piece_info is not None and 'piece' in piece_info:
                                        if piece_info['piece'].get_position() == newPosition:
                                            if piece_info['piece'].get_color() == piece.get_color():
                                                return False
                                            elif piece_info['piece'].get_color() != piece.get_color():
                                                if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                                    capturedPiece = piece_info['piece']
                                                    removePiece(app, capturedPiece, newPosition, piece_info)
                                                    promotion(app)
                                                    app.currentPlayer = 'white' 
                        else:
                            if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                moveHelperFunction(app, newPosition)
                                promotion(app)
                                app.currentPlayer = 'white'


## HARD



def HardSinglePlayer(app, x, y):
    if app.currentPlayer == 'black':
        
        score, best_move = minimax(app, app.piecesInfo, 3, float('-inf'), float('inf'), False)
        
        print(score, best_move)
        
        piece_info, move = best_move
        
        print(piece_info, move)
        
        app.selectedPiece = piece_info
        
        newPosition = move
        if app.selectedPiece is None:
            app.winner = 'white'
            return
                
        else:
            for piece_info in app.piecesInfo:
                if piece_info is not None and 'piece' in piece_info:
                    if piece_info['piece'].get_position() == newPosition and piece_info['piece'].get_color() == app.currentPlayer:
                        app.selectedPiece = piece_info
                        return
            
            if app.selectedPiece is not None and 'piece' in app.selectedPiece:
                piece = app.selectedPiece['piece']
                if piece is not None and piece.get_color() == app.currentPlayer:
                    currentPosition = currentPositions(app.blackPieces, app.whitePieces)
                    if newPosition in currentPosition:
                        if piece.get_piece_type() == 'pawn':
                            if piece.can_capture(newPosition, (app.blackPieces + app.whitePieces)):
                                capturedPiece = None
                                getCapturedPiece(app, newPosition, piece)
                                promotion(app)
                                app.currentPlayer = 'white' 
                                                
                        else:
                            for piece_info in app.piecesInfo:
                                if piece_info is not None and 'piece' in piece_info:
                                    if piece_info['piece'].get_position() == newPosition:
                                        if piece_info['piece'].get_color() == piece.get_color():
                                            return False
                                        elif piece_info['piece'].get_color() != piece.get_color():
                                            if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                                capturedPiece = piece_info['piece']
                                                removePiece(app, capturedPiece, newPosition, piece_info)
                                                promotion(app)
                                                app.currentPlayer = 'white' 
                    else:
                        if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                            moveHelperFunction(app, newPosition)
                            promotion(app)
                            app.currentPlayer = 'white'


def allValidMovesMiniMax(app):
    valid_moves = []

    for piece_info in app.piecesInfo:
        piece = piece_info['piece']
        piece_color = piece.get_color()

        if piece_color == 'black':
            piece_valid_moves = piece.get_valid_moves((app.blackPieces + app.whitePieces), currentPositions(app.blackPieces, app.whitePieces))

            # Extend the list of valid moves with the piece and move
            for move in piece_valid_moves:
                valid_moves.append((piece_info, move))

    return valid_moves

def gameOver(app):
    return True if app.gameState == 'gameOver' else False

## (Reference: https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/, 
# https://www.youtube.com/watch?v=t6JA78oRFMI&t=336s&ab_channel=nextProgram)

def minimax(app, position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or gameOver(app):
        return static_evaluation(app), position

    if maximizingPlayer:
        minEval = float('inf')
        best_move = None
        for child in allValidMovesMiniMax(app):
            piece_info, move = child
            # Save the current state of the piecesInfo
            original_state = app.piecesInfo.copy()

            # Make the move
            piece_index = app.piecesInfo.index(piece_info)
            app.piecesInfo[piece_index]['piece'].set_position(move)

            # Recursively call minimax
            eval, _ = minimax(app, position, depth - 1, alpha, beta, False)

            # Undo the move
            app.piecesInfo = original_state

            if eval < minEval:
                minEval = eval
                best_move = (piece_info, move)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move

    else:
        maxEval = float('-inf')
        best_move = None
        for child in allValidMovesMiniMax(app):
            piece_info, move = child
            # Save the current state of the piecesInfo
            original_state = app.piecesInfo.copy()

            # Make the move
            piece_index = app.piecesInfo.index(piece_info)
            app.piecesInfo[piece_index]['piece'].set_position(move)

            # Recursively call minimax
            eval, _ = minimax(app, position, depth - 1, alpha, beta, True)

            # Undo the move
            app.piecesInfo = original_state

            if eval > maxEval:
                maxEval = eval
                best_move = (piece_info, move)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move



def static_evaluation(app):
    piece_values = {
        'pawn': 1,
        'knight': 3,
        'bishop': 3,
        'rook': 5,
        'queen': 9,
        'king': 90
    }

    evaluation = 0
    for piece_info in app.piecesInfo:
        piece = piece_info['piece']
        if piece is not None:
            if piece.get_color() == 'white':
                evaluation -= piece_values[piece.get_piece_type()]
            elif piece.get_color() == 'black':
                evaluation += piece_values[piece.get_piece_type()]
    
    return evaluation


#################################################################### 
## GRAPHICS ARE BELOW ##
####################################################################

def goBack():
    drawRect(0,550,100,50,fill='lightblue')
    drawLabel('Go Back', 50, 575, size=20)

def drawStartScreen():
    drawRect(0,0,600,600,fill=rgb(48, 46, 43))
    drawLabel('Play Chess!', 300, 70,fill='white',size=60)
    
    ##
    
    drawRect(100,150,405,105,fill=rgb(69, 117, 60))
    drawRect(100,150,400,100,fill=rgb(129, 182, 76))
    drawLabel('SinglePlayer', 300,200, fill='white', size=30)
    
    drawRect(100,300,405,105,fill=rgb(51, 50, 48))
    drawRect(100,300,400,100,fill=rgb(64, 62, 60))
    drawLabel('MultiPlayer', 300,350, fill=rgb(196, 196, 195), size=30)
    
    drawRect(100,450,405,105,fill=rgb(69, 117, 60))
    drawRect(100,450,400,100,fill=rgb(129, 182, 76))
    drawLabel('Tutorial', 300,500, fill='white', size=30)

def drawSinglePlayer():
    text = 'Challenge the computer to a chess game!'
    
    drawRect(0,0,600,600,fill=rgb(48, 46, 43))
    drawLabel('SinglePlayer', 300, 70,fill='white',size=60)
    drawLabel(text, 300, 120,fill='white',size=20)
    
    ##
    
    drawRect(100,150,405,105,fill='darkgreen')
    drawRect(100,150,400,100,fill='green')
    drawLabel('Easy', 300,200, fill='black', size=30)
    
    drawRect(100,300,405,105,fill='yellow', opacity=80)
    drawRect(100,300,400,100,fill='yellow')
    drawLabel('Medium', 300,350, fill='black', size=30)
    
    drawRect(100,450,405,105,fill='darkred')
    drawRect(100,450,400,100,fill='red')
    drawLabel('Hard', 300,500, fill='black', size=30)
    
    goBack()
    
def drawMultiPlayer():
    text = 'Challenge your friend!'
    
    drawRect(0,0,600,600,fill=rgb(48, 46, 43))
    drawLabel('MultiPlayer', 300, 70,fill='white',size=60)
    drawLabel(text, 300, 120,fill='white',size=20)
    
    ##
    
    drawRect(100,150,405,105,fill='darkred')
    drawRect(100,150,400,100,fill='red')
    drawLabel('Normal Mode (1 device)', 300,200, fill='black', size=30)
    
    drawRect(100,300,405,105,fill='pink', opacity=80)
    drawRect(100,300,400,100,fill='pink')
    drawLabel('Fun Mode', 300,350, fill='black', size=30)
    
    drawRect(100,450,405,105,fill='darkred')
    drawRect(100,450,400,100,fill='red')
    drawLabel('Normal Mode (2 device)', 300,500, fill='black', size=30)
    
    goBack()

def drawGameState(app):
    if app.gameState != 'tutorial':
        if app.winner:
            drawLabel(app.winner + ' has won!', 300, 500, fill='white', size=20)
            drawReturnButton(app)
        else:
            drawLabel(app.currentPlayer + "'s turn", 300, 500, fill='white', size=20)

def drawReturnButton(app):
    drawRect(125,520,300,50,fill='blue')
    drawLabel('Return Back', 290, 540, fill='black', size=20)

def drawBoard(app):
    drawRect(0,0,600,600,fill=rgb(48, 46, 43))
    for i in range(64):
        column = i % 8
        row = i // 8
        if row % 2 == 0:
            if column % 2 == 0:
                drawRect(425 - (column * 50), 75 + row * 50, 50, 50, fill=rgb(119, 148, 85))
            else:
                drawRect(425 - (column * 50), 75 + row * 50, 50, 50, fill=rgb(235, 235, 208))
        else:
            if column % 2 == 0:
                drawRect(425 - (column * 50), 75 + row * 50, 50, 50, fill=rgb(235, 235, 208))
            else:
                drawRect(425 - (column * 50), 75 + row * 50, 50, 50, fill=rgb(119, 148, 85))
    
    drawGameState(app)

def drawPieces(app):
    for piece in app.piecesInfo:
        # color = 'black' if piece["piece"].get_color() == 'black' else 'white' ##LABELS NOT IMAGES
        # drawLabel(piece["piece"].get_piece_type(), piece["x"], piece["y"], fill=color)
    
        piece_type = piece["piece"].get_piece_type()
        color = piece["piece"].get_color()
        url = app.pieceImages[color][piece_type]
        drawImage(url, piece["x"]-20, piece["y"]-20)
        

        
def redrawAll(app):        
    drawBoard(app)
    drawPieces(app)
                
    # drawLabel(app.counter, 50, 50)
        
    if app.gameState == 'start': ## WORKS FULLY
        drawStartScreen()
    if app.gameState == 'single': ## WORKS FULLY (design wise)
        drawSinglePlayer()
        if app.gameState == 'easy': ## WORKS - Please keep clicking screen until it makes a move
            pass
    if app.gameState == 'multi': ## WORKS FULLY
        drawMultiPlayer() 
    if app.gameState == 'normal' or app.gameState == 'normal2': ## WORKS FULLY
        drawBoard(app)
        drawPieces(app)
    if app.gameState == 'tutorial': ## WORKS FULLY
        runTutorial(app)
    if app.gameState == 'fun': ##All work except promoted piece never dies!
        drawBoard(app)
        runFunMode(app)
        drawPieces(app)  

#################################################################### 
## FUN MODE IS BELOW ##
####################################################################

def runFunMode(app):
    if app.gameState == 'fun':
        if app.winner == '': 
            if app.funMode == 1:
                drawfunMode1()
            if app.funMode == 2:
                drawfunMode2()
            if app.funMode == 3:
                drawfunMode3()
            if app.funMode == 4:
                drawHillPosition(app)
                drawfunMode4()

def customPieces(app):
    if app.gameState == 'fun':
        if app.funMode == 1:
            pass
        if app.funMode == 2:
            customPieces2(app)
        if app.funMode == 3:
            customPieces3(app)
        if app.funMode == 4:
            pass


##FUN MODE 1 IS BELOW - INVINSIBLE PROMOTION CHARACTER (NEVER DIES)

def promotionFunMode(app):
    for i in range(len(app.piecesInfo)):
        piece_info = app.piecesInfo[i]
        piece = piece_info["piece"]
        if piece.get_piece_type() == "pawn":
            _, y = piece.get_position()
            if piece.get_color() == "white" and y == 2:
                # Replace the pawn with a new queen
                new_queen = Queen('white', (piece.get_position()))
                app.piecesInfo[i] = {"piece": new_queen, "x": piece_info["x"], "y": piece_info["y"], "width": 50, "height": 50}
            elif piece.get_color() == "black" and y == 9:
                # Replace the pawn with a new queen
                new_queen = Queen('black', (piece.get_position()))
                app.piecesInfo[i] = {"piece": new_queen, "x": piece_info["x"], "y": piece_info["y"], "width": 50, "height": 50}

def onMousePress1(app,x,y):
    pass

def drawfunMode1():
    drawLabel('A promoted piece will never die!', 300, 550, fill='white', size=20)

##ADD COMPELETE ONMOUSEPRESS AND CHANGE PROMOTION TO TO PROMOTIONFUNMODE


##FUN MODE 2 IS BELOW - ALL ROOKS (FREE FOR ALL - FIRST TO KILL ALL WINS)

def customPieces2(app):
    app.blackPieces =  [Rook('black', (x, 2)) for x in range(2, 10)] + [Rook('black', (x, 3)) for x in range(2, 10)]
    app.whitePieces =  [Rook('white', (x, 8)) for x in range(2, 10)] + [Rook('white', (x, 9)) for x in range(2, 10)]

    app.piecesInfo = []
    for piece in app.blackPieces + app.whitePieces:
        piece_x = 50 * piece.get_position()[0]
        piece_y = 50 * piece.get_position()[1]
        app.piecesInfo.append({"piece": piece, "x": piece_x, "y": piece_y, "width": 50, "height": 50})
    app.selectedPiece = None
        
def onMousePress2(app,x,y):
    if app.initialized == False and app.gameState == 'fun' and app.funMode == 2:
        returnNormalMode(app) 
        customPieces2(app)
        app.initialized = True
    
    cellSize = 50
    cellx = 1 + (int((x - 0.5 * cellSize) // cellSize))
    celly = 1 + (int((y - 0.5 * cellSize) // cellSize))

    newPosition = (cellx, celly)
    if app.selectedPiece is None:
        selectedPiece(app, newPosition)

    else:
        # Check if another piece is selected
        for pieceInfo in app.piecesInfo:
            if pieceInfo is not None and 'piece' in pieceInfo:
                if pieceInfo['piece'].get_position() == newPosition and pieceInfo['piece'].get_color() == app.currentPlayer:
                    app.selectedPiece = pieceInfo
                    return
        
        if app.selectedPiece is not None and 'piece' in app.selectedPiece:
            piece = app.selectedPiece['piece']
            if piece is not None and piece.get_color() == app.currentPlayer:
                currentPosition = currentPositions(app.blackPieces, app.whitePieces)
                if newPosition in currentPosition:
                    if piece.get_piece_type() == 'pawn':
                        if piece.can_capture(newPosition, (app.blackPieces + app.whitePieces)):
                            capturedPiece = None
                            getCapturedPiece(app, newPosition, piece)
                            app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white' 
                                            
                    else:
                        for pieceInfo in app.piecesInfo:
                            if pieceInfo is not None and 'piece' in pieceInfo:
                                if pieceInfo['piece'].get_position() == newPosition:
                                    if pieceInfo['piece'].get_color() == piece.get_color():
                                        return False
                                    elif pieceInfo['piece'].get_color() != piece.get_color():
                                        if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                            capturedPiece = pieceInfo['piece']
                                            removePiece(app, capturedPiece, newPosition, pieceInfo)
                                            app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'
                else:
                    if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                        moveHelperFunction(app, newPosition)
                        app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'

def allPiecesCaptured(pieces, color):
    for piece in pieces:
        if piece.get_color() == color:
            return False
    return True 

def checkWinnerFun(app):
    if allPiecesCaptured(app.whitePieces, 'white'):
        app.winner = 'Black'
        app.initialized = False
    if allPiecesCaptured(app.blackPieces, 'black'):
        app.winner = 'White'
        app.initialized = False
    return True if app.winner != '' else False

def drawfunMode2():
    drawLabel('FREE FOR ALL! KILL ALL TO WIN!!', 300, 550, fill='white', size=20)

##FUN MODE 3 IS BELOW - ALL QUEENS (FREE FOR ALL - FIRST TO KILL ALL WINS)

def customPieces3(app):
    app.blackPieces =  [Queen('black', (x, 2)) for x in range(2, 10)] + [Queen('black', (x, 3)) for x in range(2, 10)]
    app.whitePieces =  [Queen('white', (x, 8)) for x in range(2, 10)] + [Queen('white', (x, 9)) for x in range(2, 10)]

    app.piecesInfo = []
    for piece in app.blackPieces + app.whitePieces:
        piece_x = 50 * piece.get_position()[0]
        piece_y = 50 * piece.get_position()[1]
        app.piecesInfo.append({"piece": piece, "x": piece_x, "y": piece_y, "width": 50, "height": 50})
    app.selectedPiece = None
        
def onMousePress3(app,x,y):
    if app.initialized == False and app.gameState == 'fun' and app.funMode == 3:
        returnNormalMode(app) 
        customPieces3(app)
        app.initialized = True
    
    cellSize = 50
    cellx = 1 + (int((x - 0.5 * cellSize) // cellSize))
    celly = 1 + (int((y - 0.5 * cellSize) // cellSize))

    checkWinnerFun(app)

    newPosition = (cellx, celly)
    if app.selectedPiece is None:
        selectedPiece(app, newPosition)

    else:
        for piece_info in app.piecesInfo:
            if piece_info is not None and 'piece' in piece_info:
                if piece_info['piece'].get_position() == newPosition and piece_info['piece'].get_color() == app.currentPlayer:
                    app.selectedPiece = piece_info
                    return
        
        if app.selectedPiece is not None and 'piece' in app.selectedPiece:
            piece = app.selectedPiece['piece']
            if piece is not None and piece.get_color() == app.currentPlayer:
                currentPosition = currentPositions(app.blackPieces, app.whitePieces)
                if newPosition in currentPosition:               
                    for piece_info in app.piecesInfo:
                        if piece_info is not None and 'piece' in piece_info:
                            if piece_info['piece'].get_position() == newPosition:
                                if piece_info['piece'].get_color() == piece.get_color():
                                    return False
                                elif piece_info['piece'].get_color() != piece.get_color():
                                    if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                        capturedPiece = piece_info['piece']
                                        removePiece(app, capturedPiece, newPosition, piece_info)
                                        app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'
                else:
                    if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                        moveHelperFunction(app, newPosition)
                        app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'
    
def drawfunMode3():
    drawLabel('FREE FOR ALL! KILL ALL TO WIN!!', 300, 550, fill='white', size=20)

##FUN MODE 4 IS BELOW - KING OF THE HILL (King has to get to a certain cell before other king to win)

def kingOfTheHill(app):
    if app.initialized == False and app.funMode == 4:
        x = random.randint(2,9)
        y = random.randint(5,6)
        app.hillPosition = (x, y)
        returnNormalMode(app) 
        app.initialized = True

    for piece_info in app.piecesInfo:
        piece = piece_info["piece"]
        if piece.get_piece_type() == "king" and piece.get_position() == app.hillPosition:
            app.winner = 'white' if piece.get_color() == 'white' else 'black'

def onMousePress4(app,x,y):
    kingOfTheHill(app)
    
    cellSize = 50
    cellx = 1 + (int((x - 0.5 * cellSize) // cellSize))
    celly = 1 + (int((y - 0.5 * cellSize) // cellSize))

    newPosition = (cellx, celly)
    if app.selectedPiece is None:
        selectedPiece(app, newPosition)


    else:
        # Check if another piece is selected
        for piece_info in app.piecesInfo:
            if piece_info is not None and 'piece' in piece_info:
                if piece_info['piece'].get_position() == newPosition and piece_info['piece'].get_color() == app.currentPlayer:
                    app.selectedPiece = piece_info
                    return
        
        if app.selectedPiece is not None and 'piece' in app.selectedPiece:
            piece = app.selectedPiece['piece']
            if piece is not None and piece.get_color() == app.currentPlayer:
                currentPosition = currentPositions(app.blackPieces, app.whitePieces)
                if newPosition in currentPosition:
                    if piece.get_piece_type() == 'pawn':
                        if piece.can_capture(newPosition, (app.blackPieces + app.whitePieces)):
                            capturedPiece = None
                            getCapturedPiece(app, newPosition, piece)
                            app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white' 
                            promotion(app)
                                            
                    else:
                        for piece_info in app.piecesInfo:
                            if piece_info is not None and 'piece' in piece_info:
                                if piece_info['piece'].get_position() == newPosition:
                                    if piece_info['piece'].get_color() == piece.get_color():
                                        return False
                                    elif piece_info['piece'].get_color() != piece.get_color():
                                        if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                                            capturedPiece = piece_info['piece']
                                            removePiece(app, capturedPiece, newPosition, piece_info)
                                            app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'
                                            promotion(app)
                else:
                    if app.selectedPiece['piece'].can_move(newPosition, currentPositions(app.blackPieces, app.whitePieces)):
                        moveHelperFunction(app, newPosition)
                        app.currentPlayer = 'black' if app.currentPlayer == 'white' else 'white'
                        promotion(app)

def drawHillPosition(app):
    if app.initialized:
        x,y = app.hillPosition
        x = 50 * x - 25
        if y == 6:
            y = 275
        if y == 5:
            y = 225
        drawRect(x,y, 50, 50, fill='red', opacity=50)

def drawfunMode4():
    drawLabel('KING OF THE HILL. GET YOUR KING TO THE RED SQUARE.', 300, 550, fill='white', size=20)

####################################################################
## TUTORIAL CODE IS BELOW ##
####################################################################

def runTutorial(app):
    if app.stage >= 0 and app.stage <= 8:
        drawBoard(app)
    if app.stage == 0:
        stageZero()
    elif app.stage == 1:
        stageOne(app)
    elif app.stage == 2:
        stageTwo(app)
    elif app.stage == 3:
        stageThree(app)
    elif app.stage == 4:
        stageFour(app)
    elif app.stage == 5:
        stageFive(app)
    elif app.stage == 6:
        stageSix(app)
    elif app.stage == 7:
        stageSeven(app)
    elif app.stage == 8:
        stageEight(app)
    elif app.stage == 9:
        stageNine()
    drawButtons()

def customPlaces(app):
    if app.stage == 7:
        app.whitePieces = [Pawn('white', (2, 8)), Pawn('white', (3, 8)), Pawn('white', (4, 8)), Pawn('white', (5, 8)), Pawn('white', (6, 6)), Pawn('white', (7, 8)), Pawn('white', (8, 8)), Pawn('white', (9, 8)), Rook('white', (2, 9)), Knight('white', (3, 9)), Bishop('white', (4, 9)), Queen('white', (5, 9)), King('white', (6, 9)), Bishop('white', (3, 5)), Knight('white', (7, 7)), Rook('white', (9, 9))]
        app.blackPieces = [Pawn('black', (2, 3)), Pawn('black', (3, 3)), Pawn('black', (4, 3)), Pawn('black', (5, 3)), Pawn('black', (6, 4)), Pawn('black', (7, 3)), Pawn('black', (8, 3)), Pawn('black', (9, 3)), Rook('black', (2, 2)), Knight('black', (4, 4)), Bishop('black', (4, 2)), Queen('black', (5, 2)), King('black', (6, 2)), Bishop('black', (7, 2)), Knight('black', (8, 2)), Rook('black', (9, 2))]
    
        app.piecesInfo = []
        for piece in app.blackPieces + app.whitePieces:
            piece_x = 50 * piece.get_position()[0]
            piece_y = 50 * piece.get_position()[1]
            app.piecesInfo.append({"piece": piece, "x": piece_x, "y": piece_y, "width": 50, "height": 50})
            
    if app.stage == 8:
        app.whitePieces = [Pawn('white', (2, 8)), Pawn('white', (3, 8)), Pawn('white', (4, 6)), Pawn('white', (5, 6)), Pawn('white', (6, 8)), Pawn('white', (7, 8)), Pawn('white', (8, 7)), Pawn('white', (9, 8)), Rook('white', (2, 9)), Knight('white', (3, 9)), Bishop('white', (4, 9)), Queen('white', (5, 9)), King('white', (6, 9)), Bishop('white', (7, 9)), Knight('white', (8, 9)), Rook('white', (9, 9))]
        app.blackPieces = [Pawn('black', (2, 3)), Pawn('black', (3, 3)), Pawn('black', (4, 3)), Pawn('black', (5, 3)), Pawn('black', (6, 4)), Pawn('black', (7, 3)), Pawn('black', (8, 3)), Pawn('black', (9, 3)), Rook('black', (2, 2)), Knight('black', (3, 2)), Bishop('black', (4, 2)), Queen('black', (5, 2)), King('black', (6, 2)), Bishop('black', (7, 2)), Knight('black', (7, 4)), Rook('black', (9, 2))]
    
        app.piecesInfo = []
        for piece in app.blackPieces + app.whitePieces:
            piece_x = 50 * piece.get_position()[0]
            piece_y = 50 * piece.get_position()[1]
            app.piecesInfo.append({"piece": piece, "x": piece_x, "y": piece_y, "width": 50, "height": 50})

def skipbuttons(app,x, y):
    if x>400 and x<500 and y>0 and y<50 and app.stage >0:
        app.stage -=1
        time.sleep(0.1)
    elif x>500 and x<600 and y>0 and y<50 and app.stage<15: ##CHANGE HERE
        app.stage +=1
        time.sleep(0.1)

def drawButtons():
    drawRect(500,0,100,50,fill='green')
    drawLabel('Next', 550, 25, size=40)
    
    drawRect(400,0,100,50,fill='red')
    drawLabel('Prev', 450, 25, size=40)

def stageZero():
    drawLabel('Hello, this is a tutorial for the game of chess!', 300, 500, fill='white', size=20)
    drawLabel('Press next to move on.', 300, 550, fill='white', size=20)

def stageOne(app):
    drawLabel('Lets start with how the pieces move;', 300, 500, fill='white', size=20)
    for piece_info in app.piecesInfo:
        if 'piece' in piece_info and piece_info['piece'].get_color() == 'white' and piece_info['piece'].get_piece_type() == 'pawn':
            drawLabel(piece_info["piece"].get_piece_type(), 250, 300, fill='white')
            break
    drawLabel('The pawn can move 2 steps forward at his starting position', 300, 550, fill='white', size=20)
    drawLabel('or 1 step forward at any position and he captures diagonally', 300, 575, fill='white', size=20)
    drawRect(225,225,50,50,fill='blue')
    drawRect(225,175,50,50,fill='blue')
    drawRect(275,225,50,50,fill='red')
    drawRect(175,225,50,50,fill='red')

def stageTwo(app):
    drawLabel('Lets start with how the pieces move;', 300, 500, fill='white', size=20)
    for piece_info in app.piecesInfo:
        if 'piece' in piece_info and piece_info['piece'].get_color() == 'white' and piece_info['piece'].get_piece_type() == 'bishop':
            drawLabel(piece_info["piece"].get_piece_type(), 250, 300, fill='white')
            break
    drawLabel('The Bishop can move diagonally but cannot jump above any piece', 300, 550, fill='white', size=20)
    drawRect(275,225,50,50,fill='purple')
    drawRect(175,225,50,50,fill='purple')
    drawRect(275,325,50,50,fill='purple')
    drawRect(175,325,50,50,fill='purple')
    drawRect(325,375,50,50,fill='purple')
    drawRect(325,175,50,50,fill='purple')
    drawRect(125,375,50,50,fill='purple')
    drawRect(125,175,50,50,fill='purple')
    drawRect(75,425,50,50,fill='purple')
    drawRect(75,125,50,50,fill='purple')
    drawRect(375,425,50,50,fill='purple')
    drawRect(375,125,50,50,fill='purple')
    drawRect(425,75,50,50,fill='purple')

def stageThree(app):
    drawLabel('Lets start with how the pieces move;', 300, 500, fill='white', size=20)
    for piece_info in app.piecesInfo:
        if 'piece' in piece_info and piece_info['piece'].get_color() == 'white' and piece_info['piece'].get_piece_type() == 'knight':
            drawLabel(piece_info["piece"].get_piece_type(), 250, 300, fill='white')
            break
    drawLabel('The Knight jumps over pieces in an L shape', 300, 550, fill='white', size=20)
    drawRect(325, 325, 50,50, fill='blue')
    drawRect(325, 225, 50,50, fill='blue')
    drawRect(125, 325, 50,50, fill='blue')
    drawRect(125, 225, 50,50, fill='blue')
    
    drawRect(275, 375, 50,50, fill='blue')
    drawRect(275, 175, 50,50, fill='blue')
    drawRect(175, 375, 50,50, fill='blue')
    drawRect(175, 175, 50,50, fill='blue')
    
def stageFour(app):
    drawLabel('Lets start with how the pieces move;', 300, 500, fill='white', size=20)
    for piece_info in app.piecesInfo:
        if 'piece' in piece_info and piece_info['piece'].get_color() == 'white' and piece_info['piece'].get_piece_type() == 'rook':
            drawLabel(piece_info["piece"].get_piece_type(), 250, 300, fill='white')
            break
    drawLabel('The Rook can move anywhere horizontally and vertically', 300, 550, fill='white', size=20)
    drawRect(125, 275, 50,50, fill='blue')
    drawRect(75, 275, 50,50, fill='blue')
    drawRect(175, 275, 50,50, fill='blue')
    drawRect(325, 275, 50,50, fill='blue')
    drawRect(425, 275, 50,50, fill='blue')
    drawRect(375, 275, 50,50, fill='blue')
    drawRect(275, 275, 50,50, fill='blue')
    
    drawRect(225, 75, 50,50, fill='blue')
    drawRect(225, 125, 50,50, fill='blue')
    drawRect(225, 175, 50,50, fill='blue')
    drawRect(225, 225, 50,50, fill='blue')
    drawRect(225, 325, 50,50, fill='blue')
    drawRect(225, 375, 50,50, fill='blue')
    drawRect(225, 425, 50,50, fill='blue')

def stageFive(app):
    drawLabel('Lets start with how the pieces move;', 300, 500, fill='white', size=20)
    for piece_info in app.piecesInfo:
        if 'piece' in piece_info and piece_info['piece'].get_color() == 'white' and piece_info['piece'].get_piece_type() == 'queen':
            drawLabel(piece_info["piece"].get_piece_type(), 250, 300, fill='white')
            break
    drawLabel('The Queen can move anywhere horizontally and vertically and diagonally', 300, 550, fill='white', size=20)
    
    drawRect(125, 275, 50,50, fill='blue')
    drawRect(75, 275, 50,50, fill='blue')
    drawRect(175, 275, 50,50, fill='blue')
    drawRect(325, 275, 50,50, fill='blue')
    drawRect(425, 275, 50,50, fill='blue')
    drawRect(375, 275, 50,50, fill='blue')
    drawRect(275, 275, 50,50, fill='blue')
    
    drawRect(225, 75, 50,50, fill='blue')
    drawRect(225, 125, 50,50, fill='blue')
    drawRect(225, 175, 50,50, fill='blue')
    drawRect(225, 225, 50,50, fill='blue')
    drawRect(225, 325, 50,50, fill='blue')
    drawRect(225, 375, 50,50, fill='blue')
    drawRect(225, 425, 50,50, fill='blue')
    
    drawRect(275,225,50,50,fill='purple')
    drawRect(175,225,50,50,fill='purple')
    drawRect(275,325,50,50,fill='purple')
    drawRect(175,325,50,50,fill='purple')
    drawRect(325,375,50,50,fill='purple')
    drawRect(325,175,50,50,fill='purple')
    drawRect(125,375,50,50,fill='purple')
    drawRect(125,175,50,50,fill='purple')
    drawRect(75,425,50,50,fill='purple')
    drawRect(75,125,50,50,fill='purple')
    drawRect(375,425,50,50,fill='purple')
    drawRect(375,125,50,50,fill='purple')
    drawRect(425,75,50,50,fill='purple')

def stageSix(app):
    drawLabel('Lets start with how the pieces move;', 300, 500, fill='white', size=20)
    for piece_info in app.piecesInfo:
        if 'piece' in piece_info and piece_info['piece'].get_color() == 'white' and piece_info['piece'].get_piece_type() == 'king':
            drawLabel(piece_info["piece"].get_piece_type(), 250, 300, fill='white')
            break
    drawLabel('The King can move 1 cell in any direction', 300, 550, fill='white', size=20)
    
    drawRect(225, 325, 50,50, fill='blue')
    drawRect(225, 225, 50,50, fill='blue')
    
    drawRect(275, 275, 50,50, fill='blue')
    drawRect(175, 275, 50,50, fill='blue')
    
    drawRect(275,225,50,50,fill='purple')
    drawRect(175,225,50,50,fill='purple')
    drawRect(275,325,50,50,fill='purple')
    drawRect(175,325,50,50,fill='purple')

def stageSeven(app):
    drawLabel('Here are some interesting tactics', 300, 500, fill='white', size=20)
    drawLabel('Ruy Lopez Opening', 300, 550, fill='white', size=20)
    
    for piece_info in app.piecesInfo:
        color = 'black' if piece_info["piece"].get_color() == 'black' else 'white'
        drawLabel(piece_info["piece"].get_piece_type(), piece_info["x"], piece_info["y"], fill=color)

def stageEight(app):
    drawLabel('Here are some interesting tactics', 300, 500, fill='white', size=20)
    drawLabel('Catalan Opening', 300, 550, fill='white', size=20)
    
    for piece_info in app.piecesInfo:
        color = 'black' if piece_info["piece"].get_color() == 'black' else 'white'
        drawLabel(piece_info["piece"].get_piece_type(), piece_info["x"], piece_info["y"], fill=color)

def stageNine():
    drawRect(0,0,600,600,fill=rgb(48, 46, 43))
    
    drawLabel('Chess is a fun and competitive game. The only way to get better is', 300, 100, fill='white', size=20)
    drawLabel('by reading and practicing just like any other game. You should', 300, 150, fill='white', size=20)
    drawLabel('always attempt to think about what your opponent is going to', 300, 200, fill='white', size=20)
    drawLabel("play and play accordingly. Outsmarting your opponent isn't", 300, 250, fill='white', size=20)
    drawLabel('always by capturing more pieces but by rather figuring out', 300, 300, fill='white', size=20)
    drawLabel('a way past his defenses to attack the king and cornering him.', 300, 350, fill='white', size=20)
    
    drawLabel('Good Luck! Remember to have fun!', 300, 450, fill='white', size=20)

runApp()