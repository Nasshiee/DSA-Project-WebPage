class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value})"

class BinaryTree:
    MAX_CAPACITY = 30

    def __init__(self, root_value=None):
        self.root = Node(str(root_value).strip()) if root_value is not None else None

    def set_root(self, value):
        if value is None or not str(value).strip():
            raise ValueError("Root value cannot be empty.")
        clean_val = str(value).strip()
        if len(clean_val) > 50:
            raise ValueError("Value exceeds maximum length of 50 characters.")
        self.root = Node(clean_val)
        return self.root

    def insert_left(self, current_node, value):
        if current_node is None:
            raise ValueError("Target parent node cannot be None.")
        if value is None or not str(value).strip():
            raise ValueError("Node value cannot be empty.")
        clean_val = str(value).strip()
        if len(clean_val) > 50:
            raise ValueError("Value exceeds maximum length of 50 characters.")
        if self.count_nodes() >= self.MAX_CAPACITY:
            raise OverflowError(f"Tree Overflow: Maximum capacity of {self.MAX_CAPACITY} nodes reached.")
        if current_node.left is None:
            current_node.left = Node(clean_val)
            return current_node.left
        else:
            new_node = Node(clean_val)
            new_node.left = current_node.left
            current_node.left = new_node
            return new_node

    def insert_right(self, current_node, value):
        if current_node is None:
            raise ValueError("Target parent node cannot be None.")
        if value is None or not str(value).strip():
            raise ValueError("Node value cannot be empty.")
        clean_val = str(value).strip()
        if len(clean_val) > 50:
            raise ValueError("Value exceeds maximum length of 50 characters.")
        if self.count_nodes() >= self.MAX_CAPACITY:
            raise OverflowError(f"Tree Overflow: Maximum capacity of {self.MAX_CAPACITY} nodes reached.")
        if current_node.right is None:
            current_node.right = Node(clean_val)
            return current_node.right
        else:
            new_node = Node(clean_val)
            new_node.right = current_node.right
            current_node.right = new_node
            return new_node

    def preorder_traversal(self, start, traversal=""):
        if start:
            traversal += (str(start.value) + " ")
            traversal = self.preorder_traversal(start.left, traversal)
            traversal = self.preorder_traversal(start.right, traversal)
        return traversal

    def inorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.inorder_traversal(start.left, traversal)
            traversal += (str(start.value) + " ")
            traversal = self.inorder_traversal(start.right, traversal)
        return traversal

    def postorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.postorder_traversal(start.left, traversal)
            traversal = self.postorder_traversal(start.right, traversal)
            traversal += (str(start.value) + " ")
        return traversal

    def find(self, start, value):
        if start is None:
            return None
        if str(start.value) == str(value).strip():
            return start
        left_found = self.find(start.left, value)
        if left_found is not None:
            return left_found
        return self.find(start.right, value)

    def get_nodes(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return []
        nodes = [str(start.value)]
        if start.left:
            nodes.extend(self.get_nodes(start.left, False))
        if start.right:
            nodes.extend(self.get_nodes(start.right, False))
        return nodes

    def to_dict(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return None
        return {
            'value': str(start.value),
            'left': self.to_dict(start.left, False) if start.left else None,
            'right': self.to_dict(start.right, False) if start.right else None
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return cls()
        def build_node(d):
            if not d:
                return None
            node = Node(str(d.get('value', '')))
            node.left = build_node(d.get('left'))
            node.right = build_node(d.get('right'))
            return node
        tree = cls()
        tree.root = build_node(data)
        return tree

    def count_nodes(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return 0
        return 1 + self.count_nodes(start.left, False) + self.count_nodes(start.right, False)

    def height(self, start=None, is_root=True):
        if is_root and start is None:
            start = self.root
        if start is None:
            return 0
        return 1 + max(self.height(start.left, False), self.height(start.right, False))

    def clear(self):
        if self.root is None:
            raise ValueError("Tree is already empty.")
        self.root = None

    def load_default(self):
        self.root = Node("R")
        self.insert_left(self.root, "A")
        self.insert_right(self.root, "B")
        self.insert_left(self.root.left, "C")
        self.insert_right(self.root.left, "D")
        self.insert_left(self.root.right, "E")
        self.insert_right(self.root.right, "F")
        self.insert_left(self.root.right.right, "G")

def interactive_demo():
    tree = BinaryTree("R")
    tree.insert_left(tree.root, "A")
    tree.insert_right(tree.root, "B")
    tree.insert_left(tree.root.left, "C")
    tree.insert_right(tree.root.left, "D")
    tree.insert_left(tree.root.right, "E")
    tree.insert_right(tree.root.right, "F")
    tree.insert_left(tree.root.right.right, "G")

    while True:
        print("\n" + "=" * 55)
        print("          BINARY TREE INTERACTIVE DEMO")
        print("=" * 55)
        print("Total Nodes :", tree.count_nodes())
        print("Tree Height :", tree.height())
        print("Preorder    :", tree.preorder_traversal(tree.root, "").strip())
        print("Inorder     :", tree.inorder_traversal(tree.root, "").strip())
        print("Postorder   :", tree.postorder_traversal(tree.root, "").strip())
        print("-" * 55)
        print("1. Set Root Node")
        print("2. Insert Left Child")
        print("3. Insert Right Child")
        print("4. Find Node")
        print("5. Reset Default Tree")
        print("6. Clear Tree")
        print("7. Exit")
        print("-" * 55)

        choice = input("Select an option (1-7): ").strip()

        try:
            if choice == "1":
                val = input("Enter root value: ")
                tree.set_root(val)
                print(f"-> Successfully set root node to '{tree.root.value}'.")
            elif choice == "2":
                if tree.root is None:
                    print("-> Error: Tree has no root. Please set root first.")
                    continue
                parent_val = input("Enter parent node value: ").strip()
                parent_node = tree.find(tree.root, parent_val)
                if not parent_node:
                    print(f"-> Error: Parent node '{parent_val}' not found.")
                    continue
                child_val = input("Enter new left child value: ")
                tree.insert_left(parent_node, child_val)
                print(f"-> Successfully inserted '{child_val.strip()}' as left child of '{parent_val}'.")
            elif choice == "3":
                if tree.root is None:
                    print("-> Error: Tree has no root. Please set root first.")
                    continue
                parent_val = input("Enter parent node value: ").strip()
                parent_node = tree.find(tree.root, parent_val)
                if not parent_node:
                    print(f"-> Error: Parent node '{parent_val}' not found.")
                    continue
                child_val = input("Enter new right child value: ")
                tree.insert_right(parent_node, child_val)
                print(f"-> Successfully inserted '{child_val.strip()}' as right child of '{parent_val}'.")
            elif choice == "4":
                search_val = input("Enter value to search: ").strip()
                found = tree.find(tree.root, search_val)
                if found:
                    print(f"-> Node '{search_val}' FOUND in tree! (Left: {found.left}, Right: {found.right})")
                else:
                    print(f"-> Node '{search_val}' NOT found in tree.")
            elif choice == "5":
                tree.load_default()
                print("-> Default sample tree reloaded.")
            elif choice == "6":
                tree.clear()
                print("-> Tree cleared.")
            elif choice == "7":
                print("\nExiting Binary Tree Demo. Goodbye!\n")
                break
            else:
                print("-> Invalid option. Please select 1 through 7.")
        except (ValueError, IndexError, OverflowError) as err:
            print(f"-> Error: {err}")

if __name__ == "__main__":
    tree = BinaryTree("R")
    tree.insert_left(tree.root, "A")
    tree.insert_right(tree.root, "B")
    tree.insert_left(tree.root.left, "C")
    tree.insert_right(tree.root.left, "D")
    tree.insert_left(tree.root.right, "E")
    tree.insert_right(tree.root.right, "F")
    tree.insert_left(tree.root.right.right, "G")
    print("Preorder traversal: " + tree.preorder_traversal(tree.root, ""))
    print("Inorder traversal: " + tree.inorder_traversal(tree.root, ""))
    print("Postorder traversal: " + tree.postorder_traversal(tree.root, ""))
