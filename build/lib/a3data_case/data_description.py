def check_dataframe( dataframe, head = True, head_size = 5, sample_size = 5 ):
    '''
    It prints the number of NAs, the percentage of NA, the number of unique values and the data type for each column.
    It prints dataframe shape and also displays statistics for numerical variables.
    Finally, it displays the dataframe head or a random sample of dataframe according to user choice
    
    Args
        dataframe: the pandas dataframe that the user wants to check
        head: boolean that indicate if user wants to see 
            the head of the dataframe (True) or 
            a sample of the dataframe (False)
        head_size: size of the dataframe.head() function 
        sample_size: size of the dataframe.sample() function 

    Return
        None: a none type object
    '''

    # import required libraris
    import pandas as pd
    import numpy  as np

    #########################################################
    # This function requires that Jinja2 library is installed,
    # but it doesn't need to be imported 
    # -> pip install Jinja2
    #########################################################

    # ======= MEMORY USAGE INFORMATION =======

    df_size_in_memory = dataframe.memory_usage(index = True, deep = True).sum() / (10**6)
    print(f"Dataframe size in memory: {df_size_in_memory:,.3f} MB", "\n")

    # ======= DESCRIPTIVE INFORMATION =======
        
    # create dictionary with descriptive information
    dict_data = {'Num NAs': dataframe.isna().sum(),
                 'Percent NAs': (dataframe.isna().mean() * 100).round(decimals = 2),
                 'Num unique': dataframe.nunique(),
                 'Data Type': dataframe.dtypes }    

    
    # ======= SHAPE INFORMATION =======
    
    # print descriptive data
    print( pd.DataFrame( dict_data ), '\n' )
    # print dataframe shape
    print( f'Dataframe shape is {dataframe.shape}', '\n' )  

    # ======= STATISTICS =======
    
    # get numeric variables
    df_numeric = dataframe.select_dtypes( include = 'number' )
    
    # central tendency statistics   
    mean_stats = pd.DataFrame( df_numeric.apply( np.mean ) ).T
    median_stats  = pd.DataFrame( df_numeric.apply( np.median ) ).T
    
    # deviation statistics
    std_stats = pd.DataFrame( df_numeric.apply( np.std ) ).T
    min_stats = pd.DataFrame( df_numeric.apply( np.nanmin ) ).T
    max_stats = pd.DataFrame( df_numeric.apply( np.nanmax ) ).T
    range_stats = pd.DataFrame( df_numeric.apply( lambda x: x.max() - x.min() ) ).T
    skew_stats = pd.DataFrame( df_numeric.apply( lambda x: x.skew() ) ).T
    kurtosis_stats = pd.DataFrame( df_numeric.apply( lambda x: x.kurtosis() ) ).T
    iqr_stats = pd.DataFrame( df_numeric.apply( lambda x: np.percentile(x, 75, axis = 0) - \
                                                          np.percentile(x, 25, axis = 0)
                                              ) ).T
    
    # concatenate statistics    
    df_stats = pd.concat( [  mean_stats,
                             median_stats,
                             std_stats,
                             min_stats,
                             max_stats,
                             range_stats,
                             skew_stats,
                             kurtosis_stats,
                             iqr_stats
                          ] ).T.reset_index()
    
    # rename columns
    df_stats.columns = ['attribute', 
                       'mean',
                       'median',
                       'std',
                       'min',
                       'max',
                       'range',
                       'skew',
                       'kurtosis',
                       'iqr']

    # reorder columns
    df_stats = df_stats[['attribute', 
                         'mean',
                         'median',
                         'std',
                         'iqr',
                         'min',
                         'max',
                         'range',
                         'skew',
                         'kurtosis'
                        ]]    
        
    # print statistics for numerical data
    print( '\n\nStatistics for Numerical Variables')
       
    # highlight min and max statistics -> help identify 'non-sense' data
    df_stats = df_stats.style.applymap(lambda x: 'background-color: Navy; color: White', subset = ['min', 'max'])
    # display statatistics
    display( df_stats )

    # ======= DATAFRAME INSTANCES =======
    # check if user wants df.head()
    if head:
        print( '\n\nDataframe head:' )
        display( dataframe.head( head_size ) )

    # user wants df.sample()
    else:
        print( '\n\nDataframe sample:' )
        display( dataframe.sample( sample_size ) )

    return None