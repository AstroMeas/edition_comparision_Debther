class Cluster:
    def __init__(self, position_a,text_a_name='text_a',text_b_name='text_b'):
        """
    Represents a cluster of matching elements between two sequences and manages related data.

    The `Cluster` class helps store and process information about clusters of matching elements 
    identified between two texts or sequences. It supports adding clusters, naming the cluster components, 
    and selecting the largest cluster for final processing.

    Attributes:
        pos_a (int): The starting position of the cluster in the first sequence (`text_a`).
        clus_tupel_naming (tuple): A tuple defining the names for cluster elements in the format 
            (start of text_a, end of text_a, start of text_b, end of text_b, length).
        clusters (list): A list of all clusters identified for this starting position.
        final_cluster (list): The cluster with the maximum length, stored as a list of 
            [start_a, end_a, start_b, end_b, length].

    Methods:
        append_cluster(pos_b, cluster_length):
            Adds a new cluster to the `clusters` list, including its start and end positions in both sequences 
            and its length.

        pick_finalcluster():
            Selects the cluster with the maximum length from the `clusters` list and assigns it to `final_cluster`.

    Example:
        cluster = Cluster(5, text_a_name="document1", text_b_name="document2")
        cluster.append_cluster(10, 3)
        cluster.pick_finalcluster()
        print(cluster.final_cluster)
        # Output: [5, 8, 10, 13, 3]
    """

        # Startposition im Text A
        self.pos_a = position_a

        # Bezeichnung der Cluster-Tupel-Elemente für bessere Lesbarkeit
        self.clus_tupel_naming = (f'start_{text_a_name}', f'end_{text_a_name}', f'start_{text_b_name}', f'end_{text_b_name}', 'length')

        # Liste zur Speicherung der Cluster-Daten
        self.clusters = []

        # Speichert den Clusterinhalt mit der größten Länge
        self.final_cluster = ''

    def append_cluster(self, pos_b, cluster_length):
        """
        Fügt einen identischen Cluster aus Text B hinzu, unter Angabe der 
        Startposition und Länge

        Args:
            pos_b (int): Startposition des Clusters im Text B.
            cluster_length (int): Die Länge des Clusters.
        """
        # Ein neuer Cluster wird als Liste gespeichert und zu self.clusters hinzugefügt
        # Die Liste enthält [start_a, end_a, start_b, end_b, length]
        self.clusters.append([
            self.pos_a,  # Start im Text A
            self.pos_a + cluster_length,  # Ende im Text A
            pos_b,  # Start im Text B
            pos_b + cluster_length,  # Ende im Text B
            cluster_length  # Länge des Clusters
        ])

    def pick_finalcluster(self):
        """
        Wählt den Cluster in Text B mit der größten Länge aus der Cluster-Liste aus
        und speichert ihn als finalen Cluster.
        """
        if self.clusters:
        # Nutzt max() mit einem Schlüssel für die Länge
            self.final_cluster = max(self.clusters, key=lambda x: x[-1])
        