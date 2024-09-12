import os


def is_rtd_build() -> bool:
    return True #TODO REENABLE WHEN STARTING TO USE IN REAL PROJECTS
    #return os.environ.get("READTHEDOCS") is not None


def is_github_build() -> bool:
    return os.environ.get("GITHUB_ACTIONS") is not None


def is_ci_build() -> bool:
    return is_rtd_build() or is_github_build()
