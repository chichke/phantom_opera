import json
import logging
import os
import random
import socket
import torch
import math
from logging.handlers import RotatingFileHandler
from src.globals import colors

import protocol

host = "localhost"
port = 12000
# HEADERSIZE = 10

"""
set up inspector logging
"""
inspector_logger = logging.getLogger()
inspector_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s :: %(levelname)s :: %(message)s", "%H:%M:%S")
# file
if os.path.exists("./logs/inspector.log"):
    os.remove("./logs/inspector.log")
file_handler = RotatingFileHandler('./logs/inspector.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
inspector_logger.addHandler(file_handler)
# stream
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
inspector_logger.addHandler(stream_handler)

# initalize weight

dtype = torch.float
device = torch.device("cpu")
# device = torch.device("cuda:0") # Uncomment this to run on GPU

# Create random input and output data
x = torch.linspace(-math.pi, math.pi, 2000, device=device, dtype=dtype)
y = torch.sin(x)

# Randomly initialize weights
a = torch.randn((), device=device, dtype=dtype)
b = torch.randn((), device=device, dtype=dtype)
c = torch.randn((), device=device, dtype=dtype)
d = torch.randn((), device=device, dtype=dtype)

learning_rate = 1e-6

class Player():

    def __init__(self):

        self.end = False
        # self.old_question = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.socket.connect((host, port))

    def reset(self):
        self.socket.close()

    def brownPower(self, data):
        return 0

    def activatePowerBrown(self, data):
        return 0

    def activatePowerBlack(self, data):
        return 0

    def activatePowerWhite(self, data):
        return 0

    def answerQuestion(self, i, data):
            switcher = {
                'activate brown power': self.activatePowerBrown(data),
                'activate black power': self.activatePowerBlack(data),
                'activate white power': self.activatePowerWhite(data),
                'white character power move ' + colors[0]: 1,
                'white character power move ' + colors[1]: 1,
                'white character power move ' + colors[2]: 1,
                'white character power move ' + colors[3]: 1,
                'white character power move ' + colors[4]: 1,
                'white character power move ' + colors[5]: 1,
                'white character power move ' + colors[6]: 1,
                'white character power move ' + colors[7]: 1,
                'brown character power': self.brownPower(data),
                'select character': self.character(data),
                'select position': self.position(data),

            }
            return switcher.get(i, 0)

    def solution(self, data, type):
        response = random.randint(0, len(data)-1)   
        print(type)
        print(data)
        print(response)
        return response 

    def position(self, data):
        return 0 

    def character(self, data):
        tierList = ['']
        return 0    

    def answer(self, question):
        # work
        data = question["data"]
        game_state = question["game state"]
        # randIndex = torch.randn(0, len(data)-1)
        print(self.getSuspectNB(game_state))
        self.solution(data, question['question type'])
        response_index = random.randint(0, len(data)-1)
        # log
        inspector_logger.debug(game_state)  
        inspector_logger.debug("|\n|")
        inspector_logger.debug("inspector answers")
        inspector_logger.debug(f"question type ----- {question['question type']}")
        inspector_logger.debug(f"data -------------- {data}")
        inspector_logger.debug(f"response index ---- {response_index}")
        inspector_logger.debug(f"response ---------- {data[response_index]}")
        return response_index   
    def getSuspectNB(self, gameState):
        suspectNb = 0
        for character in gameState['characters']:
            if character['suspect']:
                suspectNb += 1
                pass
            pass
        return suspectNb    
    def handle_json(self, data):
        data = json.loads(data)
        response = self.answer(data)
        # send back to server
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data) 
    def run(self):  
        self.connect()  
        while self.end is not True:
            received_message = protocol.receive_json(self.socket)
            if received_message:
                self.handle_json(received_message)
            else:
                print("no message, finished learning")
                self.end = True


p = Player()

p.run()
