from cluster_functions import *
from debther_texts import *

def edition_comparison_debther(text_a=None, text_b=None,*, sep=None, replace_chars=None, min_cluster_length=10,text_a_name='text_a',text_b_name='text_b'):
    """
    Processes and compares two texts to identify and analyze clusters of matching sequences.

    This function combines the cleaning, clustering, and comparison steps to produce:
    1. A DataFrame of clusters matching between the two texts.
    2. A comparison table showing unique and clustered segments for both texts.

    Args:
        text_a (str): The first text to process and compare.
        text_b (str): The second text to process and compare.
        sep (list, optional): A list of characters used to split the text into tokens. Defaults to None, using standard separators.
        replace_chars (list, optional): A list of (old, new) tuples specifying character replacements in the text. Defaults to None.
        min_cluster_length (int, optional): The minimum length of a cluster to be considered valid. Defaults to 10.
        text_a_name (str, optional): The name of the first text for labeling in the results. Defaults to 'text_a'.
        text_b_name (str, optional): The name of the second text for labeling in the results. Defaults to 'text_b'.

    Returns:
        tuple: A tuple containing:
            - cluster_df (pandas.DataFrame): A DataFrame with cluster details, including start and end positions in both texts 
            and cluster lengths.
            - compare_table (pandas.DataFrame): A DataFrame with both unique and cluster segments, detailing their positions, 
            lengths, and content for both texts.

    Workflow:
        1. Cleans both texts using `clean()`.
        2. Identifies clusters using `find_cluster()`.
        3. Creates a comparison table with `compare_defter()`.

    Example:
        text_a = "This is a sample text for comparison."
        text_b = "Here is another sample text to compare."
        cluster_df, compare_table = main(text_a, text_b, sep=[" ", "."], replace_chars=[(",", "")], min_cluster_length=2)
        
        print(cluster_df)  # Displays the clusters.
        print(compare_table)  # Displays the comparison of unique and cluster segments.
    """
    # Clean the input texts
    text_a_cleaned = clean(text_a,sep,replace_chars)
    text_b_cleaned = clean(text_b,sep,replace_chars)

    # Find clusters in both texts
    cluster_df = find_cluster(text_a_cleaned,text_b_cleaned,min_cluster_length,text_a_name,text_b_name)
    
    # Compare the clusters and create a comparison table

    compare_table = compare_defter(text_a_cleaned,text_b_cleaned,cluster_df,text_a_name,text_b_name)
    # Return the cluster DataFrame and the comparison table
    return cluster_df,compare_table

if __name__ == "__main__":
    """
Entry point for running the text comparison pipeline with predefined test data.

This script initializes text data, parameters, and runs the `main()` function to compare 
two texts, identifying clusters of similarities and organizing unique and clustered segments.

Workflow:
    1. Retrieves test texts and parameters using helper functions:
       - `debther_gangtok()`: Provides the first text.
       - `debther_peking()`: Provides the second text.
       - `debther_parameters()`: Supplies tokenization separators, replacement characters, and text names.
    2. Runs the `main()` function with the provided inputs.
    3. Prints the first few rows of the cluster DataFrame and comparison table.

Example:
    Run the script to see the output of the text comparison pipeline:
    
    ```
    python script.py
    ```

Outputs:
    - A preview of the clusters identified between the texts.
    - A preview of the comparison table containing unique and clustered segments.

Dependencies:
    Ensure the functions `debther_gangtok`, `debther_peking`, and `debther_parameters` are implemented 
    and return appropriate data.
"""

    # Get text and parameters to test the function
    gangtok = debther_gangtok()
    peking = debther_peking()
    sep, replace_chars,text_a_name, text_b_name = debther_parameters()

    # Call the main function with the test data
    cluster, table = edition_comparison_debther(gangtok,
                        peking,
                        sep=sep,
                        replace_chars=replace_chars,
                        text_a_name=text_a_name,
                        text_b_name=text_b_name
                        )
    
    # Print the results
    print(cluster.head())
    print(table.head())