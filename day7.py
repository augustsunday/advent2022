# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/7/2022

class Directory:
    def __init__(self, dirname):
        self.size = 0
        self.children = dict()
        self.name = dirname

    def add_file(self, file_size: int):
        self.size += file_size

    def add_dir(self, dirname: str):
        if dirname not in self.children:
            self.children[dirname] = Directory(dirname)


def build_filesystem(filename: str) -> Directory:
    path = [Directory("/")]
    with open(filename, "r") as fo:
        for line in fo.read().split("\n")[1:]:
            if ".." in line:
                path.pop()

            elif line[:4] == "dir ":
                directory_name = line[4:]
                path[-1].add_dir(directory_name)

            elif line[:4] == "$ cd":
                directory_name = line[5:]
                path.append(path[-1].children[directory_name])

            elif line[0].isdigit():
                file_size = int("".join(s for s in line if s.isdigit()))
                path[-1].add_file(file_size)

        return path[0]


def find_oversize_directories(root: Directory, oversize_dirs):
    dir_size = root.size
    for dir in root.children.values():
        dir_size += find_oversize_directories(dir, oversize_dirs)
    if dir_size <= 100000:
        oversize_dirs.append(dir_size)
    return dir_size

def get_all_directory_sizes(root: Directory, all_dirs):
    dir_size = root.size
    for dir in root.children.values():
        dir_size += get_all_directory_sizes(dir, all_dirs)
    all_dirs.append((dir_size, root.name))

    return dir_size

def solution1(filename):
    root = build_filesystem(filename)
    oversized = []
    find_oversize_directories(root, oversized)
    return sum(oversized)

def solution2(filename):
    root = build_filesystem(filename)
    all_sizes = []
    get_all_directory_sizes(root, all_sizes)
    current_free_space = 70000000 - all_sizes[-1][0]
    print("Free Space: ", current_free_space)
    need_to_delete = 30000000 - current_free_space
    print("Need to Delete: ", need_to_delete)

    all_sizes.sort()
    for size, directory in all_sizes:
        if size >= need_to_delete:
            return size

print("Solution 1: ", solution1("input.txt"))
print()
print("Solution 2: ", solution2("input.txt"))
