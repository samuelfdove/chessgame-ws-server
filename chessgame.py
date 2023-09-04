import chess
import random

class Game:
    def __init__(self,config, stockfish):
        self.b = chess.Board(config["FEN"])
        self.awaitingMessage = False
        self.needtosendMessage = False
        self.message = ""
        self.allowedpieces = [1,2,3,4,5,6]
        self.p1orientation = config["orientation"]
        if self.p1orientation=="white":
          self.p2orientation= "black"
        else:
           self.p2orientation="white"
        self.config = config

        if self.p1orientation=="white":
           self.whiterandom = config["p1random"]
           self.blackrandom = config["p2random"]
           self.whitecomputer = config["p1computer"]
           self.blackcomputer = config["p2computer"]
           self.whitechoosepiece = config["p1choosepiece"]
           self.blackchoosepiece = config["p2choosepiece"]
        else:
           self.whiterandom = config["p2random"]
           self.blackrandom = config["p1random"]
           self.whitecomputer = config["p2computer"]
           self.blackcomputer = config["p1computer"]
           self.whitechoosepiece = config["p2choosepiece"]
           self.blackchoosepiece = config["p1choosepiece"]
        self.stockfish=stockfish
        
        
    
    def getlegalmoves(self):
      movesdict = {}

      if self.awaitingMessage:
         return movesdict

      for move in self.b.legal_moves:
         if self.b.piece_type_at(move.from_square) in self.allowedpieces:
            if chess.square_name(move.from_square) in movesdict:
               movesdict[chess.square_name(move.from_square)] = movesdict[chess.square_name(move.from_square)] + [chess.square_name(move.to_square)]
            else:
               movesdict[chess.square_name(move.from_square)] = [chess.square_name(move.to_square)]
      return movesdict
    
    def makerandommove(self):
       self.b.push(random.choice(list(self.b.legal_moves)))
    
    def makecomputermove(self):
      #  self.stockfish.set_fen_position(self.b.fen())
      #  self.b.push(chess.Move.from_uci(self.stockfish.get_best_move()))
       pass
    
    def processmessage(self, message):
       if (self.whitechoosepiece and self.b.fullmove_number % int(self.whitechoosepiece)==0) or (self.blackchoosepiece and self.b.fullmove_number % int(self.blackchoosepiece)==0):
          if message not in ['pawn','knight','bishop','queen','king','rook']:
             return "Please enter an appropriate piece name (pawn, knight, bishop, rook, queen, king)"
          for i in range(1,7):
             if chess.piece_name(i)==message:
                self.allowedpieces = [i]
                self.awaitingMessage = False
                return "The next move must be made with a "+message
    
    def setdefaults(self):
       self.allowedpieces = [1,2,3,4,5,6]

    
    def aftermove(self):
       self.setdefaults()
       if self.b.turn:
          if self.whiterandom:
             if self.b.fullmove_number % int(self.whiterandom)==0:
                self.makerandommove()
                self.aftermove()
          if self.whitecomputer:
             if self.b.fullmove_number % int(self.whitecomputer)==0:
                self.makecomputermove()
                self.aftermove()
          if self.whitechoosepiece:
             if self.b.fullmove_number % int(self.whitechoosepiece)==0:
                self.needtosendMessage = True
                self.message = "Choose which piece your opponent must move by sending the piece name in a message (pawn, knight, bishop, rook, queen, king):"
                self.awaitingMessage=True
       else:
          if self.blackrandom:
             if self.b.fullmove_number % int(self.blackrandom)==0:
                self.makerandommove()
                self.aftermove()
          if self.blackcomputer:
             if self.b.fullmove_number % int(self.blackcomputer)==0:
                self.makecomputermove()
                self.aftermove()
          if self.blackchoosepiece:
             if self.b.fullmove_number % int(self.blackchoosepiece)==0:
                self.needtosendMessage = True
                self.message = "Choose which piece your opponent must move by sending the piece name in a message (pawn, knight, bishop, queen, king):"
                self.awaitingMessage = True
                
       
    

    
            