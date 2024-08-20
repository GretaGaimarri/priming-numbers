import pandas as pd
import numpy as np
print(f"Versione di NumPy in uso: {np.__version__}")

data = pd.read_csv('data_dots.csv')

# filtering the data based on accuracy and limits
filtered_data = data[(data['accuracy'] == '1') & (data['reaction_time'] > 0.150) & (data['reaction_time'] < 3.000)] #to be defined

# log calculation
filtered_data['log_reaction_time'] = np.log(filtered_data['reaction_time'])

# saving 
filtered_data.to_csv('filtered_data_with_log.csv', index=False)

print("Filtrati i dati e calcolato il logaritmo dei tempi di reazione. Risultati salvati in 'filtered_data_with_log.csv'")
