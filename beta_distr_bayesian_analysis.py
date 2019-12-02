  def beta_distr_bayesian_analysis(df, mianownik, licznik, channel, nazwa_kol_wariantow, wariant):
    """
    Funkcja analizuje statystyczną istotność różnic między wariantami (2-ma).
    
    Arfumenty:
        df - dataframe z danymi (musi zawierac kolumne 'channel'). 
            Gdy takiej kolumny nie ma, najlepiej sobie w pandasie ja dodac poprzez kopie kolumny z kanalem.
        mianownik - nazwa kolumny z mianownikiem do analizowanej statystyki
        licznik - nazwa kolumny z licznikiem do analizowanej statystyki
        channel - kanał jaki chcemy filtrować z kolumny 'channel'
        nazwa_kol_wariantow - podaj nazwę kolumny w której znajdują się warianty
    """
    # importy
    from scipy.stats import chisquare
    from scipy.stats import chi2_contingency
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.stats as scs
    import pandas as pd
    from scipy.stats import beta
    from numpy import random

    df['licznikRev'] = df[mianownik] - df[licznik]
    base_df = df[(df['device_class'] == channel) & (df[nazwa_kol_wariantow] == 'base')] \
        [[mianownik, licznik, 'licznikRev']] \
        .agg({mianownik : ['sum'], licznik : ['sum'], 'licznikRev' : ['sum']})
    exp_df = df[(df['device_class'] == channel) & (df[nazwa_kol_wariantow] == wariant)] \
        [[mianownik, licznik, 'licznikRev']] \
        .agg({mianownik : ['sum'], licznik : ['sum'], 'licznikRev' : ['sum']})

    fig, ax1 = plt.subplots(1, 1, figsize=(10, 6)) 

    # Base
    control_alpha_desktop = base_df[licznik].values[0]
    control_beta_desktop = base_df['licznikRev'].values[0]
    p_control_desktop = control_alpha_desktop / (control_alpha_desktop + control_beta_desktop)

    # Test_var
    experiment_alpha_desktop = exp_df[licznik].values[0]
    experiment_beta_desktop = exp_df['licznikRev'].values[0]
    p_experiment_desktop = experiment_alpha_desktop / (experiment_alpha_desktop + experiment_beta_desktop)

    # Generate beta distributions based on number of successes(alpha) and failures(beta)
    control_distribution_desktop = beta(control_alpha_desktop, control_beta_desktop)
    experiment_distribution_desktop = beta(experiment_alpha_desktop, experiment_beta_desktop)

    #plot distributions using 
    x = np.linspace(0, 1, 10000)
    ax1.plot(x, control_distribution_desktop.pdf(x), color = 'blue')
    ax1.plot(x, experiment_distribution_desktop.pdf(x), color = 'orange')
    ax1.set_xlim((p_experiment_desktop - p_experiment_desktop * 0.1, p_experiment_desktop + p_experiment_desktop * 0.1))
    ax1.set(xlabel='conversion rate', ylabel='density');
    ax1.set_title("'{wariant}' variant VS base beta distributions on '{channel}'".format(wariant = wariant, channel = channel), size = 12);

    plt.show();
    
    # test Bayesa
    
    s_size = 100000
    
    p_b = control_alpha_desktop / (control_alpha_desktop + control_beta_desktop)
    p_e = experiment_alpha_desktop / (experiment_alpha_desktop + experiment_beta_desktop)
    
    b_samples = random.beta(control_alpha_desktop, control_beta_desktop, size = s_size)
    e_samples = random.beta(experiment_alpha_desktop, experiment_beta_desktop, size = s_size)
    
#     print('percentage chance of test_variant beating base variant:')
#     print(str((np.sum(e_samples > b_samples) / s_size * 100)) + "%")
    
    for i in np.arange(0,0.11,0.01):
        print('percentage chance of test_variant beating base variant by %s:' %(str(int(i*100)) + "%"))
        print(str((np.sum(e_samples / b_samples > (1+i) ) / s_size * 100)) + "%")
    
    print('\n')
    print('--------------------------')
    print(channel)
#     print(f'control_successes (desktop): {control_alpha_desktop}')
#     print(f'control_failures (desktop): {control_beta_desktop}')
    print(f'control_ctr (desktop): {str(p_control_desktop * 100) + "%"}')
#     print('--------------------------')
#     print(f'experiment_successes (desktop): {experiment_alpha_desktop}')
#     print(f'experiment_failures (desktop): {experiment_beta_desktop}')
    print(f'experiment_ctr (desktop): {str(p_experiment_desktop * 100) + "%"}')