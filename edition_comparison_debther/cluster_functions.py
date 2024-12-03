from cluster_class import Cluster
from itertools import chain
import pandas as pd

def clean(edition, sep=None, replace_chars=None):
    """
    Cleans and tokenizes a given text by applying character replacements and splitting based on specified separators.

    Args:
        edition (str): The input text to be processed.
        sep (list, optional): A list of separator characters used to split the text. Defaults to [' ', ',', '.'] if not provided.
        replace_chars (list, optional): A list of (old, new) tuples specifying character replacements to apply to the text.
            If not provided, no replacements are performed.

    Returns:
        list: A list of cleaned and tokenized strings derived from the input text, with empty strings removed.

    Example:
        clean("Hello, world!", sep=[',', ' '], replace_chars=[('!', '')])
        # Output: ['Hello', 'world']
    """

    # Standardwerte festlegen, falls Parameter nicht übergeben wurden
    if sep is None:
        sep = [' ', ',', '.']  # Beispiel-Trennzeichen
        print(f'no seperator given. Standard values used {sep}')

    if replace_chars is None:
        replace_chars = []
        print(f'no characters to replace given.')  # Beispiel-Ersetzungen
    else:
        # ersetze Zeichen in der edition 
        translation_table = str.maketrans(dict(replace_chars))
        edition = edition.translate(translation_table)
    print(sep)
    # Zerlegen nach Trennzeichen
    result = [edition]
    for separator in sep:
        try:
        # Zerlege alle bisherigen Einträge anhand des aktuellen Trennzeichens
            result = list(chain.from_iterable(part.split(separator) for part in result))
        except:
            pass
    # Entferne leere Strings und trimme Leerzeichen
    result = [item.strip() for item in result if item.strip()]

    return result




def cluster_length(a, b, i, j):
    """
    Determines the length of a cluster from position i in a and j in b.
    Is called in find_clusters.
    """
    length = 1  # Ein Treffer wird zu Beginn gezählt
    while i + 1 < len(a) and j + 1 < len(b) and a[i + 1] == b[j + 1]:
        i += 1
        j += 1
        length += 1
    return i, j, length


def find_cluster(a, b, min_clus_length,text_a_name='text_a',text_b_name='text_b'):
    """
    Finds clusters of matching elements between two sequences based on a minimum cluster length.

    The function compares two sequences (`a` and `b`) and identifies clusters of matching elements. A cluster is defined as a 
    contiguous sequence of matching elements in both `a` and `b` with a length greater than or equal to `min_clus_length`.
    The results are organized into a DataFrame for further analysis.

    Args:
        a (list): The first sequence to compare.
        b (list): The second sequence to compare.
        min_clus_length (int): The minimum length required for a cluster to be recorded.
        text_a_name (str, optional): The name of the first text for labeling purposes. Defaults to 'text_a'.
        text_b_name (str, optional): The name of the second text for labeling purposes. Defaults to 'text_b'.

    Returns:
        pandas.DataFrame: A DataFrame containing details of the identified clusters, including their positions in both texts 
        and the difference between start indices.

        Columns:
            - Named according to `clus_tupel_naming` attributes of `Cluster` objects.
            - A "differenz" column indicating the difference between the cluster start indices in `a` and `b`.

    Example:
        find_cluster(['a', 'b', 'c', 'd'], ['x', 'b', 'c', 'y'], 2)
        # Returns a DataFrame with clusters where elements match for at least 2 consecutive positions.

    Notes:
        - The function tracks progress during execution and prints updates to the console.
        - Uses a `Cluster` object to manage and finalize clusters.
    """

    cluster_lst = []  # Ergebnisliste
    skips = 0  # Überspringe Indizes nach Clustertreffern
    len_a = len(a)
    for i in range(len(a)):
        print(f'{i} of {len_a}', end='\r')  # Fortschrittsanzeige
        if skips > 0:  # Überspringe Indizes basierend auf vorherigen Clustern
            skips -= 1
            continue

        cluster_object = Cluster(i,text_a_name,text_b_name)

        for j in range(len(b)):
            if a[i] == b[j]:  # Potenzieller Start eines Clusters
                # Bestimme die Länge des Clusters
                _, _, length = cluster_length(a, b, i, j)
                
                # Füge das Cluster hinzu, wenn es die Mindestlänge erfüllt
                if length >= min_clus_length:
                    cluster_object.append_cluster(j, length)
                    
                    # Setze die maximale Länge für die überspringbaren Indizes
                    skips = max(skips, length)

        # Füge das Cluster-Objekt zur Liste hinzu, falls Cluster gefunden wurden
        if cluster_object.clusters:
            cluster_object.pick_finalcluster()  # Bestimme das finale Cluster
            cluster_lst.append(cluster_object)

    cluster_dict ={}

    for j in range(5):
        cluster_dict[cluster_lst[0].clus_tupel_naming[j]] = []

    for i in cluster_lst:
        for j in range(5):
            cluster_dict[i.clus_tupel_naming[j]].append(i.final_cluster[j])

    data_df = pd.DataFrame(cluster_dict)
    data_df['differenz'] = data_df[i.clus_tupel_naming[2]] - data_df[i.clus_tupel_naming[0]]    
    
    print(f'100% -- finished', end='\r')
    return data_df


