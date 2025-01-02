work in progress

# edition_comparision_Debther
# Text Comparison and Clustering

This project provides a Python-based pipeline for comparing two texts and identifying clusters of matching sequences. The comparison results are organized into two DataFrames: one for the clusters of matching text segments and another for the comparison of unique and clustered segments.

## Features

- **Text Cleaning**: Prepares and tokenizes texts by removing unwanted characters and splitting based on specified separators.
- **Cluster Detection**: Identifies contiguous sequences of matching text between two input texts, with customizable minimum cluster lengths.
- **Comparison Table**: Organizes unique and matching segments in a structured comparison table.
- **Output**: Generates two DataFrames:
  - A **cluster DataFrame** containing the details of the matching clusters.
  - A **comparison table** showing the positions and lengths of both unique and clustered segments in the two texts.

## Installation

### Prerequisites

To run this project, you'll need Python 3.x and the following libraries:

- pandas

You can install the required dependencies using `pip`:

```bash
pip install pandas
```
### Example Usage

```python
# Example of running the edition_comparison_debther comparison pipeline
from your_module import edition_comparison_debther

# Define two texts to compare
text_a = "This is the first sample text for comparison."
text_b = "This is the second sample text to compare."

# Define separators and character replacements
sep = [" ", ","]
replace_chars = [(",", ""), (";", "")]

# Run the edition_comparison_debther function
cluster_df, compare_table = edition_comparison_debther(text_a, text_b, sep=sep,
                            replace_chars=replace_chars, min_cluster_length=2)

# Display the results
print(cluster_df.head())  # Display the cluster details
print(compare_table.head())  # Display the comparison table
```
