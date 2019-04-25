
from tqdm import tqdm
import torch
import pandas as pd
import stable_nalu
import argparse
import numpy as np

pd.options.display.max_rows = 1000

# Parse arguments
parser = argparse.ArgumentParser(description='Export results from simple function task')
parser.add_argument('--dir',
                    action='store',
                    default='tensorboard/simple_function_static',
                    type=str,
                    help='Specify the directory for which the data is stored')
args = parser.parse_args()

"""
data = []
for dirname, losses, last_step in tqdm(stable_nalu.reader.TensorboardFinalReader(args.dir)):
    model, operation, seed = dirname.split('_')
    row = {
        'model': model,
        'operation': operation,
        'seed': seed,
        **losses,
        'step': last_step
    }
    data.append(row)

data_df = pd.DataFrame.from_records(
    data,
    columns=[
        'model', 'operation', 'seed', 'step',
        'loss/train', 'loss/valid/interpolation', 'loss/valid/extrapolation'
    ]
)
data_df.to_pickle('debug_simple_function_static.pkl')
"""
#data_df = pd.read_pickle('debug_simple_function_static.pkl')

# Compute baselines
baselines = []
for operation in tqdm(['add', 'sub', 'mul', 'div', 'squared', 'root']):
    for seed in range(10):
        dataset = stable_nalu.dataset.SimpleFunctionStaticDataset(
            operation=operation,
            seed=seed
        )

        baselines.append({
            'operation': operation,
            'seed': str(seed),
            'problem': dataset.print_operation(),
            'baseline/interpolation': np.sqrt(dataset.fork(input_range=1).baseline_error(batch_size=2048)),
            'baseline/extrapolation': np.sqrt(dataset.fork(input_range=5).baseline_error(batch_size=2048))
        })

baselines_df = pd.DataFrame.from_records(baselines)
print(baselines_df)

"""
df = pd.merge(data_df, baselines_df, how='left', on=['operation', 'seed'])
df['loss/norm/train'] = df['loss/train'] / df['baseline/interpolation']
df['loss/norm/valid/interpolation'] = df['loss/valid/interpolation'] / df['baseline/interpolation']
df['loss/norm/valid/extrapolation'] = df['loss/valid/extrapolation'] / df['baseline/extrapolation']

df['success/interpolation'] = df['loss/norm/valid/interpolation'] < 0.1 / 100
df['success/extrapolation'] = df['loss/norm/valid/extrapolation'] < 0.1 / 100

agg_df = df.groupby(['model', 'operation']).agg({
    'success/interpolation': 'mean',
    'success/extrapolation': 'mean',
    'loss/norm/valid/interpolation': 'mean',
    'loss/norm/valid/extrapolation': 'mean',
    'seed': 'count'
})
print(agg_df)

latex_df = agg_df.copy()
del latex_df['seed']
del latex_df['loss/norm/valid/interpolation']
del latex_df['loss/norm/valid/extrapolation']
latex_df = latex_df.reset_index()
latex_df = pd.melt(latex_df, id_vars=['model', 'operation'], var_name="dataset", value_name="value")
latex_df = latex_df.pivot_table('value', ['dataset', 'operation'], 'model')
print(latex_df)
"""