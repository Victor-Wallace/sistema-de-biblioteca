import time
from collections import deque
from queue import PriorityQueue

class Book:
    def __init__(self, book_id, title, author, category, year=None, popularity=0):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.year = year
        self.popularity = popularity


class AVLNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None
        self.height = 1
        self.author_books = [book]
        self.category_books = [book]


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, book):
        if not root:
            return AVLNode(book)
        
        if book.title < root.book.title:
            root.left = self.insert(root.left, book)
        elif book.title > root.book.title:
            root.right = self.insert(root.right, book)
        else:
            if book.author not in [b.author for b in root.author_books]:
                root.author_books.append(book)
            if book.category not in [b.category for b in root.category_books]:
                root.category_books.append(book)
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and book.title < root.left.book.title:
            return self.right_rotate(root)

        if balance < -1 and book.title > root.right.book.title:
            return self.left_rotate(root)

        if balance > 1 and book.title > root.left.book.title:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and book.title < root.right.book.title:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, node):
        return 0 if not node else node.height

    def get_balance(self, node):
        return 0 if not node else self.get_height(node.left) - self.get_height(node.right)

class AVLTreeLibrary(AVLTree):
    
    def sequential_search(self, root, title=None, author=None, category=None):
        results = []
        if root:
            if (title and root.book.title == title) or \
               (author and root.book.author == author) or \
               (category and root.book.category == category):
                results.append(root.book)
            results += self.sequential_search(root.left, title, author, category)
            results += self.sequential_search(root.right, title, author, category)
        return results
    
    def binary_search(self, title, author=None, category=None):
        node = self._binary_search_by_title(self.root, title)
        if node:
            return [
                book for book in (node.author_books if author else node.category_books)
                if (author and book.author == author) or (category and book.category == category)
            ]
        return []

    def _binary_search_by_title(self, node, title):
        if node is None or node.book.title == title:
            return node
        elif title < node.book.title:
            return self._binary_search_by_title(node.left, title)
        else:
            return self._binary_search_by_title(node.right, title)

    def combined_search(self, title=None, author=None, category=None):
        results = self.binary_search(title) if title else self.sequential_search(self.root, author=author, category=category)
        return [
            book for book in results if
            (not author or book.author == author) and (not category or book.category == category)
        ]
    
    def measure_search_time(self, search_fn, *args):
        start_time = time.time()
        results = search_fn(*args)
        end_time = time.time()
        return results, end_time - start_time
    
    def search_by_id(self, root, book_id):
        """
        Busca um livro pelo ID na árvore AVL.
        """
        if root is None:
            return None
        if root.book.book_id == book_id:
            return root
        elif book_id < root.book.book_id:
            return self.search_by_id(root.left, book_id)
        else:
            return self.search_by_id(root.right, book_id)

class LibrarySorter:
    @staticmethod
    def quick_sort(books, key=lambda x: x.title):
        if len(books) <= 1:
            return books
        pivot = books[len(books) // 2]
        left = [book for book in books if key(book) < key(pivot)]
        middle = [book for book in books if key(book) == key(pivot)]
        right = [book for book in books if key(book) > key(pivot)]
        return LibrarySorter.quick_sort(left, key) + middle + LibrarySorter.quick_sort(right, key)

    @staticmethod
    def merge_sort(books, key=lambda x: x.title):
        if len(books) <= 1:
            return books
        mid = len(books) // 2
        left = LibrarySorter.merge_sort(books[:mid], key)
        right = LibrarySorter.merge_sort(books[mid:], key)
        return LibrarySorter._merge(left, right, key)

    @staticmethod
    def _merge(left, right, key):
        result = []
        while left and right:
            if key(left[0]) <= key(right[0]):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left or right)
        return result

    @staticmethod
    def bubble_sort(books, key=lambda x: x.title):
        n = len(books)
        for i in range(n):
            for j in range(0, n - i - 1):
                if key(books[j]) > key(books[j + 1]):
                    books[j], books[j + 1] = books[j + 1], books[j]
        return books

    @staticmethod
    def auto_sort(books, criterion):
        key_func = {
            "year": lambda x: x.year,
            "popularity": lambda x: x.popularity,
            "title": lambda x: x.title
        }[criterion]
        if len(books) > 5000:
            return LibrarySorter.quick_sort(books, key=key_func)
        elif len(books) > 500:
            return LibrarySorter.merge_sort(books, key=key_func)
        else:
            return LibrarySorter.bubble_sort(books, key=key_func)

