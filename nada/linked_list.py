class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    def __repr__(self):
        return f"Node({self.data})"
class LinkedList:
    MAX_CAPACITY = 25
    def __init__(self):
        self.head = None
    def is_empty(self) -> bool:
        return self.head is None
    def size(self) -> int:
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count
    def _validate_data(self, data):
        if data is None or not str(data).strip():
            raise ValueError("Node data cannot be empty or whitespace only.")
        clean_str = str(data).strip()
        if len(clean_str) > 50:
            raise ValueError("Node data exceeds maximum length of 50 characters.")
        return clean_str
    def insertatbeginning(self, data):
        clean_data = self._validate_data(data)
        if self.size() >= self.MAX_CAPACITY:
            raise OverflowError(f"List Overflow: Cannot insert. Maximum capacity of {self.MAX_CAPACITY} nodes reached.")
        new_node = Node(clean_data)
        new_node.next = self.head
        self.head = new_node
    def insertatend(self, data):
        clean_data = self._validate_data(data)
        if self.size() >= self.MAX_CAPACITY:
            raise OverflowError(f"List Overflow: Cannot insert. Maximum capacity of {self.MAX_CAPACITY} nodes reached.")
        new_node = Node(clean_data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
    def insertafter(self, target_data, data):
        if self.is_empty():
            raise IndexError("Cannot insert after: The linked list is currently empty.")
        if target_data is None or not str(target_data).strip():
            raise ValueError("Target node value cannot be empty.")
        clean_target = str(target_data).strip()
        clean_data = self._validate_data(data)
        if self.size() >= self.MAX_CAPACITY:
            raise OverflowError(f"List Overflow: Cannot insert. Maximum capacity of {self.MAX_CAPACITY} nodes reached.")
        current = self.head
        while current is not None:
            if str(current.data) == clean_target:
                new_node = Node(clean_data)
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next
        raise ValueError(f"Target node '{clean_target}' was not found in the linked list.")
    def removeatbeginning(self):
        if self.is_empty():
            raise IndexError("List Underflow: Cannot remove from an empty linked list.")
        removed_data = self.head.data
        self.head = self.head.next
        return removed_data
    def removeatend(self):
        if self.is_empty():
            raise IndexError("List Underflow: Cannot remove from an empty linked list.")
        if self.head.next is None:
            removed_data = self.head.data
            self.head = None
            return removed_data
        current = self.head
        while current.next.next is not None:
            current = current.next
        removed_data = current.next.data
        current.next = None
        return removed_data
    def removetarget(self, target_data):
        if self.is_empty():
            raise IndexError("Cannot remove target: The linked list is currently empty.")
        if target_data is None or not str(target_data).strip():
            raise ValueError("Target value to remove cannot be empty.")
        clean_target = str(target_data).strip()
        if str(self.head.data) == clean_target:
            removed_data = self.head.data
            self.head = self.head.next
            return removed_data
        current = self.head
        while current.next is not None:
            if str(current.next.data) == clean_target:
                removed_data = current.next.data
                current.next = current.next.next
                return removed_data
            current = current.next
        raise ValueError(f"Target node '{clean_target}' was not found in the linked list.")
    insert_at_beginning = insertatbeginning
    insert_at_end = insertatend
    insert_after = insertafter
    remove_at_beginning = removeatbeginning
    remove_at_end = removeatend
    remove_target = removetarget
    def to_list(self) -> list:
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
    @classmethod
    def from_list(cls, items: list):
        ll = cls()
        for item in items:
            ll.insertatend(item)
        return ll
    def __str__(self) -> str:
        if self.head is None:
            return "Head -> None (Empty List)"
        nodes = []
        current = self.head
        while current is not None:
            nodes.append(f"[{current.data}]")
            current = current.next
        return "Head -> " + " -> ".join(nodes) + " -> None"
def interactive_demo():
    ll = LinkedList()
    for val in ["Node 1", "Node 2", "Node 3"]:
        ll.insertatend(val)
    while True:
        print("\n" + "=" * 45)
        print("     LINKED LIST INTERACTIVE CLI DEMO")
        print("=" * 45)
        print(f"Current List: {ll}")
        print(f"Items count : {ll.size()} / {ll.MAX_CAPACITY}")
        print("-" * 45)
        print("1. insertatbeginning(data)")
        print("2. insertatend(data)")
        print("3. insertafter(target_data, data)")
        print("4. removeatbeginning()")
        print("5. removeatend()")
        print("6. removetarget(target_data)")
        print("7. Exit")
        print("-" * 45)
        choice = input("Select an option (1-7): ").strip()
        try:
            if choice == "1":
                data = input("Enter value to insert at beginning: ")
                ll.insertatbeginning(data)
                print(f"-> Successfully inserted '{data.strip()}' at beginning.")
            elif choice == "2":
                data = input("Enter value to insert at end: ")
                ll.insertatend(data)
                print(f"-> Successfully inserted '{data.strip()}' at end.")
            elif choice == "3":
                target = input("Enter target value to insert after: ")
                data = input("Enter new value to insert: ")
                ll.insertafter(target, data)
                print(f"-> Successfully inserted '{data.strip()}' after '{target.strip()}'.")
            elif choice == "4":
                removed = ll.removeatbeginning()
                print(f"-> Successfully removed '{removed}' from beginning.")
            elif choice == "5":
                removed = ll.removeatend()
                print(f"-> Successfully removed '{removed}' from end.")
            elif choice == "6":
                target = input("Enter target value to remove: ")
                removed = ll.removetarget(target)
                print(f"-> Successfully removed '{removed}' from list.")
            elif choice == "7":
                print("\nExiting Linked List Demo. Goodbye!\n")
                break
            else:
                print("-> Invalid option. Please select 1 through 7.")
        except (ValueError, IndexError, OverflowError) as err:
            print(f"-> Error: {err}")
if __name__ == "__main__":
    interactive_demo()
