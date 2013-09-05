'''
Created on Sep 3, 2013

@author: Fabio
'''
import os
import shutil

help_location = r'X:\liclipse\plugins\com.brainwy.liclipse.help'

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)


def apply_to(filename, target=None):
    with open(filename, 'r') as stream:
        contents = stream.read()
        body = extract(contents, 'body')

        contents = template_contents % {'body': body}

        with open(target or os.path.join(page_dir, os.path.basename(filename)), 'w') as out_stream:
            out_stream.write(contents)


def extract(contents, tag):
    i = contents.index('<%s>' % tag)
    j = contents.rindex('</%s>' % tag)
    return contents[i + len(tag) + 2:j]

if __name__ == '__main__':
    template_contents = open(os.path.join(os.path.dirname(__file__), 'template.html'), 'r').read()

    this_file_dir = os.path.dirname(__file__)
    page_dir = os.path.dirname(this_file_dir)

    base = help_location
    for f in os.listdir(base):
        if not f.endswith('.html'):
            continue

        filename = os.path.join(base, f)
        apply_to(filename)

    apply_to(os.path.join(this_file_dir, 'index.html'))
    apply_to(os.path.join(this_file_dir, 'multi_edition_video.html'))
    copytree(os.path.join(base, 'images'), os.path.join(page_dir, 'images'))
