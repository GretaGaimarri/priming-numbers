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
=======
import statsmodels.formula.api as smf

print(f"Versione di NumPy in uso: {np.__version__}")


data = pd.read_csv('data_dots.csv')

# filtering reaction times
filtered_data = data[(data['accuracy'] == '1') & (data['reaction_time'] > 0.150) & (data['reaction_time'] < 3.000)]

# log-trasformed reaction times
filtered_data['log_reaction_time'] = np.log(filtered_data['reaction_time'])

# calculate mean accuracy for each participant
mean_accuracy_per_participant = filtered_data.groupby('participant_id')['accuracy'].mean()

# adding mean accuracy for each participant
filtered_data = filtered_data.merge(mean_accuracy_per_participant.rename('mean_accuracy_participant'), on='participant_id')

# Mean accuracy for the total sample
mean_accuracy_total_sample = filtered_data['accuracy'].mean()

print(f"Media dell'accuratezza per ciascun partecipante:\n{mean_accuracy_per_participant}")
print(f"Media dell'accuratezza per il campione totale: {mean_accuracy_total_sample}")

# Saving data
filtered_data.to_csv('filtered_data_with_log.csv', index=False)

# Linear Mixed Model

# Define the mixed effects model
model = smf.mixedlm("log_reaction_time ~ congruent", 
                    data=filtered_data, 
                    groups=filtered_data["participant_id"], 
                    re_formula="~dimension")

# Fit the model
result = model.fit()

# Print the summary of the model
print(result.summary())
