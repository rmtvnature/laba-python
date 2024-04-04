# Импорт необходимых модулей
import matplotlib.pyplot as plt  # Импорт модуля для визуализации данных
from matplotlib.patches import Circle  # Импорт класса для создания круговых элементов
import time  # Импорт модуля для работы со временем

# Класс, представляющий узел дерева
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Функция для вставки нового узла в дерево
def insert(root, value):
    if root is None:  # Если дерево пустое
        return TreeNode(value)  # Создаем новый узел
    else:
        if root.left is None:  # Если левый потомок пуст
            root.left = insert(root.left, value)  # Вставляем новый узел в левое поддерево
        elif root.right is None:  # Если правый потомок пуст
            root.right = insert(root.right, value)  # Вставляем новый узел в правое поддерево
        else:
            # Если оба поддерева заполнены, вставляем новый узел в левое поддерево
            if root.left.left is None or root.left.right is None:
                root.left = insert(root.left, value)
            else:
                # Иначе вставляем новый узел в правое поддерево
                root.right = insert(root.right, value)
    return root

# Функция для печати дерева в виде текста
def print_tree(root, level=0, prefix="Root: "):
    if root is not None:
        print("   " * level + prefix + str(root.value))  # Выводим значение узла
        if root.left is not None or root.right is not None:
            print_tree(root.left, level + 1, "L: ")  # Рекурсивно вызываем функцию для левого потомка
            print_tree(root.right, level + 1, "R: ")  # Рекурсивно вызываем функцию для правого потомка

# Функция для визуализации дерева с помощью Matplotlib
def draw_tree(ax, node, x, y, spacing, level=1):
    if node is not None:
        # Рисуем круговой узел
        circle = Circle((x, y), 0.3, color='black', fill=False)
        ax.add_patch(circle)
        ax.text(x, y, str(node.value), ha='center', va='center', fontsize=12)  # Выводим значение узла
        # Рисуем связь с левым потомком, если он есть
        if node.left is not None:
            x_left = x - spacing / (2 ** level)
            y_left = y - 1
            ax.plot([x, x_left], [y, y_left], color='black')
            draw_tree(ax, node.left, x_left, y_left, spacing, level + 1)
        # Рисуем связь с правым потомком, если он есть
        if node.right is not None:
            x_right = x + spacing / (2 ** level)
            y_right = y - 1
            ax.plot([x, x_right], [y, y_right], color='black')
            draw_tree(ax, node.right, x_right, y_right, spacing, level + 1)

# Функция для проверки наличия одинаковой структуры у двух деревьев
def is_same_structure(tree1, tree2):
    if tree1 is None and tree2 is None:
        return True
    if tree1 is None or tree2 is None:
        return False
    return is_same_structure(tree1.left, tree2.left) and is_same_structure(tree1.right, tree2.right)

# Функция для поиска поддеревьев с такой же структурой, как у заданного поддерева
def find_subtrees_with_same_structure(root, subtree_root):
    if root is None:
        return []

    subtrees = []
    if is_same_structure(root, subtree_root):
        subtrees.append(root)

    subtrees.extend(find_subtrees_with_same_structure(root.left, subtree_root))
    subtrees.extend(find_subtrees_with_same_structure(root.right, subtree_root))

    return subtrees

# Точка входа в программу
if __name__ == "__main__":
    # Список файлов для обработки
    file_names = ["tree_data1.txt", "tree_data2.txt", "tree_data3.txt"]

    # Обработка каждого файла
    for i, file_name in enumerate(file_names):
        # Запуск таймера для измерения времени выполнения
        start_time = time.time()

        main_tree = None

        # Чтение данных о дереве из файла и построение главного дерева
        with open(file_name, "r") as file:
            lines = file.readlines()
            main_tree = TreeNode(int(lines[0].strip()))
            for value in lines[1:]:
                value = int(value.strip())
                main_tree = insert(main_tree, value)

        # Для первого файла выводим поддеревья и рисунок
        if i == 0:
            # Создание графического окна для визуализации дерева
            fig, ax = plt.subplots(figsize=(8, 6))
            draw_tree(ax, main_tree, 0, 0, 3)
            ax.set_aspect(1.0)
            ax.axis('off')
            plt.show()

            # Определение структуры поддерева, которую нужно найти
            subtree_root = TreeNode(2)
            subtree_root.left = TreeNode(4)
            subtree_root.right = TreeNode(5)

            # Поиск всех поддеревьев с такой же структурой
            found_subtrees = find_subtrees_with_same_structure(main_tree, subtree_root)

            # Вывод найденных поддеревьев
            print(f"Найденные поддеревья для файла {file_name} с такой же структорой:")
            for subtree in found_subtrees:
                print_tree(subtree)
                print()

        # Завершение таймера и вывод времени выполнения в миллисекундах
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000  # Преобразуем секунды в миллисекунды
        print(f"Время выполнения для файла {file_name}: {execution_time_ms:.2f} миллисекунд")
