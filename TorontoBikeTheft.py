#Libraries 
#pip install pygsp if you don't already have it
from pygsp import graphs, filters

#Data imports
path = 'C:/Users/jwill/Downloads'
#Bike thefts, need to set path to reflect this 
bt = pd.read_csv('C:/Users/jwill/Downloads/bicycle-thefts.csv')
#Toronto network, need to set path to reflect this
mat = scipy.io.loadmat(path+'/toronto.mat')

#Create the graph of the Toronto Network 
coords = mat['G'][0][0][1]
G = graphs.Path(2202)
G.set_coordinates(mat['G'][0][0][1])

#Scrape up the lat long data from the Toronto open source theft data
BTDist = []; 
for i in range(10000):
    lat = bt['geometry'][i].find('-');
    long = bt['geometry'][i].find(' 4')+1;
    BTDist.append([bt['geometry'][i][lat:lat+8], bt['geometry'][i][long: long+7]])

#Find the closes interesection on the Toronto Road Network to the location of the bike theft 
BTDist = np.asarray(list(BTDist),dtype='float')
mini = []
for i in range(np.shape(BTDist)[0]): 
    smini = 900
    for j in range(np.shape(Coords)[0]): 
        smin = math.dist(Coords[j],BTDist[i])
        if smin < smini:  
            smini = smin
            sminiL = j
    mini.append(sminiL)
    
#Generate a signal from the bike theft data to overlay on the graph 
f = np.zeros(np.shape(Coords)[0])
for i in range(np.size(mini)):
    f[mini[i]] = f[mini[i]] + 1

#Graph the signal 
G.plot_signal(f)

#Wavelet transform (consider incorporating different thresholding techniques here
#Meyer graph wavelet has the tightframe property 
g = filters.Meyer(G, Nf = 4)
c = g.analyze(f)
#Call threhsolding techniques here (SureShrink is used for graph wavelet thresholding in (deLoynes et al. 2020))
G.plot_signal(g.synthesize(c))

