from tqdm import tqdm
import pandas as pd
import numpy as np
from pprint import pprint
import math
#import sys

def process_edep(g):
    print('TYPE', type(g['x']))
    return np.array([np.array(g['x']), np.array(g['y']), np.array(g['z']), np.array(g['energy'])])

def process_state(g,crysX,crysY,crysZ):
#crysX,Y,Z means crystal's length,width,thickness
#return momentum direction and the position of incidence point
#firstly, providing that particle are incident from above
    pbX=0.5*crysX
    pbY=0.5*crysY
    pbZ=0.5*crysZ
    incipointX=g.iloc[0]['srcX']+((crysZ-g.iloc[0]['srcZ'])/(g.iloc[0]['z']-g.iloc[0]['srcZ']))*(g.iloc[0]['x']-g.iloc[0]['srcX'])
    incipointY=g.iloc[0]['srcY']+((crysZ-g.iloc[0]['srcZ'])/(g.iloc[0]['z']-g.iloc[0]['srcZ']))*(g.iloc[0]['y']-g.iloc[0]['srcY'])
    incipointZ=crysZ
    if incipointX > 0.5*crysX or incipointX < -0.5*crysX:
        index=incipointX/abs(incipointX)
        incipointX=pbX*index
        incipointY=g.iloc[0]['srcY']+((incipointX-g.iloc[0]['srcX'])/(g.iloc[0]['x']-g.iloc[0]['srcX']))*(g.iloc[0]['y']-g.iloc[0]['srcY'])
        incipointZ=g.iloc[0]['srcZ']+((incipointX-g.iloc[0]['srcX'])/(g.iloc[0]['x']-g.iloc[0]['srcX']))*(g.iloc[0]['z']-g.iloc[0]['srcZ'])
        if incipointY> 0.5*crysY or incipointY < -0.5*crysY:
            index=incipointX/abs(incipointY)
            incipointY=pbY*index  
            incipointX=g.iloc[0]['srcX']+((incipointY-g.iloc[0]['srcY'])/(g.iloc[0]['y']-g.iloc[0]['srcY']))*(g.iloc[0]['x']-g.iloc[0]['srcX'])
            incipointZ=g.iloc[0]['srcZ']+((incipointY-g.iloc[0]['srcY'])/(g.iloc[0]['y']-g.iloc[0]['srcY']))*(g.iloc[0]['z']-g.iloc[0]['srcZ'])       
    elif incipointY > 0.5*crysY or incipointY < -0.5*crysY:
            index=incipointX/abs(incipointY)
            incipointY=pbY*index
            incipointX=g.iloc[0]['srcX']+((incipointY-g.iloc[0]['srcY'])/(g.iloc[0]['y']-g.iloc[0]['srcY']))*(g.iloc[0]['x']-g.iloc[0]['srcX'])
            incipointZ=g.iloc[0]['srcZ']+((incipointY-g.iloc[0]['srcY'])/(g.iloc[0]['y']-g.iloc[0]['srcY']))*(g.iloc[0]['z']-g.iloc[0]['srcZ'])    
    return np.array([np.array(g.iloc[0]['x']-g.iloc[0]['srcX']), np.array(g.iloc[0]['y']-g.iloc[0]['srcY']), np.array(g.iloc[0]['z']-g.iloc[0]['srcZ']),np.array(incipointX),np.array(incipointY),np.array(incipointZ)])
#np.array(g.iloc[0]['x']), np.array(g.iloc[0]['y']), np.array(g.iloc[0]['z'])])

def process_run(data,crysX,crysY,crysZ):
    data=data[data['particalID']==22]
    data=data.groupby('eventID')
    result=[]
    for e in tqdm(data.groups,ascii=True,leave=False):
#        result+=[[process_state(data.get_group(e)),process_edep(data.get_group(e))]]
        result += [[process_state(data.get_group(e),crysX,crysY,crysZ), process_edep(data.get_group(e))]]
    return result

data = pd.read_csv('hits.txt',header=0)#names=['run','event','track', 'photon', 'process', 'x', 'y', 'z', 'energy', 'compton', 'pid']
crysX=30
crysY=30
crysZ=10
result=process_run(data,crysX,crysY,crysZ)    
#np.save('try.npy',result)
pprint(result)
#pprint(result[0,3:5])
#pprint(result[2])
