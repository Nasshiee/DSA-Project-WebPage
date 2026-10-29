class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    def __repr__(self):
        return f"Node({self.data})"
class Queue:
    DEFAULT_CAPACITY = 20
    def __init__(self, max_capacity: int = DEFAULT_CAPACITY):
        self.head = None
        self.tail = None
        self._size = 0
        self.max_capacity = max_capacity
    def is_empty(self) -> bool:
        return self.head is None
    def is_full(self) -> bool:
        return self._size >= self.max_capacity
    def size(self) -> int:
        return self._size
    def enqueue(self, data):
        if data is None or not str(data).strip():
            raise ValueError("Cannot enqueue empty element. Please enter a valid value.")
        clean_data = str(data).strip()
        if len(clean_data) > 50:
            raise ValueError("Element exceeds maximum length of 50 characters.")
        if self.is_full():
            raise OverflowError(
                f"Queue Overflow: Cannot enqueue. Maximum capacity of {self.max_capacity} items reached."
            )
        new_node = Node(clean_data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
    queue = enqueue
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue Underflow: Cannot dequeue from an empty queue.")
        removed_data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return removed_data
    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek: The queue is currently empty.")
        return self.head.data
    front = peek
    def clear(self):
        if self.is_empty():
            raise ValueError("Queue is already empty.")
        self.head = None
        self.tail = None
        self._size = 0
    def to_list(self) -> list:
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
    @classmethod
    def from_list(cls, items: list, max_capacity: int = DEFAULT_CAPACITY):
        q = cls(max_capacity=max_capacity)
        for item in items:
            q.enqueue(item)
        return q
    def __str__(self) -> str:
        if self.is_empty():
            return "Front (Head) -> [ Empty Queue ] <- Rear (Tail)"
        items = []
        current = self.head
        while current is not None:
            items.append(f"[{current.data}]")
            current = current.next
        return "Front (Head) -> " + " -> ".join(items) + " -> Rear (Tail)"
def interactive_demo():
    q = Queue()
    for item in ["Customer A", "Customer B", "Customer C"]:
        q.enqueue(item)
    while True:
        print("\n" + "=" * 55)
        print("      LINKED LIST QUEUE (FIFO) INTERACTIVE DEMO")
        print("=" * 55)
        print("Current Queue:")
        print(q)
        print(f"Items count  : {q.size()} / {q.max_capacity}")
        print("-" * 55)
        print("1. enqueue(data) / queue(data)")
        print("2. dequeue()")
        print("3. peek() / front()")
        print("4. clear()")
        print("5. Exit")
        print("-" * 55)
        choice = input("Select an option (1-5): ").strip()
        try:
            if choice == "1":
                data = input("Enter element to enqueue: ")
                q.enqueue(data)
                print(f"-> Successfully enqueued '{data.strip()}' at the rear (tail).")
            elif choice == "2":
                removed = q.dequeue()
                print(f"-> Successfully dequeued '{removed}' from the front (head).")
            elif choice == "3":
                front_item = q.peek()
                print(f"-> Front element (peek): '{front_item}'.")
            elif choice == "4":
                q.clear()
                print("-> Queue has been cleared.")
            elif choice == "5":
                print("\nExiting Queue Demo. Goodbye!\n")
                break
            else:
                print("-> Invalid option. Please select 1 through 5.")
        except (ValueError, IndexError, OverflowError) as err:
            print(f"-> Error: {err}")
if __name__ == "__main__":
    interactive_demo()
