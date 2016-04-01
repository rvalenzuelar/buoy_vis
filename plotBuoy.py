
import Meteoframes as mf
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import seaborn as sns

sns.set_color_codes()

''' from north to south '''

base_folder = '/home/rvalenzuela/BUOY/'
# base_folder='/Users/raulv/Documents/BUOY/'
usr_case = raw_input('Indicate case (i.e. 3): ')
scase = 'case'+usr_case.zfill(2)

if usr_case == '3':
    st = datetime.datetime(2001, 1, 23, 0, 0)
    en = datetime.datetime(2001, 1, 25, 0, 0)
elif usr_case == '4':
    st = datetime.datetime(2001, 1, 25, 0, 0)
    en = datetime.datetime(2001, 1, 27, 0, 0)
elif usr_case == '5':
    st = datetime.datetime(2001, 2, 9, 0, 0)
    en = datetime.datetime(2001, 2, 11, 0, 0)
elif usr_case == '6':
    st = datetime.datetime(2001, 2, 11, 0, 0)
    en = datetime.datetime(2001, 2, 12, 0, 0)
elif usr_case == '7':
    st = datetime.datetime(2001, 2, 17, 0, 0)
    en = datetime.datetime(2001, 2, 18, 0, 0)
elif usr_case == '8':
    st = datetime.datetime(2003, 1, 12, 0, 0)
    en = datetime.datetime(2003, 1, 14, 0, 0)
elif usr_case == '9':
    st = datetime.datetime(2003, 1, 21, 0, 0)
    en = datetime.datetime(2003, 1, 23, 0, 0)
elif usr_case == '10':
    st = datetime.datetime(2003, 2, 15, 0, 0)
    en = datetime.datetime(2003, 2, 17, 0, 0)
elif usr_case == '11':
    st = datetime.datetime(2004, 1, 8, 0, 0)
    en = datetime.datetime(2004, 1, 11, 0, 0)
elif usr_case == '12':
    st = datetime.datetime(2004, 2, 1, 0, 0)
    en = datetime.datetime(2004, 2, 3, 0, 0)
elif usr_case == '13':
    st = datetime.datetime(2004, 2, 16, 0, 0)
    en = datetime.datetime(2004, 2, 18, 0, 0)
elif usr_case == '14':
    st = datetime.datetime(2004, 2, 24, 0, 0)
    en = datetime.datetime(2004, 2, 26, 0, 0)


buoyfiles = [base_folder + scase + '/46014c'+str(st.year)+'.txt',
             base_folder + scase + '/46013c'+str(st.year)+'.txt',
             base_folder + scase + '/46026c'+str(st.year)+'.txt',
             base_folder + scase + '/46012c'+str(st.year)+'.txt']

fig, ax = plt.subplots(len(buoyfiles), 1, figsize=(13, 10), sharex=True)
buoylats = {'B14': '39.24', 'B13': '38.24', 'B26': '37.75', 'B12': '37.36', }


def make_quiver(ax):
    """ make quiver plot for each file """
    for i, f in enumerate(buoyfiles):
        df = mf.parse_buoy(f)
        df2 = df[st:en]
        time = df2.index[::2]
        wspd = df2.SPD[::2]
        wdir = df2.DIR[::2]

        X = np.asarray(range(len(wspd)))
        Y = np.zeros(len(wspd))
        U = np.asarray(-wspd*np.sin(wdir*np.pi/180.))
        V = np.asarray(-wspd*np.cos(wdir*np.pi/180.))

        if len(time) > 0:
            ntime = len(time)
            xticks = range(0, ntime, 18)
            xticklabels = time[xticks]
            date_fmt = '%d\n%H'
            xtlabels = [t.strftime(date_fmt) for t in xticklabels]

            Q = ax[i].quiver(
                X, Y, U, V, width=0.002, facecolor='b', edgecolor='k', headwidth=3)
            if i == 0:
                ax[i].quiverkey(Q, 0.9, 0.1, 10,
                                r'$10 \frac{m}{s}$',
                                fontproperties={'weight': 'bold', 'size': 14})

            ax[i].set_xticks(xticks)
            ax[i].set_xticklabels(xtlabels)
            ax[i].invert_xaxis()
            ax[i].set_xlim([ntime+5, -5])
            ax[i].set_ylim([-0.02, 0.02])
            filename = os.path.basename(f)
            buoyname = 'B'+filename[3:5]
            degree_sign = u'\N{DEGREE SIGN}'
            atext = buoyname+' - '+buoylats[buoyname]+degree_sign+'N'
            ax[i].text(0.05, 0.1, atext, transform=ax[i].transAxes, fontsize=14,
                       verticalalignment='bottom')
        else:
            ax[i].text(
                0.5, 0.5, 'NO DATA', weight='bold', transform=ax[i].transAxes)
            filename = os.path.basename(f)
            buoyname = 'B'+filename[3:5]
            atext = buoyname+' - '+buoylats[buoyname]+degree_sign+'N'
            ax[i].text(0.05, 0.1, atext, transform=ax[i].transAxes, fontsize=14,
                       verticalalignment='bottom')

        ax[i].set_yticklabels([''])

        plt.draw()
        # return Q

make_quiver(ax)
ax[3].set_xlabel(r'$\Leftarrow$'+' Time [UTC]')
t = 'Wind vectors from NOAA buoys\nCase{} Date: {}'
plt.suptitle(t.format(usr_case.zfill(2), st.strftime('%Y-%m')))
plt.show(block=False)
