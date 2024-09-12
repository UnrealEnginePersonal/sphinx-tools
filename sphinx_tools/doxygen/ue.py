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

        name = frags[-2]
        module = os.path.abspath(os.path.join(path, '..'))
        print('module')
        print(module)
        cat = extract_category(frags, 'Source', name)
        if not cat:
            cat = [name]


        print('cat' + str(cat))

        yield Module(name, cat, module, [
            os.path.join(module, 'Public'),
            os.path.join(module, 'Private'),
            #os.path.join(module, 'Classes'),
        ])


def find_engine_plugins(project_root):
    src = os.path.join(project_root, 'Plugins')

    for path in glob.iglob(f'{src}/**/Source', recursive=True):
        frags = path.replace('\\', '/').split('/')

        name = frags[-2]
        print('name')
        print(name)

        cat = extract_category(frags, 'Plugins', name)
        print('cat')
        if not cat:
            cat = [name]

        print(cat)
        yield Module(name, cat, path, [path])


def test_modules():
    namespaces = set()

    for i in find_engine_source_modules('E:/_00_blackdog/Docs/TestDocProject'):
        namespaces.add('/'.join(i.cat))
        print(i)
        i.generate_documentation()

    for n in sorted(list(namespaces)):
        print(n)


def test_plugins():
    namespaces = set()

    for i in find_engine_plugins('E:/_00_blackdog/Docs/TestDocProject'):
        namespaces.add('/'.join(i.cat))
        print('XX' * 60)
        print(i.name)
        print('XX' * 60)
        i.generate_documentation(gen_doxygen=True)

    for n in sorted(list(namespaces)):
        print(n)


def mock_module():
    # Module(
    #     name='ALS', cat=[],
    #     path='E:/_00_blackdog/Docs/TestDocProject\\Plugins\\ALS\\Source',
    #     sources=['E:/_00_blackdog/Docs/TestDocProject\\Plugins\\ALS\\Source'], files=[]
    # )
    module: Module = Module(
        name='ALS', cat=[],
        path='E:/_00_blackdog/Docs/TestDocProject/Plugins/ALS/Source',
        sources=['E:/_00_blackdog/Docs/TestDocProject/Plugins/ALS/Source']
    )

    module.generate_documentation()

if __name__ == '__main__':
    test_plugins()
