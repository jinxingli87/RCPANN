import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as figure
from rcpann import *


import typing
import funix 

@funix.funix(
    description="The RCPANN model produce the ring current proton fluxes. This example shows how to provide default and candiadate/example values for UI widgets. For default values, simpliy take advantage of Python's default value syntax for keyword arguments. For example values, use the `example` parameter in Funix. ",
    argument_labels={
        "iek": "Energy index",
        "tstr1": "Date and Time in formate of 'yyyy-mm-dd hh:mm:ss'",
        "tstr2": "Date and Time in formate of 'yyyy-mm-dd hh:mm:ss'",
    },
    show_source=True,
)




def rc_global_dist(
    iek  :   int=1,
    tstr1:   str = '2017-03-01 22:42:00',
    tstr2:   str = '2017-03-04 22:42:00')->figure.Figure:
    

    indt1_symh=np.where(df_symh['Datetime'] >= tstr1)
    indt1_symh=indt1_symh[0][0]
    indt2_symh=np.where(df_symh['Datetime'] >= tstr2)
    indt2_symh=indt2_symh[0][0]+1
    tarr_dt=df_symh['Datetime'].astype('datetime64[ns]')[indt1_symh:indt2_symh].reset_index(drop=True)

    xrange=[-6.5,6.5]
    yrange=xrange.copy()
    delta = 0.1
    NX=int((xrange[1]-xrange[0])/delta)
    NY=int((yrange[1]-yrange[0])/delta)
    extent = (xrange[0], xrange[1], yrange[0], yrange[1])
    x = np.arange(xrange[0], xrange[1], delta)
    y = np.arange(yrange[0], yrange[1], delta)
    XX, YY = np.meshgrid(x, y)

    XX_flat=XX.flatten()
    YY_flat=YY.flatten()
    RR_flat=np.sqrt(XX_flat**2+YY_flat**2)
    sint_flat = -YY_flat/RR_flat #Since we defined sint = sin(MLT/12*!pi)
    cost_flat = -XX_flat/RR_flat
    LAT_flat = XX_flat*0.0

    coord_glb=np.concatenate((RR_flat.reshape([-1,1]),cost_flat.reshape([-1,1]),sint_flat.reshape([-1,1]),LAT_flat.reshape([-1,1])), axis=1)
    y_pred_matrix=pflux(iek,coord_glb,tstr = tstr1)




    # Visualize the global distribution of ion fluxes
    extent = (xrange[0], xrange[1], yrange[0], yrange[1])
    x = np.arange(xrange[0], xrange[1], delta)
    y = np.arange(yrange[0], yrange[1], delta)
    X, Y = np.meshgrid(x, y)
    vmax=9.0
    vmin=5.0
    norm = mpl.cm.colors.Normalize(vmax=vmax, vmin=vmin)
    cmap = mpl.cm.jet

    mpl.rcParams['pdf.fonttype']=42
    mpl.rcParams['ps.fonttype']=42

    ax_x0=0.2
    ax_dx=0.7
    ax_dy=0.10
    ax_dy_1=0.097
    ax_y0=0.55

    k=0

    tbar=tarr_dt[k]
    fig4=plt.figure(figsize=(8,8),facecolor='white')   

    n_fig=4
    #fig = plt.figure(figsize=(18, 14),facecolor='white')   
    fs_label=12
    fs_major=12
    fs_minor=9

    ax1=fig4.add_subplot(n_fig,1,1)
    ax1.set_position([ax_x0,ax_y0+3*ax_dy,ax_dx,ax_dy_1])
    ax1.plot(tarr_dt,df_symh['SymH'][indt1_symh:indt2_symh],'k')
    y_min, y_max = ax1. get_ylim()
    ax1.plot([tbar,tbar],[y_min,y_max],':g')
    ax1.set_ylabel("Sym-H (nT)",fontsize=fs_label)
    ax1.tick_params(axis='x',labelbottom=False) # labels along the bottom edge are off

    ax1.xaxis.set_major_locator(mpl.dates.DayLocator())
    ax1.xaxis.set_minor_locator(mpl.dates.HourLocator())
    ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m-%d'))
    ax1.tick_params(axis='both', which='major', labelsize=fs_major)
    ax1.tick_params(axis='both', which='minor', labelsize=fs_minor)

    ax2=fig4.add_subplot(n_fig,1,2)
    ax2.set_position([ax_x0,ax_y0+2*ax_dy,ax_dx,ax_dy_1])
    ax2.plot(tarr_dt,df_symh['AsyH'][indt1_symh:indt2_symh],'k')
    ax2.plot(tarr_dt,df_symh['AsyD'][indt1_symh:indt2_symh],'r')
    y_min, y_max = ax2. get_ylim()
    ax2.plot([tbar,tbar],[y_min,y_max],':g')
    ax2.set_ylabel("Asym (nT)",fontsize=fs_label)
    ax2.tick_params(axis='x', labelbottom=False) # labels along the bottom edge are off

    ax2.xaxis.set_major_locator(mpl.dates.DayLocator())
    ax2.xaxis.set_minor_locator(mpl.dates.HourLocator())
    ax2.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m-%d'))
    ax2.tick_params(axis='both', which='major', labelsize=fs_major)
    ax2.tick_params(axis='both', which='minor', labelsize=fs_minor)
    ax2.legend(('AsyH', 'AsyD'), loc='upper right',fontsize=fs_label)

    ax3=fig4.add_subplot(n_fig,1,3)
    ax3.set_position([ax_x0,ax_y0+1*ax_dy,ax_dx,ax_dy_1])
    ax3.plot(tarr_dt,df_symh['SME'][indt1_symh:indt2_symh],'k')
    y_min, y_max = ax3. get_ylim()
    ax3.plot([tbar,tbar],[y_min,y_max],':g')
    ax3.set_ylabel("SME (nT)",fontsize=fs_label)

    ax3.xaxis.set_major_locator(mpl.dates.DayLocator())
    ax3.xaxis.set_minor_locator(mpl.dates.HourLocator())
    ax3.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m-%d'))
    ax3.tick_params(axis='both', which='major', labelsize=fs_major)
    ax3.tick_params(axis='both', which='minor', labelsize=fs_minor)

    #Subfigure 4

    y_pred_matrix=y_pred_matrix[:,0].reshape([NX,NY])

    ax0=fig4.add_subplot(5,1,5)
    ax0.set_position([0.25,0.08,0.5,0.5])
    im = ax0.contourf(X, Y, y_pred_matrix,  256,cmap=mpl.cm.jet,vmax=vmax,vmin=vmin)

    #Set L>6.5 and L<2 blank
    theta2=np.arange(0,2.01*np.pi,0.02)
    r2=np.arange(6.5,9.5,0.1)
    R,THETA=np.meshgrid(r2,theta2)
    X2=R*np.cos(THETA)
    Y2=R*np.sin(THETA)
    im3=ax0.contourf(X2,Y2,X2*0+1.0,10,cmap=mpl.cm.cubehelix,vmax=1.0,vmin=0.0)
    r2=np.arange(0.0,2.0,0.1)
    R,THETA=np.meshgrid(r2,theta2)
    X2=R*np.cos(THETA)
    Y2=R*np.sin(THETA)
    im4=ax0.contourf(X2,Y2,X2*0+1.0,10,cmap=mpl.cm.cubehelix,vmax=1.0,vmin=0.0)

    #Add Earth
    theta=np.arange(0,2.01*np.pi,0.1)
    ax0.plot(np.cos(theta),np.sin(theta),'k')
    r=np.arange(0,1.1,0.1)
    theta1=np.arange(0.5*np.pi,1.5*np.pi,0.02)
    R,THETA=np.meshgrid(r,theta1)
    X1=R*np.cos(THETA)
    Y1=R*np.sin(THETA)
    im2=ax0.contourf(X1,Y1,X1*0+0.0,10,cmap=mpl.cm.cubehelix,vmax=1.0,vmin=0.0)
    #Add 0, 6, 12, 18 sectors and L=4,6
    ax0.plot([-6,6],[0,0],':k',linewidth=1)
    ax0.plot([0,0],[-6,6],':k',linewidth=1)
    ax0.plot(6*np.cos(theta),6*np.sin(theta),':k')
    ax0.plot(4*np.cos(theta),4*np.sin(theta),':k')

    #ax0.set_title('Proton 7.1 keV',fontsize=20)
    ax0.set_xlabel("X_sm",fontsize=fs_label)
    ax0.set_ylabel("Y_sm",fontsize=fs_label)
    ax0.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax0.xaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax0.tick_params(axis='both', which='major', labelsize=fs_label)
    ax0.tick_params(axis='both', which='minor', labelsize=fs_label)
    plt.axis('equal')
    ax0.set_xlim([-6.5,6.5])
    ax0.set_ylim(-6.5,6.5)
    ax0.invert_xaxis()
    ax0.invert_yaxis()

    # Add colorbar
    cax = plt.axes([0.8, 0.08, 0.01, 0.5])
    cbar=plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax0,cax=cax)
    cbar.ax.tick_params(labelsize=fs_label)
    cbar.set_label('log proton flux '+ekArr[iek]+' keV', fontsize=fs_label)
    ax0.set_title(tbar.strftime("%Y-%m-%d %H:%M"),fontsize=fs_label)
    #plt.show()
    return fig4
