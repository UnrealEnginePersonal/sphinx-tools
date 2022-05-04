import os


def is_rtd_build():
    return os.environ.get("READTHEDOCS") is not None


def is_github_build():
    return os.environ.get("GITHUB_ACTIONS") is not None


def is_ci_build():
    return is_rtd_build() or is_github_build()
