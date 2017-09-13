import matplotlib.pyplot as plt
import numpy as np
def histdraw(b,c,e,label=''):
    #plt.figure(figsize=(8, 6))
    #y=np.concatenate(([0],c))
    #plt.step(b,y,label=label)
    
    #dx=(b[1]-b[0])/2
    x=(b[1:]+b[:-1])/2
    plt.errorbar(x, c, yerr=e, fmt='o',label=label)
    plt.xlim((min(b),max(b)))

def hist(d,bins=20,plot=False,norm=False,label=''):
    #plt.figure(figsize=(8, 6))
    c,b = np.histogram(d,bins=bins,normed=norm)#plt.hist(d,bins=bins,alpha=0.5, fill = None, histtype = 'step')
    e=np.sqrt(c)
    if plot:
        histdraw(b,c,e,label)
    return b,np.asfarray(c),e
def ploteffpur(Vt,Yp,Yt,th,bins=5):
    b,cbdt=hist(A_test[(Yp>th) & (Yt==1)],bins=bins)
    b,ccor=hist(A_test[(Yt==1)],bins=bins)
    b,cbdtall=hist(A_test[(Yp>th)],b)
    histdraw(b,cbdt/cbdtall,label='purity')
    histdraw(b,cbdt/ccor,label='efficiency')
    plt.legend(loc=0)
    
def histratiobinomial(h1,h2,label=''):
    b1,c1,e1 = h1
    b2,c2,e2 = h2
    if (not np.array_equal(b1,b2)):
        print("Bin bondaries do not coincide!")
        return
    r = np.zeros_like(c1)
    nonzero = np.where(c2!=0)
    r[nonzero]=c1[nonzero]/c2[nonzero]

    #TMath::Abs( ( (1. - 2.* b1 / b2) * e1sq  + b1sq * e2sq / b2sq ) / b2sq );
    e1sq=e1*e1
    e2sq=e2*e2
    c1sq=c1*c1
    c2sq=c2*c2
    e=np.zeros_like(c1)
    e[nonzero]=np.sqrt(np.abs( ( (1. - 2.* c1[nonzero] / c2[nonzero]) * e1sq[nonzero]  + 
                      c1sq[nonzero] * e2sq[nonzero] / c2sq[nonzero] ) / c2sq[nonzero] ))
    histdraw(b1,r,e,label)

def drawhistratio(label,var, num, denom, bins):
    n     = hist(var[num].values,bins=bins)
    d     = hist(var[denom].values,bins=bins)
    histratiobinomial(n,d,label=label)