class Loan:
    def __init__(self, book, user, due_date):
        self.book = book
        self.user = user
        self.due_date = due_date


class User:
    
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.loan_history = []
        self.on_time_returns = 0

    def add_loan(self, loan):
        self.loan_history.append(loan)

    def undo_loan(self):
        if self.loan_history:
            return self.loan_history.pop()
        return None
    
    def __lt__(self, other):
        # Define que um usuário com mais devoluções pontuais tem prioridade
        return self.on_time_returns > other.on_time_returns


class LibraryLoanSystem:
    def __init__(self):
        self.available_books = AVLTreeLibrary()
        self.loan_queue = PriorityQueue()
        self.active_loans = {}

    def add_book(self, book):
        self.available_books.root = self.available_books.insert(self.available_books.root, book)

    def request_loan(self, user, book_id, due_date):
        super().request_loan(user, book_id, due_date)
       # Registrar a operação no relatório
        book_node = self.available_books.search_by_id(self.available_books.root, book_id)
        if book_node and book_id in self.active_loans:
            self.report.log_operation("loan", user, book_node.book)



    def return_book(self, user, book_id):
        super().return_book(user, book_id)
        # Registrar a operação no relatório
        book_node = self.available_books.search_by_id(self.available_books.root, book_id)
        if book_node:
            self.report.log_operation("return", user, book_node.book)

    def undo_last_loan(self, user):
        loan = user.undo_loan()
        if loan:
            self.active_loans.pop(loan.book.book_id, None)
            print(f"Empréstimo desfeito: {user.name} devolveu '{loan.book.title}'")
        else:
            print(f"{user.name} não possui empréstimos para desfazer.")


class OperationRecord:
    def __init__(self, operation_type, user, book, timestamp):
        self.operation_type = operation_type
        self.user = user
        self.book = book
        self.timestamp = timestamp

class PerformanceReport:
    def __init__(self):
        self.operation_log = deque()
        self.pending_returns = {}
        self.operation_count = {"loan": 0, "return": 0}

    def log_operation(self, operation_type, user, book):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        record = OperationRecord(operation_type, user, book, timestamp)
        self.operation_log.append(record)
        self.operation_count[operation_type] += 1

        if operation_type == "loan":
            self.pending_returns[book.book_id] = record
        elif operation_type == "return" and book.book_id in self.pending_returns:
            self.pending_returns.pop(book.book_id)

    def generate_weekly_report(self):
        loan_operations = return_operations = 0
        overdue_loans = []

        for record in self.operation_log:
            if record.operation_type == "loan":
                loan_operations += 1
            elif record.operation_type == "return":
                return_operations += 1

        for book_id, record in self.pending_returns.items():
            overdue_loans.append((record.book.title, record.user.name, record.timestamp))

        print("Relatório Semanal de Desempenho")
        print("Total de Empréstimos:", loan_operations)
        print("Total de Devoluções:", return_operations)
        print("Devoluções Pendentes:", len(overdue_loans))
        if overdue_loans:
            print("\\nEmpréstimos em atraso:")
            for title, user, timestamp in overdue_loans:
                print(f"- Livro: {title}, Usuário: {user}, Data de Empréstimo: {timestamp}")
        
        self.analyze_efficiency()

    def analyze_efficiency(self):
        print("\\nAnálise de Eficiência:")
        print(f"- Operações de Empréstimo (Loan): {self.operation_count['loan']}")
        print(f"- Operações de Devolução (Return): {self.operation_count['return']}")

        if self.operation_count['loan'] > 1000:
            print("- Sugestão: Avaliar uso de cache para dados de livros e otimizar busca de usuários.")
        if self.operation_count['return'] > 1000:
            print("- Sugestão: Melhorar o controle de devoluções para otimizar o tempo de execução das operações.")


