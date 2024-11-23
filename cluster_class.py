class Cluster:
    def __init__(self, position_a):
        """
        Initialisiert eine neue Cluster-Instanz.

        Args:
            position_a (int): Die Startposition des Clusters im Text A.
        """
        # Startposition im Text A
        self.pos_a = position_a

        # Bezeichnung der Cluster-Tupel-Elemente für bessere Lesbarkeit
        self.clus_tupel_naming = ('start_a', 'end_a', 'start_b', 'end_b', 'length')

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
        