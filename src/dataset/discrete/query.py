from engine import session
from events import Coincidence, Photon, Hit
import tqdm
import numpy as np


def query_phton_and_first_hit():
    return (session.query(Photon, Hit).filter(Hit.photon_id == Photon.id)
            .filter(Hit.index == 0))


def get_first_hits_for_all_photon():
    columns = ['x', 'y', 'z', 'energy']
    for p, h in (query_phton_and_first_hit().limit(10)):
        # print(p.hits)
        print(np.array([h.to_list(columns) for h in p.hits]))
        # print(p_hits)
        print(h.to_list(columns))


def get_first_hits_and_second_large_energy_hits():
    pass


get_first_hits_for_all_photon()