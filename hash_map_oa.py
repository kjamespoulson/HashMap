# Name: Kerry James Poulson
# OSU Email: poulsonk@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06.03.2022
# Description: This file contains an implementation of a HashMap using open-addressing to
#              handle collisions.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
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
        """This method adds a HashEntry to the HashMap using quadratic probing"""
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)
        stage = 0
        index = (self._hash_function(key) + stage ** 2) % self.get_capacity()
        while index < self.get_capacity():
            if self.buckets[index] is None:
                self.buckets[index] = HashEntry(key, value)    # This method functions similarly to the method in
                self._size += 1                                 # hash_map_sc.py with the additional check for a
                break                                           # tombstone
            elif self.buckets[index].is_tombstone is True:
                self.buckets[index].value = value
                self.buckets[index].is_tombstone = False
                break
            elif self.buckets[index].key == key:
                self.buckets[index].value = value
                break
            else:
                stage += 1
                index = (self._hash_function(key) + stage ** 2) % self.get_capacity()

    def table_load(self) -> float:
        """This method returns the load factor of the HashTable"""
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """This method returns the number of empty buckets in the HashTable"""
        count = 0
        for items in range(self.get_capacity()):
            if self.buckets[items] is None:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """This method resizes the HashTable"""
        if new_capacity < 1 or new_capacity < self.get_size():
            return
        # This while loop ensures that the new_capacity will actually be enough
        # to store all the HashEntries with
        while (self.get_size() / new_capacity) >= 0.5:
            new_capacity *= 2
        # Save old attributes of self
        # Initialize new HashMap instance
        new_hash = HashMap(new_capacity, self._hash_function)
        old_keys = self.get_keys()
        for items in range(old_keys.length()):
            new_hash.put(old_keys[items], self.get(old_keys[items]))
        self.buckets = new_hash.buckets
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """This method returns the value associated with the given key or
        returns None if the key does not exist in the array"""
        stage = 0
        index = (self._hash_function(key) + stage ** 2) % self.get_capacity()
        while index < self.get_capacity():
            if self.buckets[index] is None:
                return None
            elif self.buckets[index].key == key and self.buckets[index].is_tombstone is False:
                return self.buckets[index].value
            else:
                stage += 1
                index = (self._hash_function(key) + stage ** 2) % self.get_capacity()

    def contains_key(self, key: str) -> bool:
        """This method takes a key and returns True if it is present in the Hash Table and False otherwise"""
        if self.get(key) is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """This method removes a key from the array by setting HashEntry.is_tombstone = True"""
        stage = 0
        index = (self._hash_function(key) + stage ** 2) % self.get_capacity()
        while index < self.get_capacity():
            if self.buckets[index] is None:
                return
            elif self.buckets[index].key == key and self.buckets[index].is_tombstone is False:
                self.buckets[index].is_tombstone = True
                self._size -= 1
            else:
                stage += 1
                index = (self._hash_function(key) + stage ** 2) % self.get_capacity()

    def clear(self) -> None:
        """This method clears the HashTable by setting all elements to None"""
        for items in range(self.get_capacity()):
            self.buckets[items] = None
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """This method returns an array containing all the keys in the HashTable"""
        return_array = DynamicArray()
        for items in range(self.get_capacity()):
            if self.buckets[items] is not None:
                if self.buckets[items].is_tombstone is False:
                    return_array.append(self.buckets[items].key)
        return return_array


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
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(),
              round(m.table_load(), 2))

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