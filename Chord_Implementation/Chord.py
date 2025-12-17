import csv


numberofData = 682  # Πλήθος δεδομένων που θα εισαχθούν στο δακτύλιο

class ChordRing:
    def __init__(self, nodes, ids):
        self.Nodes_List = nodes  # Λίστα κόμβων στο δακτύλιο του συστήματος Chord
        self.Nodes_Ids = ids  # Λίστα με τα IDs των κόμβων του συστήματος Chord
        self.start_node_id = 0  # Εδώ αρχικοποιούμε το ID του πρώτου κόμβου
        self.end_node_id = 0  # Εδώ αρχικοποιούμε το ID του τελευταίου κόμβου

    def update(self):
        # Καλούμε κάθε φορά την συνάρτηση για να ενημερώσουμε τον δακτύλιο
        self.start_node = self.Nodes_List[0] # Τοποθετούμε τον πρώτο κόμβο του δακτυλίου σε μία μεταβλητή start_node
        self.end_node = self.Nodes_List[len(self.Nodes_List) - 1] # Όμοια για το τελευταίο στοιχείο του δακτυλίου
        self.start_node_id = self.Nodes_Ids[0] # Τοποθετούμε τα id που αποθηκεύουμε στην λίστα με τα ids σε δύο μεταβλητές
        self.end_node_id = self.Nodes_Ids[len(self.Nodes_Ids) - 1]
        self.Nodes_List.sort(key=lambda n: n.node_id) # Κάνουμε sorting την λίστα με τους κόμβους που έχουμε στον δακτύλιο κάθε φορά για να τοποθετούνται οι κόμβοι στην σωστή σειρά

