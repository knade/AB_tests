from scipy.stats import chisquare
from scipy.stats import chi2_contingency
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs
import pandas as pd
from scipy.stats import beta

def chi_test(df, channel, mianownik, licznik, alpha = 0.05):
  df['licznikRev'] = df[mianownik] - df[licznik]
  data = df[df['device_class'] == channel].groupby('experiment_variant') \
    .agg({mianownik : 'sum', licznik : 'sum', 'licznikRev' : 'sum'})
  
  data['conv'] = data[licznik] / data[mianownik]
  # data = data.reset_index()
  # data_a = data[(data['experiment_variant'] == 'base') | (data['experiment_variant'] == 'bestseller_carousel_top')]
  
  A = np.array([data[licznik], data['licznikRev']]).T
  
  print(data)
  if chi2_contingency(A, lambda_="log-likelihood", correction = False)[1] <= alpha:
    print('p_value = {0};\ndifference in {1} between variants is statistically significant with {2} level of confidence' \
          .format(chi2_contingency(A, lambda_="log-likelihood", correction = False)[1],
                  licznik,
                  str(1 - alpha)))
  else:
    print('p_value = {0};\ndifference in {1} between variants is NOT statistically significant with {2} level of confidence' \
          .format(chi2_contingency(A, lambda_="log-likelihood", correction = False)[1],
                  licznik,
                  str(1 - alpha)))