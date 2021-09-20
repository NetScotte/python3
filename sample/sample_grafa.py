"""
故事：
    实现一个图
    可以添加数据（a, b, 0)
    可以删除数据 (a, b, 0)
    可以找出从节点A到节点B的路径，给出路径，值
"""
import queue
import unittest

class Fig:
    def __init__(self, data=None):
        self.data = {}
        for item in data:
            if item:
                self.update(item)

    def update(self, item):
        assert len(item) == 3, "illege item, must be three tuple"
        if item[0] not in self.data:
            self.data[item[0]] = {item[1]: item[2]}
        elif item[1] not in self.data[item[0]]:
            self.data[item[0]][item[1]] = item[2]
        else:
            self.data[item[0]][item[1]] = item[2]

        if item[1] not in self.data:
            self.data[item[1]] = {item[0]: item[2]}
        elif item[0] not in self.data[item[1]]:
            self.data[item[1]][item[0]] = item[2]
        else:
            self.data[item[1]][item[0]] = item[2]

    def remove(self, item):
        if item[0] in self.data:
            if item[1] in self.data[item[0]]:
                del self.data[item[0]][item[1]]

        if item[1] in self.data:
            if item[0] in self.data[item[1]]:
                del self.data[item[1]][item[0]]

        if len(self.data[item[0]].keys()) == 0:
            del self.data[item[0]]

        if len(self.data[item[1]].keys()) == 0:
            del self.data[item[1]]

    def find(self, src, dest):
        if src not in self.data or dest not in self.data:
            return None, None, None

        valid_path = []
        q = queue.Queue()
        q.put((src, [], 0))

        # 将要访问某个对象，需要知道前置的路径，前置路径长度，已经访问过的数据
        while not q.empty():
            i, current, weight = q.get()
            for j in self.data[i]:
                if j == dest:
                    valid_path.append((current + [i, j], weight + self.data[i][j]))
                elif j not in current:
                    q.put((j, current + [i], weight + self.data[i][j]))
        return valid_path



class myTest(unittest.TestCase):
    def test_myfig(self):
        fig = Fig([
            ("a", "b", 2),
            ("a", "c", 2),
            ("a", "d", 3),
            ("b", "a", 2),
            ("b", "d", 2),
            ("c", "a", 2),
            ("d", "a", 3),
            ("d", "b", 2),
            ("d", "e", 2),
            ("d", "g", 2),
            ("e", "d", 2),
            ("e", "g", 2),
            ("g", "d", 2),
            ("g", "e", 2)
        ])

        print(fig.find("a", "e"))







