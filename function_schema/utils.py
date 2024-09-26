import platform


def is_py310_atleast():
    version_tuple = tuple(map(int, platform.python_version_tuple()))
    return version_tuple >= (3, 10)
