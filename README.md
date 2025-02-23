**HashMap**

    This project is a demonstration of the Hash data structure in Python. HashMap uses different
    structures for collision resolution including Seperate Chaining and Open Addressing.
    
    Seperate Chaining transforms each node in the Hash table into its own Linked List. Values
    that are mapped to the same node in the table are chained onto the end of the Linked List.

    The Open Addressing scheme uses a Dynamic Array to store vales in the table. If a value is
    maped via hash function to an occupied space in the array, a new spot is discovered using 
    quadratic probing.
