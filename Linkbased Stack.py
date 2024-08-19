class MyStack:
    def __init__(self):
        self.top = None
    def load(self, newStack): # Nieuwe stack als parameter, deze inhoud moet naar de stack gepushed worden
        """
        Laad een nieuwe stack en verwijdert de oude
        Preconditie: Geen
        Postconditie: De stack is even groot als de lijst
        :param newStack:
        :return: Deze functie geeft de ingevoerde stack terug als een lijst
        """
        self.destroyStack()
        self.createStack()
        self.push(newStack[0])
        for i in newStack[1:]: # Deze loop gaat elk item van de nieuwe stack pushen
            self.push(i)
        return self.top
    def save(self):
        """
        Slaagt de lijst op en drukt deze af op het scherm
        Preconditie: Geen
        Postconditie: De volledige stack wordt afgedrukt
        :return: Deze functie geeft de een afgeprinte lijst terug
        """
        stack = []
        kopie = self.top
        while kopie is not None: # Deze loop gaat een kopie van de stack maken in een lijst en deze afdrukken
            stack.append(kopie[0])
            kopie = kopie[1]
        return stack[::-1] # We returnen het inverse van de lijst
    def createStack(self):
        """
        maak een lege stack aan
        Preconditie: De oproeper heeft eerst de stack verwijderd voor dat zij een nieuwe aanmaakt
        Postconditie: Je krijgt een nieuwe, lege stack
        :return: Deze functie heeft geen return
        """
        self.top = None
    def destroyStack(self):
        """
        wis de stack
        Preconditie: Geen
        Postconditie: De stack wordt in zijn geheel verwijderd
        :return: Deze functie heeft geen return
        """
        self.top = None
    def isEmpty(self):
        """
        bepaal of een stack leeg is
        Preconditie: Geen
        Postconditie: Dit commando verandert niets aan de stack zelf
        :return: True wanneer de stack leeg is, False wanneer die niet leeg is
        """
        return self.top is None
    def push(self, data): # Data is het element dat de gebruiker heeft meegegeven dat moet worden toegevoegd aan onze stack
        """
        voeg een element toe aan de top van de stack
        Preconditie: Er is nog plaats op de stack
        Postconditie: De stack is 1 item groter en bevat het toegevoegde item aan de top
        :param data:
        :return: True wanneer dit gelukt is
        """
        self.top = (data, self.top)
        return True
    def pop(self):
        """
        verwijder het laatst toegevoegde element
        Preconditie: De stack is niet leeg
        Postconditie: Item aan de top van de stack wordt verwijderd, stack verminder in grootte met 1
        :return: False wanneer de stack leeg is, als de stack niet leeg is krijg je het verwijderde item te zien
        """
        if self.isEmpty(): # Als de stack leeg is krijgen we een False return
            return (None, False)
        data = self.top[0] # Als de stack niet leeg is verwijderen we de top
        self.top = self.top[1]
        return (data, True) # We geven de data terug
    def getTop(self):
        """
        vraag het laatst toegevoegde element van de stack op
        Preconditie: De stack wordt niet aangepast
        Postconditie: De stack worrdt niet aangepast
        :return: False wanneer de stack leeg is, als de stack niet leeg is krijg je de waarde van de top terug
        """
        return self.top if self.top is not None else (None, False) # Als de stack leeg is geven we False terug