from cluster_class import Cluster
from itertools import chain
import pandas as pd

def clean(edition, sep=[], replace_chars=[]):
    """
    Bereinigt einen Text, ersetzt Zeichen und zerlegt ihn nach gegebenen Trennzeichen.

    Args:
        edition (str): Der zu bereinigende Text.
        sep (List[str]): Eine Liste von Trennzeichen, nach denen der Text aufgeteilt werden soll.
        replace_chars (List[tuple]): Eine Liste von Tupeln (alt, neu) zur Zeichenersetzung.

    Returns:
        pd.DataFrame: Positionen und Längen von Clustern in beiden Texten.
    """
    # Standardwerte festlegen, falls Parameter nicht übergeben wurden
    if sep is None:
        sep = [' ', ',', '.']  # Beispiel-Trennzeichen
        print(f'no seperator given. Standard values used {sep}')

    if replace_chars is None:
        print(f'no characters to replace given.')  # Beispiel-Ersetzungen
    else:
        # ersetze Zeichen in der edition 
        translation_table = str.maketrans(dict(replace_chars))
        edition = edition.translate(translation_table)

    # Zerlegen nach Trennzeichen
    result = [edition]
    for separator in sep:
        # Zerlege alle bisherigen Einträge anhand des aktuellen Trennzeichens
        result = list(chain.from_iterable(part.split(separator) for part in result))

    # Entferne leere Strings und trimme Leerzeichen
    result = [item.strip() for item in result if item.strip()]

    return result




def cluster_length(a, b, i, j):
    """
    Bestimmt die Länge eines Clusters ab Position i in a und j in b.
    Wird in find_clusters aufgerufen.
    """
    length = 1  # Ein Treffer wird zu Beginn gezählt
    while i + 1 < len(a) and j + 1 < len(b) and a[i + 1] == b[j + 1]:
        i += 1
        j += 1
        length += 1
    return i, j, length


def find_cluster(a, b, min_clus_length):
    """
    Findet Cluster in zwei Texten a und b.

    Args:
        a (str): Der erste Text.
        b (str): Der zweite Text.
        min_clus_length (int): Minimale Clusterlänge.

    Returns:
        List[Cluster]: Liste von Cluster-Objekten.
    """
    cluster_lst = []  # Ergebnisliste
    skips = 0  # Überspringe Indizes nach Clustertreffern
    len_a = len(a)
    for i in range(len(a)):
        print(f'{i} von {len_a}', end='\r')  # Fortschrittsanzeige
        if skips > 0:  # Überspringe Indizes basierend auf vorherigen Clustern
            skips -= 1
            continue

        cluster_object = Cluster(i)

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
    data_df['differenz'] = data_df['start_b'] - data_df['start_a']    
    
    print(f'100% -- Abgeschlossen', end='\r')
    return data_df


def compare_defter(a, b, cluster_df=pd.DataFrame(), text_name_a='text_a',text_name_b='text_b'):
    """
    Vergleicht zwei Texte (a und b) basierend auf einem Cluster-Dictionary und
    aktualisiert die geclusterten Texte.

    Args:
        a (list): Liste der Segmente des ersten Texts.
        b (list): Liste der Segmente des zweiten Texts.
        cluster_dict (dict): Dictionary mit Cluster-Informationen.

    Returns:
        dict: Aktualisiertes `clustered_text` mit neuen Einträgen.
    """
    
    # Wandle Dataframe in Dictionary um
    dict = cluster_df.to_dict(orient='tight',index=False)
    cluster_dict={}
    for i in range(6):
        cluster_dict[dict['columns'][i]]=[]
        for j in range(len(dict['data'])):
            cluster_dict[dict['columns'][i]].append(dict['data'][j][i])     
    # Bereite Dictionary für Ausgabe vor
    clustered_text = {'tag':[],f'Pos_{text_name_a}':[],f'Length_{text_name_a}':[],f'{text_name_a}':[],
                      f'Pos_{text_name_b}':[],f'Length_{text_name_b}':[],f'{text_name_b}':[],
                      'Length_Cluster':[],'Cluster':[]}
    
    # Validierung der Eingaben
    required_keys = ['start_a', 'end_a', 'start_b', 'end_b', 'length']
    if not all(key in cluster_dict for key in required_keys):
        raise ValueError(f"cluster_dict muss die Keys {required_keys} enthalten.")



    a_start = 0
    b_start = 0

    # Iteriere über alle Cluster
    for cluster_nr in range(len(cluster_dict['start_a'])):
        # Cluster-Start- und Endpositionen auslesen
        start_a, end_a = cluster_dict['start_a'][cluster_nr], cluster_dict['end_a'][cluster_nr]
        start_b, end_b = cluster_dict['start_b'][cluster_nr], cluster_dict['end_b'][cluster_nr]
        length = cluster_dict['length'][cluster_nr]

        # Uniques hinzufügen
        clustered_text['tag'].append('unique')
        clustered_text[f'Pos_{text_name_a}'].append(a_start)
        clustered_text[f'Pos_{text_name_b}'].append(b_start)
        clustered_text[f'Length_{text_name_a}'].append(start_a - a_start)
        clustered_text[f'Length_{text_name_b}'].append(start_b - b_start)
        clustered_text[f'{text_name_a}'].append('་'.join(a[a_start:start_a]))
        clustered_text[f'{text_name_b}'].append('་'.join(b[b_start:start_b]))
        clustered_text['Length_Cluster'].append(0)
        clustered_text['Cluster'].append('')

        # Cluster hinzufügen
        clustered_text['tag'].append('cluster') 
        clustered_text[f'Pos_{text_name_a}'].append(start_a)
        clustered_text[f'Pos_{text_name_b}'].append(start_b)
        clustered_text[f'Length_{text_name_a}'].append(0)
        clustered_text[f'Length_{text_name_b}'].append(0)
        clustered_text[f'{text_name_a}'].append('')
        clustered_text[f'{text_name_b}'].append('')
        clustered_text['Length_Cluster'].append(length)
        clustered_text['Cluster'].append('་'.join(a[start_a:end_a]))

        # Aktualisiere Startpositionen
        a_start = end_a
        b_start = end_b


    #wandle Dictionary in DataFrame um
    return pd.DataFrame(clustered_text)
