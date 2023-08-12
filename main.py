import asyncio
import chess
import json
import os
import secrets
import signal
# from stockfish import Stockfish
import websockets

JOIN = {}
# stockfish = Stockfish(path="./stockfish_15_x64_avx2.exe")

async def play(websocket, b, connected):
  async for message in websocket:
    event = json.loads(message)
    if event["type"]=="newgame":
      b.reset()
      await websocket.send(json.dumps({"type": "fen","value": b.fen()}))
    else:
       move = event['from']+event['to']
       b.push(chess.Move.from_uci(move))
       websockets.broadcast(connected, json.dumps({"type": "fen","value": b.fen()}))
       

async def start(websocket):
  b = chess.Board()
  connected = {websocket}
  joinkey = "test"
  JOIN[joinkey] = b,connected
  print('player1 started game')
  await play(websocket,b,connected)
  print("player1left?")
  

async def joingame(websocket,joinkey="test"):
   b,connected= JOIN[joinkey]
   connected.add(websocket)
   try:
      print('player2 joined')
      await play(websocket,b,connected)
   finally:
      print('player2left?')
      connected.remove(websocket)
   



async def handler(websocket):
   message = await websocket.recv()
   event = json.loads(message)
   if event["type"]=="joingame":
      await joingame(websocket)
   else:
      await start(websocket)
        

        


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())