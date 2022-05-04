import subprocess


def get_version():
    """Report the git tags & commit hash"""
    try:
        version_tag = subprocess.check_output(
            'git describe --tags --abbrev=0', shell=True
        ).decode('utf-8').strip()
    except:
        version_tag = ''

    commit = subprocess.check_output(
        'git rev-parse --short HEAD', shell=True
    ).decode('utf-8').strip()

    if version_tag == '':
        version_identifier = commit
    else:
        version_identifier = f'{version_tag}-{commit}'

    return version_identifier
