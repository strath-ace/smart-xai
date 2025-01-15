import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

def violin_chart(plot_data, plot_label, fig_name, fig_subtitle):


    # print(plot_data.columns)
    # plotol = fig.add_subplot(grid[0, 0])
    fig = sns.barplot( data=plot_data,x = "Assessment", y ="Score", hue='Average Correctness', split=True, inner="quart", )

    plt.show()

if __name__ == "__main__":
    plot_data = pd.read_csv("Iterations_code_gen.csv")
    # plot_data = pd.DataFrame(pl_data).transpose()
    # plot_data.columns = ['Swap_actions', 'Single_Substitution', 'Verification', 'Forward_Backward']
    fig_subtitle = "Assessment_Scores"
    plot_label = 'Scores'
    fig_name = "Assessment_Scores.png"
    violin_chart(plot_data, plot_label, fig_name, fig_subtitle)

