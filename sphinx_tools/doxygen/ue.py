import os
import glob


from sphinx_tools.doxygen.module import Module


def extract_category(frags, start_tag, end_tag):
    cat = []
    cat_started = False

    for frag in frags:

        if frag == start_tag:
            cat_started = True
            continue

        if frag == end_tag:
            break

        if cat_started:
            cat.append(frag)

    return cat


def find_engine_source_modules(project_root):
    src = os.path.join(project_root, 'Source')

    for path in glob.iglob(f'{src}/**/Public', recursive=True):
        frags = path.replace('\\', '/').split('/')

        if 'ThirdParty' in path or 'Datasmith' in path:
            continue

        name = frags[-2]
        module = os.path.abspath(os.path.join(path, '..'))

        cat = extract_category(frags, 'Source', name)

        yield Module(name, cat, module, [
            os.path.join(module, 'Public'),
            os.path.join(module, 'Private'),
            os.path.join(module, 'Classes'),
        ])


def find_engine_plugins(project_root):
    src = os.path.join(project_root, 'Plugins')

    for path in glob.iglob(f'{src}/**/Source', recursive=True):

        if 'ThirdParty' in path or 'Datasmith' in path:
            continue

        frags = path.replace('\\', '/').split('/')

        name = frags[-2]
        cat = extract_category(frags, 'Plugins', name)

        yield Module(name, cat, path, [path])


def test_modules():
    namespaces = set()

    for i in find_engine_source_modules('/mnt/e/UnrealEngine/Engine'):
        namespaces.add('/'.join(i.cat))

    for n in sorted(list(namespaces)):
        print(n)


def test_plugins():
    namespaces = set()

    for i in find_engine_plugins('/mnt/e/UnrealEngine/Engine'):
        namespaces.add('/'.join(i.cat))

    for n in sorted(list(namespaces)):
        print(n)


if __name__ == '__main__':
    test_plugins()
