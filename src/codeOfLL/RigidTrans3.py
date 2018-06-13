import numpy as np
import math

def process_translation(g,hchz):
    for i in range(0,3):
        g[1][i]-=g[0][i+3]
    g[1][2]+=2*hchz
    g[0][3:6]=np.array([0,0,2*hchz])
    return g

def process_rotation(g,theta):
    dirx=g[0][0]
    diry=g[0][1]
    m=np.sqrt(pow(dirx,2)+pow(diry,2))
#rotation matrix around axis z: Rotate the incident direction around the z-axis to the x-axis
    matrix_z=np.array([[dirx/m,-diry/m,0],[diry/m,dirx/m,0],[0,0,1]])
    g[0][0:3]=np.dot(g[0][0:3],matrix_z)
    dirx2=g[0][0]
    dirz2=g[0][2]
    n=np.sqrt(pow(dirx2,2)+pow(dirz2,2))
#rotation matrix around y-axis: Rotate the x-axiss around the y-axis to the z-axis
    matrix_y=np.array([[-dirz2/n,0,-dirx2/n],[0,1,0],[dirx2/n,0,-dirz2/n]])
#    g[1][0:3]=np.transpose(np.dot(np.dot(np.transpose(g[1][0:3]),matrix_z),matrix_y))
    g[0][0:3]=np.dot(g[0][0:3],matrix_y)
#rotation matrix around y-axis: Rotate the z-axiss around the y-axis to other direction
    matrix_y2=np.array([[np.cos(theta),0,-np.sin(theta)],[0,1,0],[np.sin(theta),0,np.cos(theta)]])
    g[1][0:3]=np.transpose((np.dot(np.dot(np.dot(np.transpose(g[1][0:3]),matrix_z),matrix_y),matrix_y2)))
    g[0][0:3]=np.dot(g[0][0:3],matrix_y2)
#    matrix_y=np.array([[math.cos(theta)*dirx2/n+math.sin(theta)*dirz2/n,0,math.sin(theta)*dirx2/n-math.cos(theta)*dirz2/n],
#                       [0,1,0],
#                       [-math.sin(theta)*dirx2/n+math.cos(theta)*dirz2/n,0,math.cos(theta)*dirx2/n+math.sin(theta)*dirz2/n]])
#    matrix_y=np.array([[-dirz2/n,0,-dirx2/n],[0,1,0],[dirx2/n,0,-dirz2/n]])
#    g[0][0:3]=np.dot(g[0][0:3],matrix_y)
#    g[0][0:3]=np.dot(np.dot(g[0][0:3],matrix_z),matrix_y)
#    print(lin1)
#    print(lin2)

    return g

def process_distribution(g,lx,wy,hz,hclx,hcwy,hchz):
    columnP=[int(((y+hcwy)/wy)) for y in g[1][1]]
    print(columnP)
    rowP=[int(((x+hclx)/lx)) for x in g[1][0]]
    print(rowP)
    pageP=[int(((2*hchz-z)/hz)) for z in g[1][2]]
    print(pageP)
    l=len(rowP)
    numMatrix=np.zeros((int(2*hclx/lx),int(2*hcwy/wy),int(2*hchz/hz)))
    energyMatrix=np.zeros((int(2*hclx/lx),int(2*hcwy/wy),int(2*hchz/hz)))
    for i in range(0,l):
        if rowP[i]<2*hclx and columnP[i]<2*hcwy and pageP[i]<2*hchz:
            numMatrix[rowP[i]][columnP[i]][pageP[i]]+=1
            energyMatrix[rowP[i]][columnP[i]][pageP[i]]+=g[1][3][i]
    return numMatrix,energyMatrix
        

def process_run(data,theta,lx,wy,hz,hclx,hcwy,hchz):
    l=data.shape[0]
    numM=np.zeros((int(2*hclx/lx),int(2*hcwy/wy),int(2*hchz/hz)))
    energyM=np.zeros((int(2*hclx/lx),int(2*hcwy/wy),int(2*hchz/hz)))
    for i in range(0,l):
        data[i]=process_translation(data[i],hchz)   
        data[i]=process_rotation(data[i],theta)
        numMatrix,energyMatrix= process_distribution(data[i],lx,wy,hz,hclx,hcwy,hchz)
        numM+=numMatrix
        energyM+=energyMatrix
    return data,numM,energyM
    
data=np.load('try.npy')
result,numM,energyM=process_run(data,math.pi/4,1,1,1,15,15,5)
np.save('postData.npy',result)
np.save('NumberCollect.npy',numM)
np.save('EnergyDeposition.npy',energyM)
#print(result)
#print(numM)      
#print(energyM)   
