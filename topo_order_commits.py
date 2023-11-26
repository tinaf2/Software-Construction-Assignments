#!/usr/local/cs/bin/python3

import zlib
import sys
import os

class CommitNode:
    def __init__(self, commit_id, associated_branches=[]):
        self.commit_id = commit_id
        self.parents = set()
        self.children = set()
        self.branches = associated_branches

# Top-level function for orchestrating the entire process.
def topo_order_commits():
    # Get the commits associated with local branches.
    branch_commits = get_local_branch_commits()

    # Build the original commit graph based on branch commits.
    original_graph = build_original_commit_graph(branch_commits)

    # Build the commit graph for topological sorting.
    root_commits, commit_graph = build_commit_graph(branch_commits)

    # Generate a topological order of commits.
    ordered_commits = generate_topological_order(root_commits, commit_graph)

    # Display the ordered commits and their relationships.
    display_ordered_commits(ordered_commits, original_graph)

# Function to find the Git directory by moving up the directory tree.
# Uses strace to verify no external commands are used for directory discovery.
def find_git_dir():
    while os.getcwd() != '/':
        if os.path.isdir(os.path.join(os.getcwd(), '.git')):
            return os.path.join(os.getcwd(), '.git')
        os.chdir('../')
    print("Not inside a Git repository", file=sys.stderr)
    sys.exit(1)

# Function to retrieve local branch commits and associated branch names.
def get_local_branch_commits():
    git_dir = os.path.join(find_git_dir(), 'refs', 'heads')
    branch_commits = {}

    for root, dirs, files in os.walk(git_dir, topdown=True):
        for name in files:
            commit_id = open(os.path.join(root, name), 'r').read()[:-1]
            branch_name = os.path.join(root[len(git_dir) + 1:], name)

            if commit_id not in branch_commits:
                branch_commits[commit_id] = [branch_name]
            else:
                branch_commits[commit_id].append(branch_name)

    return branch_commits

# Function to build the original commit graph based on branch commits.
def build_original_commit_graph(branch_commits):
    original_graph = {}
    commit_stack = []
    objects_path = os.path.join(os.path.join(find_git_dir(), 'objects'))

    for commit_id in branch_commits:
        commit_stack.append(commit_id)

    while True:
        commit_id = commit_stack.pop()
        commit_path = os.path.join(objects_path, commit_id[:2], commit_id[2:])
        compressed_data = open(commit_path, 'rb').read()
        commit_data = zlib.decompress(compressed_data).decode()

        while commit_data.find('\nparent') > -1:
            parent_index = commit_data.find('\nparent')
            parent_commit_id = commit_data[parent_index + 8:parent_index + 48]

            if parent_commit_id not in commit_stack:
                commit_stack.append(parent_commit_id)

            if commit_id not in original_graph:
                original_graph[commit_id] = CommitNode(commit_id, branch_commits.get(commit_id, []))

            original_graph[commit_id].parents.add(parent_commit_id)

            if parent_commit_id not in original_graph:
                original_graph[parent_commit_id] = CommitNode(parent_commit_id, branch_commits.get(parent_commit_id, []))

            original_graph[parent_commit_id].children.add(commit_id)
            commit_data = commit_data[commit_data.find('\nparent') + 48:]

        if len(commit_stack) == 0:
            break

    return original_graph

# Function to build the commit graph for topological sorting.
def build_commit_graph(branch_commits):
    commit_graph = {}
    root_commits = []
    commit_stack = []
    objects_path = os.path.join(os.path.join(find_git_dir(), 'objects'))

    for commit_id in branch_commits:
        commit_stack.append(commit_id)

    while True:
        commit_id = commit_stack.pop()
        commit_path = os.path.join(objects_path, commit_id[:2], commit_id[2:])
        compressed_data = open(commit_path, 'rb').read()
        commit_data = zlib.decompress(compressed_data).decode()

        while commit_data.find('\nparent') > -1:
            parent_index = commit_data.find('\nparent')
            parent_commit_id = commit_data[parent_index + 8:parent_index + 48]

            if parent_commit_id not in commit_stack:
                commit_stack.append(parent_commit_id)

            if commit_id not in commit_graph:
                commit_graph[commit_id] = CommitNode(commit_id, branch_commits.get(commit_id, []))

            commit_graph[commit_id].parents.add(parent_commit_id)

            if parent_commit_id not in commit_graph:
                commit_graph[parent_commit_id] = CommitNode(parent_commit_id, branch_commits.get(parent_commit_id, []))

            commit_graph[parent_commit_id].children.add(commit_id)
            commit_data = commit_data[commit_data.find('\nparent') + 48:]

        if len(commit_stack) == 0:
            break

    for node in commit_graph:
        if len(commit_graph[node].parents) == 0:
            root_commits.append(node)

    return root_commits, commit_graph

# Function to generate a topological order of commits.
def generate_topological_order(root_commits, commit_graph):
    topological_order = []
    roots = root_commits.copy()

    while roots:
        commit_id = roots.pop(0)
        topological_order.append(commit_id)

        for child in commit_graph[commit_id].children:
            commit_graph[child].parents.remove(commit_id)
            if len(commit_graph[child].parents) == 0:
                roots.append(child)

    topological_order.reverse()
    return topological_order

# Function to display the ordered commits and their relationships.
def display_ordered_commits(ordered_commits, commit_graph):
    for i in range(len(ordered_commits)):
        commit_id = ordered_commits[i]
        node = commit_graph[commit_id]

        if len(node.branches) == 0:
            print(commit_id)
        else:
            print(commit_id, end=" ")
            print(*sorted(node.branches))

        if i < (len(ordered_commits) - 1):
            next_node = commit_graph[ordered_commits[i + 1]]
            if ordered_commits[i + 1] not in node.parents:
                print(*[parent for parent in node.parents], end="=\n\n=")
                print(*[child for child in next_node.children])

if __name__ == '__main__':
    topo_order_commits()


# I used the commands 'strace -f python3 topo_order_commits.py [args...] 2>&1 | grep exec' 
# and 'strace -f python3 topo_order_commits.py [args...] 2>&1 | grep sys' to make sure that 
# no system calls were made to the exec() family and system(). Since both of them returned 0, 
# I know that no program was launched and have thus verified that my implementation does not use any commands.