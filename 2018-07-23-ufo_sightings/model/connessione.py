from dataclasses import dataclass
from model.states import State


@dataclass
class Connessione:
    s1: State
    s2: State