# Κλάση η οποία αφορά τον κάθε κόμβο και ανάλογα με την ενέργεια που θέλουμε να ακολουθήσουμε,
# αξιοποιούμε τις συναρτήσεις που έχουμε υλοποιήσει στην κλάση αυτή 
class ChordNode:
    def __init__(self, node_id, chord_ring): # Ο constructor της κλάσης μας
        self.node_id = node_id  # ID του κόμβου
        self.successor = None  # Διάδοχος κόμβος
        self.predecessor = None  # Προκάτοχος κόμβος
        self.finger = []  # Πίνακας που θα αποθηκεύει τα finger
        self.ring = chord_ring  # Δακτύλιος στον οποίο ανήκει ο κόμβος και σχετίζεται με την κλάση ChordRing
        self.key_store = {}  # Εδώ αποθηκεύονται τα κλειδιά μαζί μετα δεδομένα που θα τοποθετηθούν στους κόμβους

    def add_key_value_pair(self, key, surname, awards):
        # Προσθήκη ζεύγους κλειδιού-τιμής στον κόμβο όπου το κλειδί θα είναι το πεδίο education και 
        # και η τιμή θα έχει τα πεδία surname και awards
        self.key_store[key] = {'surname': surname, 'awards': awards}

    def finger_table(self):
        # Υπολογισμός του finger table για κάθε κόμβο
        for i in range(0, m):
            s = (self.node_id + (2**i)) % (2**m) 
            self.finger.append(self.find_successor_id(s)) # Κλήση της find_successor ώστε να εντοπίζουμε κάθε φορά τον σωστό κόμβο, ώστε να αποθηκευτεί στο finger table

    def update_successor_predeccessor(self): # Συνάρτηση η οποία ανανεώνει κάθε φορά τον predeccessor και τον successor κάθε κόμβου
        counter = 0
        
        # Ενημέρωση του successor και predeccessor του κόμβου
        if self.node_id == self.ring.start_node_id: # Εάν ο τρέχοντας κόμβος ισούται με τον αρχικό κόμβο στον δακτύλιο 
            self.successor = self.ring.Nodes_List[1]
            self.predecessor = self.ring.Nodes_List[len(self.ring.Nodes_List) - 1]
        elif self.node_id == self.ring.end_node_id: # Εάν ο τρέχοντας κόμβος είναι ο τελευταίος, τότε ανέθεσε σαν successor τον πρώτο κόμβο
            self.successor = self.ring.start_node
            self.predecessor = self.ring.Nodes_List[len(self.ring.Nodes_List) - 2]
        else: # Διαφορετικά αναζήτησε εσωτερικά στον δακτύλιο 
              # Προσαρμόζουμε για κάθε κόμβο τον successor και τον predeccessor του
            for i in range(0, len(self.ring.Nodes_List)): 
                if self.ring.Nodes_List[i].node_id < self.node_id: 
                    counter += 1
            self.successor = self.ring.Nodes_List[(counter + 1) % len(self.ring.Nodes_List)]
            self.predecessor = self.ring.Nodes_List[(counter - 1) % len(self.ring.Nodes_List)]

    
    def find_successor_id(self, key): # Με την συγκεκριμένη συνάρτηση εντοπίζουμε τον successor κάθε κόμβου με βάση το κλειδί που δώσαμε σαν όρισμα
        
        if self.node_id == key: # Εάν το id του κόμβου ισούται με το κλειδί, τότε επέστρεψε σαν successor τον ίδιο τον κόμβο
            return self.node_id
        elif self.node_id < key <= self.successor.node_id: # Εάν το κλειδί είναι μεγαλύτερο απο τον τρέχοντα κόμβο και μικρότερο ή ίσο από τον successor εκείνου του κόμβου, επέστρεψε τον successor του κόμβου όπου αναζητούμε αυτή την στιγμή 
            return self.successor.node_id
        elif self.successor.node_id < self.node_id and (key < self.successor.node_id or self.node_id < key): # Εάν ο κόμβος είναι ο τελευταίος στον δακτύλιο, τότε επέστρεψε τον successor του τελευταίου κόμβου
            return self.successor.node_id
        else: # Εάν δεν ισχύουν τα παραπάνω, τότε καλούμε αναδρομικά την συνάρτηση μεχρι να εντοπίσουμε τον successor που αναζητούμε με βάση το κλειδί που δώσαμε σαν όρισμα
            return self.successor.find_successor_id(key)
        
    def find_successor(self, key): # Λειτουργεί με παρόμοιο τρόπο όπως η find_successor_id και αξιοποιείται στην συνάρτηση lookup για την εύρεση κάποιου κόμβου με βάση το κλειδί  
        
        if self.node_id == key:
            return self
        elif self.node_id < key <= self.successor.node_id:
            return self.successor
        elif self.successor.node_id < self.node_id and (key < self.successor.node_id or self.node_id < key):
            return self.successor
        else:
            return self.successor.find_successor(key)

    
    def join(self, chord_ring):
        # Τοποθέτηση του κόμβου στο δακτύλιο
        self.ring = chord_ring
        self.ring.Nodes_List.append(self)  # Προσθήκη του κόμβου στη λίστα των κόμβων
        self.ring.Nodes_Ids.append(self)  # Προσθήκη του κόμβου στη λίστα με τα Ids των κόμβων
        self.ring.update()  # Ενημέρωση του δακτυλίου με τη νέα προσθήκη

        # Ενημέρωση των successor και predeccessor
        self.update_successor_predeccessor()  # Ενημέρωση του διαδόχου και προκατόχου του νέου κόμβου
        for nodes in self.ring.Nodes_List:
            nodes.update_successor_predeccessor()  # Ενημέρωση των διαδόχων και προκατόχων όλων των κόμβων
        self.finger_table()  # Ενημέρωση του πίνακα finger του κόμβου

        # Εύρεση του διαδόχου του νέου κόμβου που κάναμε εισαγωγή
        successor_index = (self.ring.Nodes_List.index(self) + 1) % len(self.ring.Nodes_List)
        successor = self.ring.Nodes_List[successor_index]

        # Μεταφορά ενός στοιχείου από τον διαδόχο κόμβο, στον νέο κόμβο μόλις εισήχθει
        if successor != self:
            # Παίρνουμε το κλειδί και το ένα από τα δεδομένα του διαδόχου κόμβου
            keys_to_transfer = list(successor.key_store.keys())
            if keys_to_transfer:
                # Επιλογή του κλειδιού για μεταφορά απο την λίστα
                key_to_transfer = keys_to_transfer[0]
                # Αφαίρεση του κλειδιού και ενός από τα δεδομένα από τον διάδοχο κόμβο ώστε να τοποθετηθούν στον καινούριο κόμβο
                value_to_transfer = successor.key_store.pop(key_to_transfer)
                # Προσθήκη του κλειδιού και ενός από τα δεδομένα στον νέο κόμβο
                self.key_store[key_to_transfer] = value_to_transfer


    def leave(self):
        # Αποχώρηση του κόμβου από τον δακτύλιο
        if self.ring is not None:
            if self in self.ring.Nodes_Ids:
                self.ring.Nodes_Ids.remove(self)
            self.ring.Nodes_List.remove(self)
            self.ring.update()

            # Εύρεση νέου διαδόχου χρησιμοποιώντας την find_successor
            new_successor_id = self.find_successor_id(self.node_id + 1)
            new_successor = self.ring.Nodes_List[0].find_successor(new_successor_id)

            # Μεταφορά δεδομένων στο νέο διάδοχο
            new_successor.key_store.update(self.key_store)

            # Αφαίρεση των δεδομένων από τον αποχωρούντα κόμβο
            self.key_store = {}

            # Ενημέρωση των κόμβων για τους νέους διαδόχους
            for nodes in self.ring.Nodes_List:
                nodes.update_successor_predeccessor()
            self.finger_table()
    
    def lookup(self, key):
        # Συνάρτηση για την αναζήτηση του κόμβου που αντιστοιχεί στο κλειδί
        successor_id = self.find_successor_id(key)

        # Βρέθηκε ο κόμβος που αντιστοιχεί στο κλειδί
        if successor_id == self.node_id:
            return self
        else:
            # Καλεί τη συνάρτηση find_successor για τον πραγματικό κόμβο
            return self.find_successor(key)

    


