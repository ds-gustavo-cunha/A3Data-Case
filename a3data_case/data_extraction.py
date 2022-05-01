def downcast_dataframe(df, verbose=True):
    """Try to downcast numeric columns of the dataframe so as to use less memory.

    Args
        df: a pd.DataFrame object
        verbose: a boolean to check if user wants to see downcast report

    Return
        dataframe: a pd.DataFrame object with downcasted columns if it was possible; 
            otherwise, it will just return the original dataframe columns"""
    # import required libraries
    import pandas as pd

    # get total dataframe input size in bytes
    # the size will include the index size
    input_size = df.memory_usage(index=True, deep = True).sum()

    # iterate over numeric columns types
    for type in ["float", "integer"]:

        # get the column names whose type is the given type iteration
        list_cols = list( df.select_dtypes( include=type ) )

        # iterate over the columns with the selected types
        for col in list_cols:
            
            # downcast the given column to the smallest numerical dtype possible
            df[col] = pd.to_numeric( df[col], downcast=type )
            
            # check if column is float
            if type == "float":
                # try to convert float column to integer column and downcast
                df[col] = pd.to_numeric(df[col], downcast="integer")

    # check if user wants a quick report of the results
    if verbose:

        # get total dataframe output size in bytes
        # the size will include the index size
        output_size = df.memory_usage( index=True, deep = True ).sum()
        # get the percentage size that was reduced
        ratio = (1 - round(output_size / input_size, 2) ) * 100   

        # print report
        print(f"Dataframe size was reduced to {ratio:.2f}% of its original size.",
              f"\nInitial dataframe size: {input_size / 1000000:,.2f} MB",
              f"\nFinal dataframe size: {output_size / 1000000:,.2f} MB")

    return df