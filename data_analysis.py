import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.regressionplots import plot_partregress_grid


df = pd.read_csv('data_dots.csv')

# Convert reaction times to milliseconds
df['reaction_time'] = df['reaction_time'] * 1000


# Filter RTs between 100 and 3000 milliseconds
df = df[(df['reaction_time'] > 100) & (df['reaction_time'] < 3000)]

# How many trials were excluded?
trials_excluded = len(df[(df['reaction_time'] <= 100) | (df['reaction_time'] >= 3000)])
print(f"Number of trials excluded: {trials_excluded}")

data_db = df.groupby(['ID', 'congruent']).agg(
    accuracy=('accuracy', 'mean'),
    sum_resp=('resp', 'sum')
).reset_index()

# Calculate the mean accuracy
mean_accuracy = data_db['accuracy'].mean()
print(f"Mean accuracy: {mean_accuracy}")

# Subset data where accuracy is 1
df = df[df['accuracy'] == 1]

# How many trials excluded now?
trials_excluded_now = len(df[df['accuracy'] != 1])
print(f"Number of trials excluded after filtering for accuracy: {trials_excluded_now}")

# log calculation
df['logRTs'] = np.log(df['reaction_time'])

# Fit the linear mixed model
m0 = smf.mixedlm("logRTs ~ congruent", data=df, groups=df["ID"], re_formula="~dimension")
fit_m0 = m0.fit()

# Summary of the model
print(fit_m0.summary())

# Add fitted values and residuals to the dataframe
df['fitted'] = fit_m0.fittedvalues
df['residuals'] = df['reaction_time'] - np.exp(df['fitted'])

# Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='congruent', y='residuals', data=df, color='black', s=15, label='Partial Residuals')
sns.lineplot(x='congruent', y='fitted', data=df, color='red', label='Fitted Line')

# Customize plot
plt.title('Predictor Effects with Partial Residuals')
plt.xlabel('Congruence')
plt.ylabel('Log(RTs)')
plt.grid(True)
plt.legend()
plt.show()


