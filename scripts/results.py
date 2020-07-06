import numpy as np
import matplotlib.pyplot as plt
from bqplot import *
import sys
sys.path.append("..") # Adds higher directory to python modules path
from utils import utils

def display_graph(asset_name, year):
    
    #inizialize the plot
    #fig_hist = Figure()
    
    glad_dir = utils.create_result_folder()
    aoi_name = utils.set_aoi_name(asset_name) 
    alert_stats = glad_dir + "stats_glad_" + year + "_" + aoi_name + ".txt"
    
    data = np.loadtxt(alert_stats, delimiter=' ')
    
    bins=30

    #need to confirm who's who
    Y_conf = data[:,5]
    Y_conf = np.ma.masked_equal(Y_conf,0).compressed()
    maxY5 = np.amax(Y_conf)

    #null if all the alerts have been confirmed
    Y_prob = data[:,4]
    Y_prob = np.ma.masked_equal(Y_prob,0).compressed()
    try:
        maxY4 = np.amax(Y_prob)
        data_hist = [Y_conf, Y_prob]
        colors = ["#C26449", "#59C266"]
        labels = ['confirmed alert', 'potential alert']
    except ValueError:  #raised if `Y_prob` is empty.
        maxY4 = 0
        data_hist = [Y_conf]
        colors = ["#C26449"]
        labels = ['confirmed alert']
        pass
    
    #plot in kilometers ?
    
    hist_y, hist_x = np.histogram(Y_conf, bins=30, weights=Y_conf)
    
    x_sc = LinearScale()
    #y_sc = LogScale()
    y_sc = LinearScale()

    bar = Bars(x=hist_x, y=hist_y, scales={'x': x_sc, 'y': y_sc})
    ax_x = Axis(label='patch size (px)', scale=x_sc)
    ax_y = Axis(label='number of pixels', scale=y_sc, orientation='vertical')

    fig_hist = Figure(
        title='Distribution of GLAD alerts for {0} in {1}'.format(aoi_name, year), 
        marks=[bar], 
        axes=[ax_x, ax_y], 
        padding_x=0.025, 
        padding_y=0.025
    )
    
    fig_hist.layout.width = 'auto'
    fig_hist.layout.height = 'auto'
    fig_hist.layout.min_width = "300px"
    fig_hist.layout.min_height = '300px' # so it still shows nicely in the notebook


    #plt.hist(
    #    data_hist, 
    #    label=labels, 
    #    weights=data_hist,color=colors, 
    #    bins=bins, 
    #    density=True, 
    #    histtype='bar', 
    #    stacked=True
    #)
    #plt.xlim(0, max(maxY5, maxY4))
    #plt.yscale('log')
    #plt.legend(loc='upper right')
    #plt.title('Distribution of GLAD alerts for '+ aoi_name + " in " + year)
    #plt.xlabel('patch size (px)')
    #plt.ylabel('number of pixels (log)')
    #plt.show()
    
    return fig_hist