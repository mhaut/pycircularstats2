import numpy as np


for fff in ["datos2cartesian.txt", "datos4cartesia.txt", "datos500cartesia.txt", "vientos_cartesiana1000.txt"]:
    datas = np.loadtxt(fff, delimiter='\t')
    data2 = np.zeros(datas.shape)
    data2[:,0] = datas[:,2]
    data2[:,1] = datas[:,3]
    data2[:,2] = datas[:,0]
    data2[:,3] = datas[:,1]
    np.savetxt("okD/"+fff, data2, delimiter='\t')
