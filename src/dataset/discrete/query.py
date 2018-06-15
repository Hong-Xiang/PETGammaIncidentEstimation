from engine import get_or_create_session
from events import Coincidence, Photon, Hit, create_all
import tqdm
import numpy as np

from contextlib import contextmanager
dataset_path = '../../../data/gamma.db'

create_all(dataset_path)


def query_phton_and_first_hit():
    return (get_or_create_session().query(Photon, Hit)
            .filter(Hit.photon_id == Photon.id).filter(Hit.index == 0))


def photon_capacity():
    return get_or_create_session().query(Photon).count()


def hits():
    return get_or_create_session().query(Photon.hits).limit(10).all()


@contextmanager
def hits_generator():
    get_or_create_session().query(Photon.hits)


def get_first_hits_for_all_photon():
    columns = ['x', 'y', 'z', 'energy']
    for p, h in (query_phton_and_first_hit().limit(10)):
        # print(p.hits)
        print(np.array([h.to_list(columns) for h in p.hits]))
        # print(p_hits)
        print(h.to_list(columns))


def get_first_hits_and_second_large_energy_hits():
    pass


print(hits())