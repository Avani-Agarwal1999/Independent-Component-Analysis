import time
import numpy as np
from numpy import linalg as la
from scipy.io import loadmat
import matplotlib.pyplot as plt

def ICA(X, W, ETA=0.000001, MAX_ITER=1000):

    n,m = W.shape
    m,t = X.shape
    
    print(f'Running ICA...')
    print(f'eta={ETA} and R_max={MAX_ITER}')
    
    start_time = time.time()
    for i in range(0, int(MAX_ITER)):
        # Estimate of U
        Y = W@X         # (n,t)

        # find delW
        Z = 1/(1 + np.exp(-Y))   # (n,t)
        delW = ETA*((np.identity(n)*t + (1 - 2*Z)@Y.T) @W)
        
        # update W
        W += delW
    end_time = round(time.time() - start_time, 4)
    print(f'Completed ICA in {end_time} sec')
    
    return W


COLOR = ['b','g','r','c','k']
def plots(A, spacing=None, title=None):   
    
    n,_ = A.shape
    Anorm = norm(A,spacing)
    
    fig = plt.figure(figsize=(16,8))
    ax = plt.gca()
    for i in range(0,n):
        plt.plot(Anorm[i][:40], COLOR[i])
        vis = False if i < n-1 else True
        ax.axes.xaxis.set_visible(vis)
    
    if title: ax.set_title = title
        
    plt.show()

def norm(A,spacing):
    Anorm = []
    
    mi = min(map(min, A))
    ma = max(map(max, A))
    
    s = spacing if spacing is not None else 0
    
    for i in range(len(A)):
        Anorm.append(s*i + (A[i]-mi) / (ma-mi))
        
    return Anorm

def correlation_coefficient(T1, T2):
    numerator = np.mean((T1 - T1.mean()) * (T2 - T2.mean()))
    denominator = T1.std() * T2.std()
    if denominator == 0:
        return 0
    else:
        result = numerator / denominator
        return result

"""# ICA on all 5 signals"""

np.random.seed(8)

# Load data
data = loadmat('sound.mat')['sounds']

U = data[:][:]
n,t = U.shape
m = n

# Mix signals and create W_init
A = np.random.rand(m,n)
X = A@U
W_init = np.random.rand(n,m)
W = ICA(X, W_init/100, ETA=0.000001, MAX_ITER=1000)
rec = W@X

plots(U,0.05)
plots(X,0.05)

r = np.array([rec[1],rec[0],rec[2]])
plots(rec, 0.05)

#above is when you use bottom 3 signals

r=[rec[4],rec[1],rec[2],rec[3],rec[0]]
plots(rec,0.05)
rr=np.array(r)
for i in range(0,5):
  for j in range(0,5):
    print(round(correlation_coefficient(U[i],rr[j]),4))
  print("     ")

"""#ICA on bottom 3 signals

"""

np.random.seed(8)
# Load data
data = loadmat('sound.mat')['sounds']

U = data[:3][:]
n,t = U.shape
m = n

# Mix signals and create W_init
A = np.random.rand(m,n)
X = A@U
W_init = np.random.rand(n,m)
W = ICA(X, W_init/100, ETA=0.000001, MAX_ITER=1000)
rec = W@X
plots(U,0.05)
plots(X,0.05)
r = np.array([rec[1],rec[0],rec[2]])
plots(rec, 0.05)

rr=np.array(r)
for i in range(0,3):
  for j in range(0,3):
    print(round(correlation_coefficient(U[i],rr[j]),4))
  print("     ")

n = 3
m = 3
U = data[:n,:]

R_max_TEST_results = []
c=[]
c1=[]
c2=[]
np.random.seed(8)
A = np.random.rand(m,n)
W_init = np.random.rand(n,m)
X = A@U
R_max_trials = np.array([100,200,300,400,500,600,700,800,900,1000])
for R_max in R_max_trials:
    W = ICA(X, W_init, ETA=0.000001, MAX_ITER=R_max)
    rec = W@X
    r=[rec[1],rec[0],rec[2]]
    rr=np.array(r)
    R_max_TEST_results.append(rr)
    print(round(correlation_coefficient(U[0],rr[0]),3))
    print(round(correlation_coefficient(U[1],rr[1]),3))
    print(round(correlation_coefficient(U[2],rr[2]),3))

#best value of m
np.random.seed(8)

n = 5
U = data[:n,:]

m_TEST_results = []
m_TEST_errors = []

for m in range(n,20):
    print(f'm={m}')

    A = np.random.rand(m,n)
    W_init = np.random.rand(n,m)

    X = A@U
    W = ICA(X, W_init, ETA=0.000001, MAX_ITER=1000)

    rec = W@X
    m_TEST_results.append(rec)

    error = la.norm(rec-U,2)
    m_TEST_errors.append(error)
    print(f'Error: {error}\n')
fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(range(5,20), m_TEST_errors)
ax.set_title('eta=1e-6, R_max=1000')
ax.set_xlabel('m')
ax.set_ylabel('norm error')

plt.show()

np.random.seed(8)
U = loadmat('icaTest.mat')['U']
A = loadmat('icaTest.mat')['A']

m,n = A.shape
X = A@U
# ICA
W_init = np.random.rand(n,m)
W = ICA(X, W_init, ETA=0.01, MAX_ITER=1000000)

#Recovered_signals
rec = W@X

e = la.norm(rec-U,2)
print('Error is equal to', e)

plots(U, 1)
print("Original signals are displayed above")
plots(X, 1)
print("Mixed signals are displayed above")

r = np.array([rec[0],rec[2],-rec[1]])
plots(r, 1)
print("Recovered signals are displayed above")

for i in range(0,3):
  c = correlation_coefficient(U[i],r[i])
  print(round(c,4))