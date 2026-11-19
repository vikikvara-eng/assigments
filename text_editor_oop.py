
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def insert_at(self, index, data):
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")

        new_node = Node(data)

        if index == 0:
            new_node.next = self.head
            self.head = new_node

            if self._size == 0:
                self.tail = new_node
        else:
            current = self.head

            for _ in range(index - 1):
                current = current.next

            new_node.next = current.next
            current.next = new_node

            if new_node.next is None:
                self.tail = new_node

        self._size += 1

    def delete_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")

        if index == 0:
            self.head = self.head.next

            if self._size == 1:
                self.tail = None
        else:
            current = self.head

            for _ in range(index - 1):
                current = current.next

            current.next = current.next.next

            if current.next is None:
                self.tail = current

        self._size -= 1

    def __iter__(self):
        current = self.head

        while current is not None:
            yield current.data
            current = current.next


class TextEditor:
    def __init__(self):
        self.lines = SinglyLinkedList()
        self.undo_stack = []
        self.redo_stack = []

    def add_line(self, text):
        index = self.lines._size
        self.lines.append(text)
        self.undo_stack.append(("insert", index, text))
        self.redo_stack.clear()

    def insert_line(self, index, text):
        self.lines.insert_at(index, text)
        self.undo_stack.append(("insert", index, text))
        self.redo_stack.clear()

    def delete_line(self, index):
        if index < 0 or index >= self.lines._size:
            raise IndexError("Index out of bounds")

        current = self.lines.head

        for _ in range(index):
            current = current.next

        text = current.data

        self.lines.delete_at(index)
        self.undo_stack.append(("delete", index, text))
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return

        action, index, text = self.undo_stack.pop()

        if action == "insert":
            self.lines.delete_at(index)
        elif action == "delete":
            self.lines.insert_at(index, text)

        self.redo_stack.append((action, index, text))

    def redo(self):
        if not self.redo_stack:
            return

        action, index, text = self.redo_stack.pop()

        if action == "insert":
            self.lines.insert_at(index, text)
        elif action == "delete":
            self.lines.delete_at(index)

        self.undo_stack.append((action, index, text))

    def show(self):
        for index, line in enumerate(self.lines, start=1):
            print(f"{index}. {line}")


editor = TextEditor()

editor.add_line("A")
editor.add_line("B")
editor.add_line("C")

editor.delete_line(1)
editor.undo()
editor.undo()
editor.redo()

editor.add_line("D")
editor.redo()

editor.show()
