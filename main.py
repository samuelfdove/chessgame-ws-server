import asyncio
import chess
import json
import os
import secrets
import signal
from stockfish import Stockfish
import websockets
from chessgame import Game

JOIN = {}

print(os.listdir())
# stockfish = Stockfish(path="./stockfish-ubuntu-x86-64-avx2")
# stockfish = Stockfish(path="./stockfish_15_x64_avx2.exe")

async def play(websocket, g, connected):
  async for message in websocket:
    event = json.loads(message)
    if event["type"]=="newgame":
      g.b.reset()
    else:
       move = event['from']+event['to']
       g.b.push(chess.Move.from_uci(move))
       g.aftermove()
    websockets.broadcast(connected, json.dumps({"type": "boardupdate","fen": g.b.fen(), "dests": g.getlegalmoves()}))

async def start(websocket, event):
   event_id = event["id"]
   if event_id in JOIN:
      await websocket.send(json.dumps({"type": "gameconfirmation", "value": "false"}))
   else:
      g = Game(event["config"], stockfish)
      await websocket.send(json.dumps({"type": "gameconfirmation", "value": "true", "orientation": g.p1orientation, "FEN": g.b.fen(), "dests": g.getlegalmoves()}))
      connected = {websocket}
      JOIN[event_id] = g,connected
      try:
         print('player1 started game')
         await play(websocket,g,connected)
      finally:
         print("player1left?")
         del JOIN[event_id]
  

async def joingame(websocket,event):
   if event["id"] in JOIN:
      g,connected= JOIN[event["id"]]
      await websocket.send(json.dumps({"type": "gameconfirmation", "value": "true", "orientation": g.p2orientation, "FEN": g.b.fen(), "dests": g.getlegalmoves()}))
      
      connected.add(websocket)
      try:
         print('player2 joined')
         await play(websocket,g,connected)
      finally:
         print('player2left?')
         connected.remove(websocket)
   else:
      await websocket.send(json.dumps({"type": "gameconfirmation", "value": "false"}))
   



async def handler(websocket):
   message = await websocket.recv()
   event = json.loads(message)
   if event["type"]=="joingame":
      await joingame(websocket, event)
   else:
      await start(websocket, event)
        

        


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever

async def mainlocal():
   port = int(os.environ.get("PORT", "8001"))
   async with websockets.serve(handler, "", port):
      await asyncio.Future()  # run forever


if __name__ == "__main__":
   stockfish = Stockfish(path="./stockfish_15_x64_avx2.exe")
   asyncio.run(mainlocal())