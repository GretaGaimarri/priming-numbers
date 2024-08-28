
# Scalar Adjective Priming Task

This project involves a priming task where the primes are scalar adjectives and the targets are symbolic or non-symbolic quantities. The objective is to investigate the potential relationship between these words and the generalized quantity mechanism.

## Description

The Scalar Adjective Priming Task is designed to explore how scalar adjectives (e.g., good, bad, tall, short) can influence the perception and processing of quanitity targets. The idea is to reproduce a similar subliminal priming task with scalar adjectives, to test the possible involvement of the Generalized Magnitude System (Walsh, 2003; Kochari et al., 2022).
The experiment is composed of a prime (adjective) followed by a target. Adjectives are divided into “less quantity-related” (0) and “more quantity-related” (1). Two versions of the experiment: numerical priming and dots. In the numerical priming task, targets are numbers from 1 to 9 (except 5). Participants are asked to say whether the target number is smaller or bigger than 5. Two conditions: Congruent and Incongruent. In the congruent condition: low-magnitude adjectives are followed by a number smaller than 5 and high-magnitude by a number bigger than 5. Vice versa in the incongruent condition. 
The second version of this task is similar to Lourenco et al. (2016): the experiment involves presenting participants with pairs of adjectives (a low- and a high-magnitude adjective, these are displayed in different colors: one in black, one in white) followed by a display of two groups of dots (black and white). Participants are asked to estimate which group of dots is more numerous.The purpose of these adjectives is to serve as primes, which may influence participants' perceptions or responses in the subsequent dot estimation task. The congruence or incongruence between the prime's color and the dominant dot color might reveal how alignment between expectation (set by the prime) and reality (dot counts) affects response accuracy and reaction times.

## Dependencies:

| Language/Package | Version tested on |
|------------------|-------------------|
| Python           | 3.8.19            |
| Pandas           | 2.0.3             |
| PsychoPy         | 2024.2.0          |
| Pillow           | 10.4.0            |
| Numpy            | 1.24.4            |
| Statsmodels      | 0.14.1            |

## Scripts ##

- **numerical_priming.py**: A Python script focused on running the numerical priming tasks. This script sets up a classification experiment, presents stimuli, records participant responses, and saves the data for further analysis.

- **priming_dots.py**: The main Python script to run the dot priming experiment. It includes the logic for presenting the dots in different conditions (e.g., congruent, incongruent), handling participant responses, and recording data like reaction times and accuracy.

- **data_analysis.py**: A Python script that analyzes the experimental data collected from participants. It performs statistical tests, such as linear mixed models and t-tests, to evaluate the effects of different conditions (congruent/incongruent) on reaction times and accuracy.

- **creating_stimuli.py**: This script leads to generate and visualize stimuli for the experiment in 'priming_dots.py'. In this case it is not used, and the groups of dots are randomly created. However, controlling for the number of dots and having specific defined stimuli/images could be useful in some circumstances.


## Utility Module

The `utility.py` file is a module that provides helper functions for various tasks needed during the experiment, such as creating the PsychoPy window, generating instruction text, and determining participant IDs.


## Data Files

### `adjectives.xlsx`

The `adjectives.xlsx` file provides a list of scalar adjectives used in the experiment to create stimuli, along with metadata used for categorization and trial balancing.

#### Columns

- `word`: The prime adjective.
- `dimension`: The category or dimension of the adjective.
- `bigsmall`: Indicator for grouping based on concept size.

This file is crucial for generating the randomized trials and displaying the appropriate stimuli to participants.


