import pygame
from Settings import *
from enemies import *

class TimeTable():
    def __init__(self):
        self.enemytiming = {0: [Shadow()]}

    def reset(self):
        for time in self.enemytiming:
            for e in self.enemytiming[time]:
                e.reset()