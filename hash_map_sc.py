# Name: Kerry James Poulson
# OSU Email: poulsonk@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06.03.2022
# Description: This file contains an implementation of a HashMap using separate chaining to handle collisions.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """This method adds a key/value pair to the hash table. If the key is already present, its value is updated
        to the new value"""
        index = self._hash_function(key) % self.get_capacity()  # Returns an index to be used to place an element
        if self._buckets[index].contains(key) is None:
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            self._buckets[index].contains(key).value = value

    def empty_buckets(self) -> int:
        """This method returns the number of empty buckets in the hash table"""
        counter = 0
        for items in range(self.get_capacity()):
            if self._buckets[items].length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """This method returns the load factor of the hash table, calculated by dividing self._size by the
        length of the array"""
        return self._size / self._buckets.length()

    def clear(self) -> None:
        """This method clears the contents of the hash table"""
        my_aray = DynamicArray()
        for items in range(self.get_capacity()):
            my_aray.append(LinkedList())    # Replaces all elements in the DA to empty Linked Lists
        self._buckets = my_aray
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """This method changes the underlying capacity of the hash table"""
        if new_capacity < 1:
            return
        my_array = DynamicArray()
        for items in range(new_capacity):
            my_array.append(LinkedList())
        add_keys = self.get_keys()              # Calling this function allows for easier rehashing of the keys into
        for items in range(add_keys.length()):  # the different capacity HashTable
            value = self.get(add_keys[items])
            index = self._hash_function(add_keys[items]) % new_capacity
            my_array[index].insert(add_keys[items], value)
        self._capacity = new_capacity
        self._buckets = my_array

    def get(self, key: str) -> object:
        """This method returns the value associated with a given key in the hash table"""
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index].contains(key) is None:
            return None
        node = self._buckets[index].contains(key)
        return node.value

    def contains_key(self, key: str) -> bool:
        """This method returns True if a given key is present and returns False otherwise"""
        if self.get_size() == 0:
            return False
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index].contains(key) is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """This method remove the matching key/value pair from the hash table"""
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index].contains(key) is None:
            return
        self._buckets[index].remove(key)
        self._size -= 1

    def get_keys(self) -> DynamicArray:
        """This method returns all the keys in the hash table within a Dynamic Array"""
        my_array = DynamicArray()
        for items in range(self.get_capacity()):
            if self._buckets[items].length() != 0:
                current = self._buckets[items].__iter__()    # Creates an iterator object to allow traversal through
                new = current.__next__()                     # a Linked List
                while new is not None:
                    my_array.append(new.key)
                    new = new.next
            else:
                pass
        return my_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """This method finds the mode(s) in a Dynamic Array and returns a tuple of
    a Dynamic Array with the most occurring values and returns their frequencies"""
    map = HashMap(da.length() // 3, hash_function_1)
    my_array = DynamicArray()
    for items in range(da.length()):            # This for loop is used to Hash the elements in the DA.
        occurrences = 1                         # The key is the element and the corresponding value is the
        if map.contains_key(da[items]) is False:    # number of occurrences of that element in the DA
            map.put(da[items], occurrences)
        else:
            occurrences = map.get(da[items])
            occurrences += 1
            map.put(da[items], occurrences)
    my_keys = map.get_keys()
    occurrences = 0
    for items in range(my_keys.length()):           # This loop finds each unique key (string) and will alter the
        if map.get(my_keys[items]) == occurrences:  # DA, always storing the most occurring string in the DA and
            my_array.append(my_keys[items])         # changing occurrences to match
        elif map.get(my_keys[items]) > occurrences:
            while my_array.length() != 0:
                my_array.pop()
            my_array.append(my_keys[items])
            occurrences = map.get(my_keys[items])
    return my_array, occurrences


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
