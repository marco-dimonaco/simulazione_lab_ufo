from dataclasses import dataclass # 1
from model.states import State


@dataclass
class Connessione:
    stato1: State
    stato2: State
