def beta_distr_bayesian_hist(df, mianownik, licznik, channel, nazwa_kol_wariantow, wariant):
    """
    Funkcja analizuje statystyczną istotność różnic między wariantami (2-ma).
    
    Arfumenty:
        df - dataframe z danymi (musi zawierac kolumne 'channel'). 
            Gdy takiej kolumny nie ma, najlepiej sobie w pandasie ja dodac poprzez kopie kolumny z kanalem.
        mianownik - nazwa kolumny z mianownikiem do analizowanej statystyki
        licznik - nazwa kolumny z licznikiem do analizowanej statystyki
        channel - kanał jaki chcemy filtrować z kolumny 'channel'
        nazwa_kol_wariantow - podaj nazwę kolumny w której znajdują się warianty
        wariant - jaki wariant badasz
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

    # Base
    control_alpha_desktop = base_df[licznik].values[0]
    control_beta_desktop = base_df['licznikRev'].values[0]
    p_control_desktop = control_alpha_desktop / (control_alpha_desktop + control_beta_desktop)

    # Test_var
    experiment_alpha_desktop = exp_df[licznik].values[0]
    experiment_beta_desktop = exp_df['licznikRev'].values[0]
    p_experiment_desktop = control_alpha_desktop / (control_alpha_desktop + control_beta_desktop)

    # Generate beta distributions based on number of successes(alpha) and failures(beta)
    control_distribution_desktop = beta(control_alpha_desktop, control_beta_desktop)
    experiment_distribution_desktop = beta(experiment_alpha_desktop, experiment_beta_desktop)
    
    # test Bayesa
    
    s_size = 100000
    
    p_b = control_alpha_desktop / (control_alpha_desktop + control_beta_desktop)
    p_e = experiment_alpha_desktop / (experiment_alpha_desktop + experiment_beta_desktop)
    
    b_samples = random.beta(control_alpha_desktop, control_beta_desktop, size = s_size)
    e_samples = random.beta(experiment_alpha_desktop, experiment_beta_desktop, size = s_size)

    data =  e_samples / b_samples - 1
    
    fig = plt.figure(figsize = (10,6)) 
    results, edges = np.histogram(data, 
                                  bins = 100, 
                                  normed=True)
    binWidth = edges[1] - edges[0]
    plt.bar(edges[:-1], 
            results*binWidth, 
            binWidth,
            alpha = 0.5)
    plt.axvline(x=0, 
                c='red', 
                alpha=0.75, 
                linestyle='--')
    #     plt.hist(data, 
    #              bins = 100, 
    #              alpha = 0.5, 
    #              density = True)
    #     plt.xlim(-0.1, 0.1)
    plt.title("Histogram of '{wariant}' variant / base variant scenarios on '{channel}'".format(wariant = wariant, channel = channel))
    plt.ylabel('probability')
    plt.xlabel('test variant / base variant')
    plt.show();