def compare_defter(a, b, cluster_df=pd.DataFrame(), text_a_name='text_a',text_b_name='text_b'):
    """
    Compares two sequences and organizes their similarities and unique elements into a structured DataFrame.

    This function takes two sequences (`a` and `b`), a DataFrame of clusters, and optional text names, 
    then generates a DataFrame detailing both unique elements and clustered matches between the sequences.

    Args:
        a (list): The first sequence to compare.
        b (list): The second sequence to compare.
        cluster_df (pandas.DataFrame, optional): A DataFrame containing cluster information. Defaults to an empty DataFrame.
            Expected columns: 
            - f'start_{text_a_name}', f'end_{text_a_name}', f'start_{text_b_name}', f'end_{text_b_name}', 'length'.
        text_a_name (str, optional): The name of the first sequence for labeling. Defaults to 'text_a'.
        text_b_name (str, optional): The name of the second sequence for labeling. Defaults to 'text_b'.

    Returns:
        pandas.DataFrame: A DataFrame with the following columns:
            - 'tag': Indicates whether the entry is 'unique' or part of a 'cluster'.
            - f'Pos_{text_a_name}': Start position in `a`.
            - f'Length_{text_a_name}': Length of the segment in `a`.
            - f'{text_a_name}': Content of the segment in `a`.
            - f'Pos_{text_b_name}': Start position in `b`.
            - f'Length_{text_b_name}': Length of the segment in `b`.
            - f'{text_b_name}': Content of the segment in `b`.
            - 'Length_Cluster': Length of the cluster (0 for unique segments).
            - 'Cluster': Content of the matching cluster (empty for unique segments).

    Raises:
        ValueError: If the `cluster_df` does not contain the required keys 
                    (e.g., f'start_{text_a_name}', f'end_{text_a_name}', etc.).

    Example:
        a = ["word1", "word2", "word3", "word4"]
        b = ["wordA", "wordB", "word3", "word4"]
        cluster_df = pd.DataFrame({
            "start_text_a": [2],
            "end_text_a": [4],
            "start_text_b": [2],
            "end_text_b": [4],
            "length": [2],
        })
        result = compare_defter(a, b, cluster_df, text_a_name="text_a", text_b_name="text_b")
        print(result)
        # Output: A DataFrame with rows for unique and cluster segments.
    """

    
    # Wandle Dataframe in Dictionary um
    dict = cluster_df.to_dict(orient='tight',index=False)
    cluster_dict={}
    for i in range(6):
        cluster_dict[dict['columns'][i]]=[]
        for j in range(len(dict['data'])):
            cluster_dict[dict['columns'][i]].append(dict['data'][j][i])     
    # Bereite Dictionary für Ausgabe vor
    clustered_text = {'tag':[],f'Pos_{text_a_name}':[],f'Length_{text_a_name}':[],f'{text_a_name}':[],
                      f'Pos_{text_b_name}':[],f'Length_{text_b_name}':[],f'{text_b_name}':[],
                      'Length_Cluster':[],'Cluster':[]}
    
    # Validierung der Eingaben
    required_keys = [f'start_{text_a_name}', f'end_{text_a_name}', f'start_{text_b_name}', f'end_{text_b_name}', 'length']
    if not all(key in cluster_dict for key in required_keys):
        raise ValueError(f"cluster_dict muss die Keys {required_keys} enthalten. Es enthält {[key for key in cluster_dict]}")
 


    a_start = 0
    b_start = 0

    # Iteriere über alle Cluster
    for cluster_nr in range(len(cluster_dict[f'start_{text_a_name}'])):
        # Cluster-Start- und Endpositionen auslesen
        start_a, end_a = cluster_dict[f'start_{text_a_name}'][cluster_nr], cluster_dict[f'end_{text_a_name}'][cluster_nr]
        start_b, end_b = cluster_dict[f'start_{text_b_name}'][cluster_nr], cluster_dict[f'end_{text_b_name}'][cluster_nr]
        length = cluster_dict['length'][cluster_nr]

        # Uniques hinzufügen
        clustered_text['tag'].append('unique')
        clustered_text[f'Pos_{text_a_name}'].append(a_start)
        clustered_text[f'Pos_{text_b_name}'].append(b_start)
        clustered_text[f'Length_{text_a_name}'].append(start_a - a_start)
        clustered_text[f'Length_{text_b_name}'].append(start_b - b_start)
        clustered_text[f'{text_a_name}'].append('་'.join(a[a_start:start_a]))
        clustered_text[f'{text_b_name}'].append('་'.join(b[b_start:start_b]))
        clustered_text['Length_Cluster'].append(0)
        clustered_text['Cluster'].append('')

        # Cluster hinzufügen
        clustered_text['tag'].append('cluster') 
        clustered_text[f'Pos_{text_a_name}'].append(start_a)
        clustered_text[f'Pos_{text_b_name}'].append(start_b)
        clustered_text[f'Length_{text_a_name}'].append(0)
        clustered_text[f'Length_{text_b_name}'].append(0)
        clustered_text[f'{text_a_name}'].append('')
        clustered_text[f'{text_b_name}'].append('')
        clustered_text['Length_Cluster'].append(length)
        clustered_text['Cluster'].append('་'.join(a[start_a:end_a]))

        # Aktualisiere Startpositionen
        a_start = end_a
        b_start = end_b


    #wandle Dictionary in DataFrame um
    return pd.DataFrame(clustered_text)