class LibrarySystemWithReports(LibraryLoanSystem):
    def __init__(self):
        super().__init__()
        self.report = PerformanceReport()
        self.users = {}

    def add_user(self, user):
        self.users[user.user_id] = user

    def request_loan(self, user, book_id, due_date):
        # Busca o livro pelo ID usando a função search_by_id
        book_node = self.available_books.search_by_id(self.available_books.root, book_id)
        
        if book_node:
            book = book_node.book
            if book_id not in self.active_loans:
                loan = Loan(book, user, due_date)
                self.active_loans[book_id] = loan
                user.add_loan(loan)
                print(f"{user.name} emprestou o livro '{book.title}' até {due_date}.")
                # Registrar empréstimo no relatório
                self.report.log_operation("loan", user, book)
            else:
                self.loan_queue.put((-user.on_time_returns, user.user_id, book_id, due_date))
                print(f"O livro '{book.title}' já está emprestado. {user.name} entrou na fila de espera.")
        else:
            print(f"Livro com ID {book_id} não encontrado no acervo.")

    def return_book(self, user, book_id):
        loan = self.active_loans.pop(book_id, None)
        if loan:
            if loan.due_date >= time.strftime("%Y-%m-%d"):
                user.on_time_returns += 1
            print(f"{user.name} devolveu o livro '{loan.book.title}'.")
            # Registrar devolução no relatório
            self.report.log_operation("return", user, loan.book)
            
            # Processa o próximo usuário na fila de prioridade
            if not self.loan_queue.empty():
                priority, user_id, book_id, due_date = self.loan_queue.get()
                next_user = self.get_user_by_id(user_id)
                if next_user:
                    self.request_loan(next_user, book_id, due_date)
        else:
            print(f"Livro com ID {book_id} não está emprestado.")

    def get_user_by_id(self, user_id):
        return self.users.get(user_id, None)









# Exemplo de uso do sistema da biblioteca
if __name__ == "__main__":
    # Criando instâncias do sistema com relatórios
    library_system = LibrarySystemWithReports()

    # Adicionando alguns livros ao acervo
    books = [
        Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, 300),
        Book(2, "To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, 450),
        Book(3, "1984", "George Orwell", "Dystopian", 1949, 520),
        Book(4, "Moby Dick", "Herman Melville", "Adventure", 1851, 200)
    ]
    for book in books:
        library_system.add_book(book)

    # Criando e adicionando usuários
    user1 = User(1, "Alice")
    user2 = User(2, "Bob")
    library_system.add_user(user1)
    library_system.add_user(user2)

    # Teste de empréstimo
    print("\n--- Teste de Empréstimo ---")
    library_system.request_loan(user1, 1, "2024-11-01")  # Alice empresta "The Great Gatsby"
    library_system.request_loan(user2, 1, "2024-11-05")  # Bob tenta emprestar "The Great Gatsby" (entra na fila)

    # Teste de devolução e fila de espera
    print("\n--- Teste de Devolução ---")
    library_system.return_book(user1, 1)  # Alice devolve o livro, e Bob deve pegá-lo em seguida

    # Teste de busca combinada
    print("\n--- Teste de Busca Combinada ---")
    results = library_system.available_books.combined_search(title="1984", author="George Orwell", category="Dystopian")
    print("Resultados da Busca Combinada:", [book.title for book in results])

    # Teste de ordenação
    print("\n--- Teste de Ordenação Automática ---")
    sorted_books = LibrarySorter.auto_sort(books, "popularity")
    print("Livros ordenados por popularidade:", [book.title for book in sorted_books])

    # Geração de relatório semanal
    print("\n--- Relatório Semanal de Desempenho ---")
    library_system.report.generate_weekly_report()
