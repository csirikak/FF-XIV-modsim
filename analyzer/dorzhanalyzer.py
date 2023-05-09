import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
file_name='arrivalRates.txt'

def import_file_to_list(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    # remove newline characters from each line and return the list
    return [line.strip() for line in lines]

def write_list_to_file(output_file, output_list):
    with open(output_file, 'w') as file:
        for item in output_list:
            file.write(f"{item}\n")

def interarrival_time_data(file_name):
    data=import_file_to_list(file_name)
    data=data[1::]
    output=[]
    for i in range(len(data)):
        search_time=int(data[i].split(' ')[0]) 
        arrivals=int(data[i].split(' ')[1])       
        output.append(search_time/arrivals)
    return output

def plot_histogram(data, num_bins=10):
    plt.hist(data, bins=num_bins)
    plt.xlabel('Data')
    plt.ylabel('Frequency')
    plt.title('Histogram of Data')
    plt.show()

def qq_plot(data, quantile_func):


    data = np.sort(data)
    inverse = np.array([])
    for j in range(len(data)):
        inverse=np.append(inverse,quantile_func((j-1/2)/len(data)))

    
    # Plot the q-q plot
    plt.plot(data, inverse, '.')
    plt.plot(data, data, 'k--')
    plt.xlabel("Inverse((j-1/2)/n)")
    plt.ylabel("Y")
    plt.title("Q-Q Plot")
    plt.show()

def ks_test(data, cdf_func):
    # Generate a sample of points from the PDF
    data = np.sort(data)
    cdf = cdf_func(data)
    # Calculate the empirical CDF of the data
    ecdf = np.searchsorted(data, data, side='right') / len(data)
    # Perform the Kolmogorov-Smirnov test
    D, p = stats.ks_2samp(ecdf, cdf)
   
    plt.plot(data, ecdf, '.', c='m',label='data')
    plt.plot(data, cdf, '.',c='c', label='expected data')
    plt.title('Kolmogorov–Smirnov test')
    plt.xlabel('Inter-arrival time')
    plt.ylabel('cumulative Probability')
    plt.legend()
    plt.show()

    return D, p


def expected(data):
    n = len(data)
    mean = np.mean(data)
    stddev = np.std(data)
    def cdf_func(x):
        #return stats.fisk.cdf(x,c=14.537,loc=-0.77938,scale=2.5643)
        return stats.norm.cdf(x,loc=mean,scale=stddev)
    def quantile_func(x):
        #return stats.fisk.ppf(x,c=14.537,loc=-0.77938, scale=2.5643)
        return stats.norm.ppf(x,loc=mean,scale=stddev)
    plot_histogram(data,10)
    qq_plot(data,quantile_func)
    print(ks_test(data,cdf_func))


data=np.array(interarrival_time_data(file_name))
expected(data)