import pandas
from engine import session
from events import Coincidence, Photon, Hit
from tqdm import tqdm

data = pandas.read_csv('./compton_scatter.csv')

nb_hits = data.shape[0]

previous_coincidence = None
previous_photon = None
coincidence = None
photon = None


def make_hit(row, photon):
    hit = Hit(
        index=row['hitIndex'],
        x=row['x'],
        y=row['y'],
        z=row['z'],
        energy=row['energy'],
        time=row['timeT'])
    photon.hits.append(hit)
    session.add(hit)
    return hit


def make_coincidence(cid, c, row):
    global previous_coincidence
    if previous_coincidence != cid:
        if c is not None:
            session.add(c)
            # session.commit()
        c = Coincidence(photons=[], is_scatter=(row['true_scatter'] == 0))
        previous_coincidence = cid
    return c


def make_photon(pid, p, coincidence):
    global previous_photon
    if previous_photon != pid:
        if p is not None:
            session.add(p)
        p = Photon(hits=[], index=pid)
        coincidence.photons.append(p)
        previous_photon = pid
    return p


import time

for i in tqdm(range(nb_hits)):
    row = data.iloc[i]
    cid = row['coincidenceID']
    pid = row['photonID']
    coincidence = make_coincidence(cid, coincidence, row)
    photon = make_photon(pid, photon, coincidence)
    hit = make_hit(row, photon)
session.commit()