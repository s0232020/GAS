class MyQueue:
    def __init__(self, capacity):
        """
        Initialisatie van de queue met een array van opgegeven capaciteit.
        Front en rear worden geïnitialiseerd op respectievelijk 0 en -1.
        Size houdt het aantal elementen in de queue bij, en capacity is het maximale aantal elementen dat de queue kan bevatten.
        Precondities: 'capacity' moet een positief geheel getal zijn.
        Postcondities: Initialiseert de queue met de opgegeven capaciteit. Front en rear worden geïnitialiseerd op respectievelijk 0 en -1. Size wordt ingesteld op 0.
        """
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0
        self.capacity = capacity

    def createQueue(self):
        """
        Creëer een lege queue met dezelfde capaciteit.
        Precondities: Geen.
        Postcondities: Creëert een lege queue met dezelfde capaciteit. Front en rear worden gereset naar respectievelijk 0 en -1. Size wordt ingesteld op 0.
        """
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def destroyQueue(self):
        """
        Maak de queue leeg door alle elementen naar None te zetten en front/rear te resetten.
        Precondities: Geen.
        Postcondities: Maakt de queue leeg door alle elementen naar None te zetten. Front en rear worden gereset naar respectievelijk 0 en -1. Size wordt ingesteld op 0.
        """
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def isEmpty(self):
        """
        Controleer of de queue leeg is.
        Precondities: Geen.
        Postcondities: Retourneert True als de queue leeg is, anders False.
        """
        return self.size == 0

    def getFront(self):
        """
        Retourneer het element aan de achterkant van de queue als de queue niet leeg is, anders retourneer None.
         Precondities: Geen.
        Postcondities: Retourneert het element aan de achterkant van de queue als de queue niet leeg is, anders retourneert None. Het tweede element van de tuple geeft aan of de operatie is geslaagd.
        """
        return (self.queue[self.rear], False) if not self.isEmpty() else (None, False)

    def enqueue(self, data):
        """
        Voeg een nieuw element toe aan de voorkant van de queue.
        Als de queue vol is, retourneer False.
        Precondities: Geen.
        Postcondities: Voegt een nieuw element toe aan de voorkant van de queue. Retourneert True als de operatie is geslaagd, anders False.
        """
        if self.size == self.capacity:
            return False  # Queue is full

        self.front = (self.front - 1) % self.capacity
        self.queue[self.front] = data
        self.size += 1
        return True

    def dequeue(self):
        """
        Verwijder het element aan de achterkant van de queue.
        Als de queue leeg is, retourneer (None, False).
        Precondities: Geen.
        Postcondities: Verwijdert het element aan de achterkant van de queue en retourneert een tuple met het verwijderde element en True als de operatie is geslaagd, anders (None, False).
        """
        if self.isEmpty():
            return (None, False)

        self.rear = (self.rear - 1) % self.capacity
        data = self.queue[(self.rear + 1) % self.capacity]
        self.size -= 1

        return (data, True)

    def save(self):
        """
        Retourneer een lijst met de elementen in de huidige queue in volgorde van voorkant naar achterkant.
        Precondities: Geen.
        Postcondities: Retourneert een lijst met de elementen in de huidige queue in volgorde van voorkant naar achterkant.
        """
        return [self.queue[i] for i in range(self.front, self.front + self.size)]

    def load(self, newQueue):
        """
        Vernietig de huidige queue, creëer een nieuwe lege queue en voeg de elementen toe van de gegeven lijst aan de voorkant.
        Retourneer de nieuwe queue.
         Precondities: 'newQueue' moet een lijst zijn.
        Postcondities: Vernietigt de huidige queue, creëert een nieuwe lege queue en voegt de elementen toe van de gegeven lijst aan de voorkant. Retourneert de nieuwe queue.
        """
        self.destroyQueue()
        self.createQueue()
        for item in newQueue[::-1]:
            self.enqueue(item)
        return self.queue