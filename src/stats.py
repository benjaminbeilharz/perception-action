import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def read_data_and_separate(fp: str,
                           conditions: list[int] = [1, 2],
                           phases: list[int] = [2, 3, 4],
                           investigate_participant: str = 'PF23EN',
                           ) -> dict[str, pd.DataFrame]:
    data = pd.read_csv(fp, encoding='utf8', sep='\t')
    dfs = {}
    for condition in conditions:
        for phase in phases:
            tmp = data[data['Condition'] == condition]
            tmp = tmp[tmp['Phase'] == phase]
            dfs[f'c{condition}-p{phase}'] = tmp
            dfs[f'{investigate_participant}-c{condition}-p{phase}'] = tmp[tmp['Subject'] == investigate_participant]

    return dfs

def plots(df: pd.DataFrame,
          x: str,
          y: str,
          row: str = 'Condition',
          col: str = 'Phase',
          fit_reg: bool = True,
          ):
    sns.lmplot(
            data=df,
            x=x,
            y=y,
            row=row,
            col=col,
            fit_reg=fit_reg,
            height=5,
            facet_kws=dict(sharex=True, sharey=False))
    plt.show()


        

        
