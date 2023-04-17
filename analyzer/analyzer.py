import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fitter import Fitter

# Load data from txt file
data = np.loadtxt('sessions.txt')

# Convert data to a Pandas DataFrame
df = pd.DataFrame({'x': data[:,0], 'count': data[:,1]})

# Generate random data using the frequency of each value
data = []
for i in range(len(df)):
    data += [df['x'][i]] * int(df['count'][i])

# Fit various distributions to the data using the Fitter package
f = Fitter(data)
f.fit()

# View the summary of the fitting results
print(f.summary())

# Visualize the fitting results by plotting the PDF of each distribution
f.plot_pdf()
plt.show()

# Choose the best distribution for the data based on the goodness-of-fit statistics and PDF plots
best_dist = f.get_best()
print("Best distribution: ", best_dist)

# You can now use the parameters of the best distribution to generate random data or calculate probabilities.