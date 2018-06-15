"""
Convert csv data to database.
"""
import pandas
from engine import get_or_create_session
from orms import Experiment, Coincidence, Event, Photon, Hit, get_experiment_hash, create_all
from tqdm import tqdm
import numpy as np
from functools import lru_cache
import time

import click
from dxl.core.logger import Logger
from dxl.core.logger.utils import set_logging_info_level_with_default_format

from dxl.core.debug import enter_debug
enter_debug()

logger = Logger('incident_estimation')
set_logging_info_level_with_default_format()

NB_CHUNK = 1000


class DataSpec:
    def __init__(self, hits_csv, coincidence_csv, target_path):
        self.hits_csv = hits_csv
        self.coincidence_csv = coincidence_csv
        self.target_path = target_path


def load_data(s: DataSpec):
    coincidence = pandas.read_csv(s.coincidence_csv)
    hits = pandas.read_csv(s.hits_csv)
    return hits, coincidence


class Processing:
    experiment = None
    session = None
    events = {}
    photons = {}


def make_experiment(s: DataSpec):
    e = Experiment(hash=get_experiment_hash(s.coincidence_csv, s.hits_csv))
    Processing.experiment = e
    return e


def get_photon(eid, pid):
    # result = (Processing.session.query(Photon).filter(Photon.index == pid)
    #           .filter(Photon.experiment == Processing.experiment).join(Event)
    #           .filter(Event.index == eid).all())
    # if len(result) == 0:
    #     return None
    # if len(result) > 1:
    #     raise ValueError("Multiple photon found.")
    # return result[0]
    return Processing.photons.get(eid, {}).get(pid)


def make_photon(eid, pid):
    p = Photon(index=pid, experiment=Processing.experiment, hits=[])
    get_event(eid).photons.append(p)
    Processing.session.add(p)
    Processing.photons[eid][pid] = p
    return p


def get_or_create_photon(eid, pid):
    if get_photon(eid, pid) is None:
        p = make_photon(eid, pid)
    return get_photon(eid, pid)


def get_event(eid):
    # return (Processing.session.query(Event).filter(Event.index == eid)
    # .filter(Event.experiment == Processing.experiment).one())
    return Processing.events.get(eid)


def make_event(eid):
    e = Event(index=int(eid), photons=[], experiment=Processing.experiment)
    Processing.session.add(e)
    Processing.events[eid] = e
    Processing.photons[eid] = {}
    return e


def get_or_create_event(eid):
    if get_event(eid) is None:
        Processing.events[eid] = make_event(eid)
    return get_event(eid)


def make_hit(row):
    hit = Hit(
        x=row['posX'],
        y=row['posY'],
        z=row['posZ'],
        energy=row['edep'],
        time=row['time'],
        experiment=Processing.experiment)
    Processing.session.add(hit)
    return hit


def process_row(row):
    hit = make_hit(row)
    eid, pid = int(row['eventID']), int(row['photonID'])
    e = get_or_create_event(eid)
    p = get_or_create_photon(eid, pid)
    p.hits.append(hit)
    hit.index = len(p.hits) - 1
    return hit


@logger.before.info('Processing rows...')
@logger.after.info('Process row done.')
def process_rows(hits_data):
    for i in tqdm(range(hits_data.shape[0]), ascii=True):
        process_row(hits_data.iloc[i])
        if i % NB_CHUNK == 0:
            flush()


@logger.before.info('committing...')
@logger.after.info('commit done.')
def commit():
    Processing.session.commit()


# @logger.before.info('flushing...')
# @logger.after.info('flush done.')
def flush():
    Processing.session.flush()


# @logger.before.info('Making events...')
# @logger.after.info('Making events done, with {} eids:\n{}.\n')
# def make_events(hits_data):
#     eids = hits_data['eventID'].unique()
#     eids = [int(e) for e in eids]
#     for e in tqdm(eids, ascii=True):
#         make_event(e)
#     return len(eids), np.array(eids)


def make_coincidence(row):
    c = Coincidence(
        events=[
            get_event(int(row['eventID1'])),
            get_event(int(row['eventID2']))
        ],
        type=(int(row['type(0:scatter-1:random-2:true)'])),
        experiment=Processing.experiment)
    Processing.session.add(c)
    return c


def make_coincidences(conincidence_data):
    for i in tqdm(range(conincidence_data.shape[0]), ascii=True):
        make_coincidence(conincidence_data.iloc[i])
        if i % NB_CHUNK == 0:
            flush()


# def make_photon(pid, p, coincidence):
#     global previous_photon
#     if previous_photon != pid:
#         if p is not None:
#             session.add(p)
#         p = Photon(hits=[], index=pid)
#         coincidence.photons.append(p)
#         previous_photon = pid
#     return p


def make_session(target):
    create_all(target)
    Processing.session = get_or_create_session(target)


@logger.before.info(
    'Generating database from:\nCoincidence csv: {coincidence_csv},\nHits csv: {hits_csv},\nTarget: {target}.\n'
)
@logger.after.info('Done.')
def main(coincidence_csv, hits_csv, target):
    s = DataSpec(hits_csv, coincidence_csv, target)
    hits_data, coincidences_data = load_data(s)
    make_experiment(s)
    make_session(target)
    # make_events(hits_data)
    # flush()
    process_rows(hits_data)
    flush()
    make_coincidences(coincidences_data)
    commit()
    Processing.session.close()
    # make_photons(hits_data)
    # for i in tqdm(range(nb_hits)):
    #     row = data.iloc[i]
    #     cid = row['coincidenceID']
    #     pid = row['photonID']
    #     coincidence = make_coincidence(cid, coincidence, row)
    #     photon = make_photon(pid, photon, coincidence)
    #     hit = make_hit(row, photon)
    # session.commit()


import shutil
from pathlib import Path
import os


@click.command()
@click.option(
    '--coincidence',
    '-c',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    '--hits',
    '-h',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--target', '-t', type=click.types.Path(exists=False))
def cli(coincidence, hits, target):
    if Path(target).exists():
        os.remove(target)
    main(coincidence_csv=coincidence, hits_csv=hits, target=target)


if __name__ == "__main__":
    cli()