def create_chord_ring(m, ids):
    # Δημιουργία του δακτυλίου Chord και ενημέρωση των κόμβων
    chord_create = [ChordNode(i, None) for i in ids]
    chord_ring = ChordRing(chord_create, ids)
    for node in chord_create:
        node.ring = chord_ring
        node.update_successor_predeccessor()

    return chord_ring

def print_successor_predecessor(chord_ring):
    # Εκτύπωση των διαδόχων και προκατόχων κάθε κόμβου (predeccessors και successors)
    for node in chord_ring.Nodes_List:
        print(f"Node {node.node_id}: Successor - {node.successor.node_id}, Predecessor - {node.predecessor.node_id}")

def print_node_data(chord_ring):
    # Εκτύπωση των δεδομένων κάθε κόμβου
    for node in chord_ring.Nodes_List:
        print(f"Node {node.node_id}: {node.key_store}")

def display_menu():
    # Εμφάνιση μενού επιλογών
    print("Καλώς ήρθατε στον Δακτύλιο Chord:")
    print("1. Εισαγωγή Κόμβου")
    print("2. Διαγραφή Κόμβου")
    print("3. Εκτύπωση Διαδόχων και Προκατόχων")
    print("4. Εκτύπωση Δεδομένων κάθε Κόμβου")
    print("5. Αναζήτηση δεδομένων με βάση το κλειδί")
    print("6. Αναζήτηση σε κόμβο με βάση το Πανεπιστήμιο και τον αριθμό των βραβείων")
    print("7. Έξοδος")

