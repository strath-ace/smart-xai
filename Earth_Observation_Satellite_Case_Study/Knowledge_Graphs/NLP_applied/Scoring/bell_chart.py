# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This file creates bell plots for plotting word count
# ===========================================================================================================


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def bell_chart(plot_data, plot_label, fig_name, fig_subtitle):

# plot_data = pd.read_csv("Swap_actions.csv")
    print(plot_data)
    fig, axs = plt.subplots(ncols=1)
    for i in plot_data.columns:
        sns.kdeplot(data=plot_data, x=plot_data.loc[:, str(i)], label=str(i))
    fig.figure.suptitle(fig_subtitle, fontsize = 10)
    plt.xlabel(plot_label)
    plt.ylim(0, 0.025)
    plt.xlim(-100, 600)
    # sns.boxplot(x='education',y='wage', data=tips2, ax=axs[2])
    plt.legend()
    plt.savefig(fig_name)
    plt.show()

if __name__ == "__main__":
    # plot_data = pd.read_csv("Swap_actions.csv")
    pl_data = [[ 0.6507444444, 0.6154777778, 0.6117, 0.6763611111, 0.6598222222, 0.5436111111, 0.5629611111,
      0.6517222222, 0.6069444444, 0.6974944444, 0.6215, 0.5181666667, 0.70395, 0.6097444444, 0.5650777778, 0.4788888889,
      0.5762666667, 0.7246666667, 0.6480333333, 0.6632263158],
     [ 0.6460736842, 0.6510815789, 0.5478175439, 0.5384776316, 0.5211610526, 0.545954386,
      0.5598834586, 0.5713335526, 0.5769555556, 0.5672052632, 0.5691822967, 0.5750320175, 0.5746554656, 0.5786721805,
      0.5726961404, 0.5782032895, 0.5719972136, 0.5740479532, 0.5754036011, 0.5734573684],
     [ 0.3955789474, 0.4672657895, 0.4755929825, 0.5012315789, 0.5277547368, 0.5377315789, 0.5473142857,
      0.5560164474, 0.5636099415, 0.5679452632, 0.5571124402, 0.5630697368, 0.5643526316, 0.5664045113, 0.5564091228,
      0.5597460526, 0.5601532508, 0.5577938596, 0.5592822715, 0.5599752632],
     [ 0.5372526316, 0.5554789474, 0.5210263158, 0.5108960526, 0.5170010526, 0.5186061404,
      0.5280894737, 0.5367460526, 0.534797076, 0.5429984211, 0.5488488038, 0.5513442982, 0.5517024291, 0.5543176692,
      0.5554863158, 0.5573976974, 0.5483052632, 0.4801052632, 0.5156315789, 0.5370486842]]
    plot_data = pd.DataFrame(pl_data).transpose()
    plot_data.columns = ['Swap_actions', 'Single_Substitution', 'Verification', 'Forward_Backward']
    fig_subtitle = "Cosine Similarity"
    plot_label = 'Cosine Similarity'
    fig_name = "Q_Cosine_Similarity.png"
    bell_chart(plot_data, plot_label, fig_name, fig_subtitle)

