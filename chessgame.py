import chess
import random

class Game:
    def __init__(self,config, stockfish):
        self.b = chess.Board(config["FEN"])
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
        else:
           self.whiterandom = config["p2random"]
           self.blackrandom = config["p1random"]
           self.whitecomputer = config["p2computer"]
           self.blackcomputer = config["p1computer"]
        self.stockfish=stockfish
        
        
    
    def getlegalmoves(self):
      movesdict = {}
      for move in self.b.legal_moves:
        if chess.square_name(move.from_square) in movesdict:
          movesdict[chess.square_name(move.from_square)] = movesdict[chess.square_name(move.from_square)] + [chess.square_name(move.to_square)]
        else:
          movesdict[chess.square_name(move.from_square)] = [chess.square_name(move.to_square)]
      return movesdict
    
    def makerandommove(self):
       self.b.push(random.choice(list(self.b.legal_moves)))
    
    def makecomputermove(self):
       self.stockfish.set_fen_position(self.b.fen())
       self.b.push(chess.Move.from_uci(self.stockfish.get_best_move()))
    
    def aftermove(self):
       if self.b.turn:
          if self.whiterandom:
             if self.b.fullmove_number % int(self.whiterandom)==0:
                self.makerandommove()
                self.aftermove()
          if self.whitecomputer:
             if self.b.fullmove_number % int(self.whitecomputer)==0:
                self.makecomputermove()
                self.aftermove()
       else:
          if self.blackrandom:
             if self.b.fullmove_number % int(self.blackrandom)==0:
                self.makerandommove()
                self.aftermove()
          if self.blackcomputer:
             if self.b.fullmove_number % int(self.blackcomputer)==0:
                self.makecomputermove()
                self.aftermove()
                
       
    

    
            