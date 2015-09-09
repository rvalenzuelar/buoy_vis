
import Meteoframes as mf
import numpy as np 
import matplotlib.pyplot as plt 
import datetime
import os
import seaborn as sns

sns.set_color_codes()

''' from north to south '''
buoyfiles = ['/home/rvalenzuela/BUOY/case03/46014c2001.txt',
			'/home/rvalenzuela/BUOY/case03/46013c2001.txt',
			'/home/rvalenzuela/BUOY/case03/46026c2001.txt',
			'/home/rvalenzuela/BUOY/case03/46012c2001.txt']

st = datetime.datetime(2001, 1, 23, 0, 0)
en = datetime.datetime(2001, 1, 25, 0, 0)
fig,ax = plt.subplots(len(buoyfiles),1,figsize=(13,10),sharex=True)
buoylats={'B14':'39.24', 'B13':'38.24', 'B26':'37.75', 'B12':'37.36',}

def make_quiver(ax):
	""" make quiver plot for each file """
	for i,f in enumerate(buoyfiles):

		df=mf.parse_buoy(f)
		df2=df[st:en]
		time = df2.index
		wspd = df2.SPD
		wdir = df2.DIR

		X=np.asarray(range(len(wspd)))
		Y=np.zeros(len(wspd))
		U=np.asarray(-wspd*np.sin(wdir*np.pi/180.))
		V=np.asarray(-wspd*np.cos(wdir*np.pi/180.))

		xticks=range(0,len(time),18)
		xticklabels=df2.index[xticks]
		date_fmt='%H\n%d'
		xtlabels=[t.strftime(date_fmt) for t in xticklabels]

		Q=ax[i].quiver(X,Y,U,V,width=0.002,color='b')
		if i == 0:
			ax[i].quiverkey(Q, 0.9, 0.1, 10, 
							r'$10 \frac{m}{s}$',
							fontproperties={'weight': 'bold','size':14})
		if i	== len(buoyfiles)-1:
			ax[i].set_xlabel(r'$\Leftarrow$'+' Time [UTC]')	
		ax[i].set_xticks(xticks)
		ax[i].set_xticklabels(xtlabels)
		ax[i].invert_xaxis()
		ax[i].set_xlim([len(time),-10])
		ax[i].set_ylim([-0.02,0.02])
		ax[i].tick_params(
			axis='y',          # changes apply to the x-axis
			which='both',      # both major and minor ticks are affected
			left='off',      # ticks along the bottom edge are off
			right='off',         # ticks along the top edge are off
			labelleft='off') # labels along the bottom edge are off
		filename=os.path.basename(f)
		buoyname='B'+filename[3:5]
		degree_sign= u'\N{DEGREE SIGN}'
		atext=buoyname+'\n'+buoylats[buoyname]+degree_sign+'N'
		ax[i].text(0.05, 0.95, atext, transform=ax[i].transAxes, fontsize=14,
					verticalalignment='top')		
		plt.draw()

make_quiver(ax)
plt.suptitle('Wind vectors from NOAA buoys')
plt.show()
