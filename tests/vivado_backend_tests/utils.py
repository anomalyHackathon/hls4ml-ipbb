import os


def get_project_path(name):
    return os.path.join(os.path.dirname(__file__), 'projects', name)
