import queue
import unittest

class Name:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class myTest(unittest.TestCase):
    def test_queue(self):
        """测试先进新出队列"""
        q = queue.Queue(20)
        for i in range(5):
            q.put(i)

        while not q.empty():
            print(q.get())


    def test_lifoqueue(self):
        """测试先进后出队列"""
        q = queue.Queue(20)
        for i in range(5):
            q.put(i)

        while not q.empty():
            print(q.get())


    def test_priorityqueue(self):
        """基本测试"""
        q = queue.PriorityQueue(20)
        info = [
            (22, "netliu"),
            (18, "july"),
            (30, "liuxing"),
            (10, "keqi")
        ]
        for i in info:
            print(i)
            q.put(i)
        while not q.empty():
            print(q.get())

    def test_priorityqueue2(self):
        """测试不可比较对象"""
        q = queue.PriorityQueue(20)
        info = [
            (22, Name("netliu")),
            (18, Name("july")),
            (30, Name("liuxing")),
            (10, Name("keqi"))
        ]
        for i in info:
            print(i)
            q.put(i)
        while not q.empty():
            print(q.get())



if __name__ == "__main__":
    unittest.main()


