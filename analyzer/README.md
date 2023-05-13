### This directory contains three Python scripts that can be used to analyze Final Fantasy XIV gameplay data.

## analyzer.py
This script reads data from a sessions.txt file, which is expected to contain two columns of space-separated values representing values and their frequencies. It then uses the Fitter package to fit various statistical distributions to the data and select the best-fit distribution. The script outputs the summary of fitting results and a PDF plot of each distribution. You can use the parameters of the best-fit distribution to generate random data or calculate probabilities.

## dorzhanalyzer.py
This script contains functions to read inter-arrival time data from a text file (arrivalRates.txt), plot a histogram, generate a Q-Q plot, and perform the Kolmogorov-Smirnov test to determine the goodness-of-fit of the data to a normal distribution. It outputs the plot of the empirical cumulative distribution function (ECDF) of the data and the expected cumulative distribution function (CDF) of the normal distribution, along with the test statistic and p-value.

## parser.py
This script reads data files in a directory (ffxivdata), sorts them by creation time, and extracts character names and play times. It then creates a sessions.txt file with the values and frequencies of play time and outputs the final list of names and play times.

## Usage
To use any of these scripts, simply run them with a Python interpreter. Make sure to modify any directory or file paths as necessary.