def load_data_from_csv(filename):
    # Φόρτωση των δεδομένων που ανακτήθηκαν από τον crawler και τοποθετήθηκαν στο CSV αρχείο
    data = []

    with open(filename, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        for row in reader:
            surname, awards, education = row
            data.append({'surname': surname, 'awards': awards, 'education': education})

    return data

def hash_function(value, m):
    # Υποθέτουμε ότι η hash function θα επιστρέφει την τιμή μεταξύ 0 και 2^m-1
    return hash(value) % (2**m)

if __name__ == "__main__":
    # Φόρτωση των δεδομένων από το CSV αρχείο
    csv_data = load_data_from_csv('output3.csv')
    m = 10
    ids = [hash_function(i, m) for i in range(numberofData)]
    
    # Δημιουργία του δακτυλίου Chord και εισαγωγή των δεδομένων στους κόμβους
    chord_ring = create_chord_ring(m, ids)

    for i, node in enumerate(chord_ring.Nodes_List):
        if i < len(csv_data):
            entry = csv_data[i]
            key = entry['education']
            surname = entry['surname']
            awards = entry['awards']
            node.add_key_value_pair(key, surname, awards)

    # Είσοδος στο κύριο μενού
    while True:
        display_menu()
        choice = input("Επιλέξτε την επιλογή σας (1-7): ")
        # Εισαγωγή νέου κόμβου στον δακτύλιο
        if choice == "1":
            put_id = int(input("Εισαγωγή του ID του νέου κόμβου: "))
            n = ChordNode(put_id, None)
            n.join(chord_ring)
            
        # Διαγραφή κάποιου κόμβου από τον δακτύλιο
        elif choice == "2":
            put_id = int(input("Εισαγωγή του ID του κόμβου που θέλετε να διαγράψετε: "))
            for nodes in chord_ring.Nodes_List:
                if nodes.node_id == put_id:
                    nodes.leave()
            
        # Εκτυπώνουμε τους successors και τους predeccessors για κάθε κόμβο
        elif choice == "3":
            print_successor_predecessor(chord_ring)
        # Εκτυπώνουμε τα δεδομένα όλων των κόμβων
        elif choice == "4":
            print_node_data(chord_ring)

        # Αναζήτηση με lookup όπου ο χρήστης εισάγει σαν όρισμα το κλειδί και λαμβάνει τον κόμβο που αντιστοιχεί στο κλειδί αυτό με τα δεδομένα του 
        elif choice == "5":
            key = int(input("Εισαγωγή του κλειδιού για αναζήτηση: "))
            result_node = chord_ring.Nodes_List[0].lookup(key)
            print(f"Ο κόμβος που αντιστοιχεί στο κλειδί {key} είναι ο κόμβος {result_node.node_id}")
            
            # Εκτύπωση των δεδομένων του κόμβου που βρέθηκε
            print(f"Δεδομένα του κόμβου {result_node.node_id}: {result_node.key_store}")
        # Εκτέλεση ενός query και αναζήτηση στον κόμβο με βάση το Πανεπιστήμιο και των αριθμό των βραβείων που εισήγαγε ο χρήστης
        elif choice == "6":
            node_id = int(input("Εισαγωγή του ID του κόμβου για την αναζήτηση: "))
            education = input("Εισαγωγή του Πανεπιστημίου: ")
            awards = int(input("Εισαγωγή του αριθμού των Βραβείων: "))
            
            for node in chord_ring.Nodes_List:
                if node.node_id == node_id:
                    # Εκτέλεση της επιθυμητής λειτουργίας για τον επιλεγμένο κόμβο
                    scientists = []
                    for key, value in node.key_store.items():
                        # Έλεγχος αν το κλειδί είναι ίσο με την επιλεγμένη εκπαίδευση ("education")
                        if key == education and int(value['awards']) >= awards:
                            scientists.append(value['surname'])

                    if scientists:
                        print(f"Οι επιστήμονες που έκαναν βασικές σπουδές στο {education} και έχουν αποσπάσει > {awards} βραβεία είναι: {', '.join(scientists)}")
                    else:
                        print("Δεν βρέθηκαν επιστήμονες που πληρούν τα κριτήρια.")
        # Έξοδος από το σύστημα
        elif choice == "7":
            print("Έξοδος από το πρόγραμμα. Αντίο!")
            break

        else:
            # Μήνυμα για μη έγκυρη επιλογή από το menu των επιλογών
            print("Μη έγκυρη επιλογή. Παρακαλώ εισάγετε έναν αριθμό μεταξύ του 1 και του 7.")
