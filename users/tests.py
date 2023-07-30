#
#
# class CircularBufferList:
#     def __init__(self, capacity):
#         self.capacity = capacity
#         self.buffer = []
#
#     def is_empty(self):
#         return len(self.buffer) == 0
#
#     def is_full(self):
#         return len(self.buffer) == self.capacity
#
#     def enqueue(self, item):
#         if self.is_full():
#             self.buffer.pop(0)
#         self.buffer.append(item)
#
#     def dequeue(self):
#         if self.is_empty():
#             raise IndexError("Buffer is empty")
#         return self.buffer.pop(0)
#
# class CircularBufferArray:
#     def __init__(self, capacity):
#         self.capacity = capacity
#         self.buffer = [None] * capacity
#         self.head = 0
#         self.tail = 0
#         self.size = 0
#
#     def is_empty(self):
#         return self.size == 0
#
#     def is_full(self):
#         return self.size == self.capacity
#
#     def enqueue(self, item):
#         if self.is_full():
#             self.head = (self.head + 1) % self.capacity
#         self.buffer[self.tail] = item
#         self.tail = (self.tail + 1) % self.capacity
#         self.size += 1
#
#     def dequeue(self):
#         if self.is_empty():
#             raise IndexError("Buffer is empty")
#         item = self.buffer[self.head]
#         self.head = (self.head + 1) % self.capacity
#         self.size -= 1
#         return item
#
#
# from timeit import timeit
# print(timeit(lambda:CircularBufferList(100).enqueue(1), number=100000))
# # 0.03790120000485331
# print(timeit(lambda:CircularBufferArray(100).enqueue(1), number=100000))
# # 0.09426479996182024
#
#
#
#
#
# # Задаем функции, которые нужно измерить
# def test_list():
#     CircularBufferList(100).enqueue(1)
#
# def test_array():
#     CircularBufferArray(100).enqueue(1)
#
# # Измеряем время выполнения и выводим результаты
# list_time = timeit(test_list, number=100000)
# print("Время выполнения для CircularBufferList:", list_time)
#
# array_time = timeit(test_array, number=100000)
# print("Время выполнения для CircularBufferArray:", array_time)

# from collections import deque
# from timeit import timeit
#
# class CircularBuffer1:
#     def __init__(self, capacity):
#         self.capacity = capacity
#         self.buffer = [None] * capacity
#         self.size = 0
#         self.head = 0
#
#     def is_empty(self):
#         return self.size == 0
#
#     def is_full(self):
#         return self.size == self.capacity
#
#     def enqueue(self, item):
#         if self.is_full():
#             self.head = (self.head + 1) % self.capacity
#         else:
#             self.size += 1
#         self.buffer[(self.head + self.size - 1) % self.capacity] = item
#
#     def dequeue(self):
#         if self.is_empty():
#             raise IndexError("Buffer is empty")
#         item = self.buffer[self.head]
#         self.head = (self.head + 1) % self.capacity
#         self.size -= 1
#         return item
#
#
# class CircularBuffer2:
#     def __init__(self, capacity):
#         self.capacity = capacity
#         self.buffer = deque(maxlen=capacity)
#
#     def is_empty(self):
#         return not self.buffer
#
#     def is_full(self):
#         return len(self.buffer) == self.capacity
#
#     def enqueue(self, item):
#         self.buffer.append(item)
#
#     def dequeue(self):
#         if self.is_empty():
#             raise IndexError("Buffer is empty")
#         return self.buffer.popleft()
#
#
# print(timeit(lambda:CircularBuffer1(100).enqueue(1), number=100000))
# # 0.09110540000256151
# print(timeit(lambda:CircularBuffer2(100).enqueue(1), number=100000))
# # 0.0496926000341773



def quicksort(array):
    if len(array) <= 1:
        return array

    pivot = array[len(array) // 2]
    smaller = [x for x in array if x < pivot]
    equal = [x for x in array if x == pivot]
    larger = [x for x in array if x > pivot]

    return quicksort(smaller) + equal + quicksort(larger)

array = [4, 3, 1, 2]
x = quicksort(array)
print(x)



