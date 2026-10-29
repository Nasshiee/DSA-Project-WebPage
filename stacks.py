class Stack:
    DEFAULT_CAPACITY = 15
    def __init__(self, max_capacity: int = DEFAULT_CAPACITY):
        self._items = []
        self.max_capacity = max_capacity
    def is_empty(self) -> bool:
        return len(self._items) == 0
    def is_full(self) -> bool:
        return len(self._items) >= self.max_capacity
    def push(self, item):
        if item is None or not str(item).strip():
            raise ValueError("Cannot push empty element. Please enter a valid value.")
        clean_item = str(item).strip()
        if len(clean_item) > 50:
            raise ValueError("Item exceeds maximum length of 50 characters.")
        if self.is_full():
            raise OverflowError(
                f"Stack Overflow: Cannot push onto full stack (maximum limit of {self.max_capacity} items reached)."
            )
        self._items.append(clean_item)
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack Underflow: Cannot pop from an empty stack.")
        return self._items.pop()
    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek: The stack is currently empty.")
        return self._items[-1]
    def clear(self):
        if self.is_empty():
            raise ValueError("Stack is already empty.")
        self._items.clear()
    def size(self) -> int:
        return len(self._items)
    def to_list(self) -> list:
        return list(self._items)
    @classmethod
    def from_list(cls, items: list, max_capacity: int = DEFAULT_CAPACITY):
        stack = cls(max_capacity=max_capacity)
        for item in items:
            stack.push(item)
        return stack
    def __str__(self) -> str:
        if self.is_empty():
            return "[ Empty Stack ]"
        lines = []
        for i in reversed(range(len(self._items))):
            marker = " <- TOP" if i == len(self._items) - 1 else ""
            lines.append(f"| {str(self._items[i]):^16} |{marker}")
        lines.append("+------------------+")
        return "\n".join(lines)
def interactive_demo():
    stack = Stack()
    for item in ["Plate 1", "Plate 2", "Plate 3"]:
        stack.push(item)
    while True:
        print("\n" + "=" * 45)
        print("         STACK INTERACTIVE CLI DEMO")
        print("=" * 45)
        print("Visual Stack:")
        print(stack)
        print(f"\nItems count: {stack.size()} / {stack.max_capacity}")
        print("-" * 45)
        print("1. push(item)")
        print("2. pop()")
        print("3. peek()")
        print("4. clear()")
        print("5. Exit")
        print("-" * 45)
        choice = input("Select an option (1-5): ").strip()
        try:
            if choice == "1":
                data = input("Enter item to push: ")
                stack.push(data)
                print(f"-> Pushed '{data.strip()}' onto the top of the stack.")
            elif choice == "2":
                popped = stack.pop()
                print(f"-> Popped '{popped}' from the top of the stack.")
            elif choice == "3":
                top_item = stack.peek()
                print(f"-> Peek: Top item is '{top_item}'.")
            elif choice == "4":
                stack.clear()
                print("-> Stack has been cleared.")
            elif choice == "5":
                print("\nExiting Stack Demo. Goodbye!\n")
                break
            else:
                print("-> Invalid option. Please select 1 through 5.")
        except (ValueError, IndexError, OverflowError) as err:
            print(f"-> Error: {err}")
if __name__ == "__main__":
    interactive_demo()
