from dataclasses import dataclass
from model.states import State


@dataclass
class Connessione:
    stato1: State
    stato2: State
