import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
#from matplotlib import ticker, cm
import matplotlib as mpl

def lws_rbspice_loss_function_history(history,figname="tmp",ylim=[0,1]):
    fig1=plt.figure(figsize=(10, 8),facecolor='w')
    ax1=fig1.add_subplot(1,1,1)
    ax1.plot(pd.DataFrame(history.history))
    ax1.grid(True)
    plt.gca().set_ylim(ylim[0],ylim[1])
    fontsize1=20
    ax1.set_xlabel("Epoches",fontsize=fontsize1)
    ax1.set_ylabel("Loss",fontsize=fontsize1)
    ax1.legend(["Train","Validation"],fontsize=fontsize1)
    ax1.tick_params(axis='both', which='major', labelsize=fontsize1)
    ax1.tick_params(axis='both', which='minor', labelsize=fontsize1)
    #ax1.set_facecolor((1.0, 1.0,1.0))
    plt.savefig(figname+".png", format="png", dpi=300)
    plt.show()


def lws_rbspice_correlation(y_test_reshaped, y_test_pred_reshaped, xrange=[4,9],figname="tmp",ek="148"):
    
    #y_test_pred = model.predict(X_test)

    #y_test_reshaped=y_test.reshape([-1])
    #y_test_pred_reshaped=y_test_pred.reshape([-1])
    corr = r2_score(y_test_reshaped, y_test_pred_reshaped)
    #corr1, _ = scipy.stats.pearsonr(y_test_reshaped, y_test_pred_reshaped)
    #corr2, _ = scipy.stats.spearmanr(y_test_reshaped, y_test_pred_reshaped)
    
    print(y_test_reshaped.shape)
    mse_test1=sum((y_test_pred_reshaped-y_test_reshaped)**2)/len(y_test_reshaped)
    print(mse_test1)
    
    #Plot data vs model predictioin
    dx=0.05
    yrange=xrange
    dy=dx
    NX=int((xrange[1]-xrange[0])/dx)
    NY=int((yrange[1]-yrange[0])/dy)
    M_test=np.zeros([NX,NY],dtype=np.int16)

    for k in range(y_test_reshaped.size):
        xk=(y_test_reshaped[k]-xrange[0])/dx
        yk=(y_test_pred_reshaped[k]-yrange[0])/dy
        xk=min(xk,NX-1)
        yk=min(yk,NY-1)
        xk=int(xk)#xk.astype(int)
        yk=int(yk)
        M_test[xk,yk]+=1


    delta = dx
    extent = (xrange[0], xrange[1], yrange[0], yrange[1])

    x = np.arange(xrange[0], xrange[1], delta)
    y = np.arange(yrange[0], yrange[1], delta)
    X, Y = np.meshgrid(x, y)

    # Boost the upper limit to avoid truncation errors.
    levels = np.arange(0, M_test.max(), 200.0)

    norm = mpl.cm.colors.Normalize(vmax=M_test.max(), vmin=M_test.min())
    #cmap = cm.PRGn
    cmap = mpl.cm.jet

    fig2=plt.figure(figsize=(10, 8),facecolor='w')
    ax1=fig2.add_subplot(1,1,1)

    im = ax1.imshow(M_test.transpose(),  cmap=mpl.cm.jet,interpolation='none',#'bilinear',
                origin='lower', extent=[xrange[0],xrange[1],yrange[0],yrange[1]],
                vmax=M_test.max(), vmin=-M_test.min())


    ax1.plot(xrange,yrange,'r')

    ax1.set_title('Proton '+ek+' keV',fontsize=20)
    ax1.set_xlabel("log measured flux",fontsize=20)
    ax1.set_ylabel("log predicted flux",fontsize=20)
    #ax1.set_facecolor('xkcd:salmon')
    #ax1.set_facecolor((0.2, 0.6,1.0))
    plt.text(7,4.4,('R2: %(corr)5.3f' %{"corr": corr}),color='w',fontsize=20)
    plt.text(7,5,('mse_test:%(mse_test)5.3f' %{"mse_test":mse_test1}),color='w',fontsize=20)

    # We change the fontsize of minor ticks label 
    ax1.tick_params(axis='both', which='major', labelsize=16)
    ax1.tick_params(axis='both', which='minor', labelsize=12)

    #plt.axis('equal')
    plt.xlim(xrange[0],xrange[1])
    plt.ylim(yrange[0],yrange[1])
    cbar=fig2.colorbar(im, ax=ax1)
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label('# of samples', fontsize=20)
    plt.savefig(figname+".png", format="png", dpi=300)
    plt.show()
