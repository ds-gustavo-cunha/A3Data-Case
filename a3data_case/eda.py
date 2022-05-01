def numerical_plot( dataframe, column, figsize = (8, 7), hist = True ):
    '''
    Plot histogram (or kde) on the hist_axs and boxplot on the box_axs
    
    Args
        dataframe: datataframe with numerical features
        column: numerical feature to be plotted
        figsize: tuple with figsize (width, height) in inches
        hist: boolean to indicate if user wants a histplot or a kdeplot.
            This may be useful when histplot is too slow.
    
    Return
        None: a None Type object
    '''

    # import required libraries
    import matplotlib.pyplot as     plt
    from   matplotlib        import gridspec 
    import seaborn           as     sns
       
    # create a figure object
    fig = plt.figure( figsize = (8, 7), constrained_layout = True );

    # create a grid for plotting
    specs = gridspec.GridSpec( ncols = 1, nrows = 2, figure = fig);

    # check sales distribution
    hist_axs = fig.add_subplot( specs[ 0, 0 ] )
    box_axs = fig.add_subplot( specs[ 1, 0 ] )

    # check if user wants histplot
    if hist:
        # set title
        hist_axs.set_title( column.upper() )
        # plot histogram
        sns.histplot( x = column, data = dataframe, ax = hist_axs, kde = True )

    # in case user want kdeplot instead of histplot
    else:
        # set title
        hist_axs.set_title( column.upper() )
        # plot kdeplot
        sns.kdeplot( x = column, data = dataframe, ax = hist_axs, fill = True )

    # set title
    box_axs.set_title( column.upper() )

    # plot boxplot
    sns.boxplot(  x = column, data = dataframe, ax = box_axs )

    
    return None


def categorical_plot( df_cat, n_cols = 3, countplot = True, figsize = None ):
    '''
    Plot histogram for all features in the dataframe. 
    Dataframe is supposed to have only categorical features.
    
    Args
        df_cat: datataframe with categorical features
        n_cols: is a integer with the number of columns on the final chart
        countplot: a boolean to indicate if user wants to plot a countplot (count = True)
            or a histplot (countplot = False)
        figsize: tuple with figsize (width, height) in inches       
    
    Return
        None
    '''

    # import required libraries
    import matplotlib.pyplot as plt
    from matplotlib import gridspec
    import seaborn as sns

    # define number of rows
    n_rows = df_cat.shape[1] // n_cols + 1
    
    # check if user input figsize
    if figsize is None:
        # assign th default figsize
        figsize = (n_cols*4.5, n_rows*4.5)
    
    # create a figure object
    fig = plt.figure( figsize = figsize, constrained_layout = True )

    # create grid for plotting
    specs = gridspec.GridSpec( ncols = n_cols, nrows = n_rows, figure = fig)

    # iterate over column to plot countplot figure
    for index, column in enumerate( df_cat.columns ):
        # create a subplot to plot the given feature
        ax1 = fig.add_subplot( specs[index // n_cols, index % n_cols] )
        # set the title for the subplot
        ax1.set_title( column.upper() )
        # check if user wants a countplot
        if countplot:
            # plot countplot
            sns.countplot( x = column, data = df_cat, ax = ax1 )
        # user wants a histplot
        else:
            # plot histplot
            sns.histplot( x = column, data = df_cat, ax = ax1 )
        # rotate x ticks
        plt.xticks( rotation = 90 );
        
    
    return None


def cramer_v_corrected_stat( series_one, series_two ):
    '''
    Calculate crame v statistics for two categorical series 
    
    Args:
        series_one: first categorical dataframe column
        series_two: second categorical dataframe column
    
    Return:
        corr_cramer_v: corrected Cramer-V statistic

    NOTE: This implementation doesn't handle missing value (e.g. np.nan). It will raise warnings in this case.
    '''
    # import required libraries
    import numpy as np
    import pandas as pd
    from scipy.stats import chi2_contingency

    # create confusion matrix
    cm = pd.crosstab( series_one, series_two )
    # calculate the sum along all dimensions
    n = cm.sum().sum()
    # calculate number of row and columns of confusion matrix
    r, k = cm.shape

    # calculate chi_squared statistics
    chi2 = chi2_contingency( cm )[0]
    
    # calculate chi_squared correction
    chi2corr = max( 0, chi2 - (k-1)*(r-1)/(n-1) )
    # calculate k correction
    kcorr = k - (k-1)**2/(n-1)
    # calculate r correction
    rcorr = r - (r-1)**2/(n-1)

    # calculate corrected cramer-v
    corr_cramer_v = np.sqrt( (chi2corr/n) / ( min( kcorr-1, rcorr-1 ) ) )
   
    
    return corr_cramer_v


def create_cramer_v_dataframe( categ_features_analysis_dataframe ):
    '''
    Create a correlation matrix for features on categorical dataframe
    
    Args:
        categ_features_analysis_dataframe: dataframe with only categorical features
    
    Return:
        categ_corr_matrix: dataframe with cramer-v for every row-column pair 
                           in the input dataframe'''
    # import required libraries
    import numpy as np
    import pandas as pd
    
    # create final dataframe skeleton
    df_cramer_v = pd.DataFrame( columns = categ_features_analysis_dataframe.columns, 
                                index = categ_features_analysis_dataframe.columns )

    # fill final dataframe with cramer-v statistics for every row-column pair
    for row in df_cramer_v:
        for column in df_cramer_v:   
            df_cramer_v.loc[row, column] = float( cramer_v_corrected_stat( categ_features_analysis_dataframe[ row ],
                                                                           categ_features_analysis_dataframe[ column] ) )

    # ensure cramer-v is float
    categ_corr_matrix = df_cramer_v.astype( 'float' )
        
        
    return categ_corr_matrix