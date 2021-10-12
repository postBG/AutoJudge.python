import os


def find_src_root(search_root):
    for root, dirs, files in os.walk(search_root):
        if root.endswith('src'):
            return root


def to_src_roots(extracted_paths):
    return [find_src_root(r) for r in extracted_paths]


def to_project_roots(extracted_paths):
    src_roots = to_src_roots(extracted_paths)
    return [os.path.dirname(src_root) for src_root in src_roots]
