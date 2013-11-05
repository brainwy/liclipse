'''
Created on Sep 3, 2013

@author: Fabio
'''
import os
import shutil
import pyodict

help_location = r'X:\liclipse\plugins\com.brainwy.liclipse.help'

#===================================================================================================
# copytree
#===================================================================================================
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


template_contents = open(os.path.join(os.path.dirname(__file__), 'template.html'), 'r').read()
this_file_dir = os.path.dirname(__file__)
page_dir = os.path.dirname(this_file_dir)


HEADER = '''
<h1>LiClipse (Beta)</h1>
<p>Lightweight editors, theming and usability improvements for Eclipse</p>
<!-- <p class="view"><a href="https://github.com/brainwy/liclipse.page">
    View the Project on GitHub <small>brainwy/liclipse.page</small></a></p> -->
<ul class="top1">
    <!-- <li><a href="http://???">Get It <strong>Download</strong></a></li> -->
    <li><a href="https://groups.google.com/forum/#!forum/liclipse">Googlegroups <strong>Forum</strong></a></li>
    <li><a href="http://liclipse.blogspot.com.br/">View <strong>Blog</strong></a></li>
    <li><a href="https://sw-brainwy.rhcloud.com/tracker/LiClipse/">LiClipse<strong>Tracker</strong></a></li>
</ul>
<ul class="top2">
    <li class="lifull"><a href="download.html">Get it<strong>Download</strong></a></li>
</ul>

<ul class="top3">
    <li class="lifull">
    <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=NJW4VEJQZ36GJ">Help to make better<strong>Buy Single User</strong></a>
    </li>
</ul>

<ul class="top4">
    <li class="lifull">
    <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=G5APKLQNXK7DL">For Organizations<strong>Buy Multi User</strong></a>
    </li>
</ul>

Pricing: A LiClipse license is US$ 50.00 (only during Beta).<br><br><br>
<p><small>Copyright 2013 - Brainwy Software Ltda.<br/>Hosted on GitHub Pages - Theme by <a href="https://github.com/orderedlist">orderedlist</a></small></p>
'''

#===================================================================================================
# apply_to
#===================================================================================================
def apply_to(filename, header=None):
    with open(filename, 'r') as stream:
        contents = stream.read()
        body = extract(contents, 'body')
        apply_to_contents(contents, os.path.basename(filename), body, header or HEADER)


#===================================================================================================
# apply_to_contents
#===================================================================================================
def apply_to_contents(contents, basename, body, header):

    contents = template_contents % {'body': body, 'header': header}

    with open(os.path.join(page_dir, basename), 'w') as out_stream:
        out_stream.write(contents)


#===================================================================================================
# extract
#===================================================================================================
def extract(contents, tag):
    i = contents.index('<%s>' % tag)
    j = contents.rindex('</%s>' % tag)
    return contents[i + len(tag) + 2:j]


class Info:
    def __init__(self, title):
        self.title = title
        self.filename = None


FILE_TO_INFO = pyodict.odict([
    ('change_color_theme.html', Info('Changing colors')),
    ('supported_languages.html', Info('Language Support')),
    ('scope_definition.html', Info('&nbsp;&nbsp;&nbsp;&nbsp;Language Scopes')),
    ('ctags.html', Info('&nbsp;&nbsp;&nbsp;&nbsp;Ctags')),
    ('indent.html', Info('&nbsp;&nbsp;&nbsp;&nbsp;Specifying indentation')),
    ('templates.html', Info('&nbsp;&nbsp;&nbsp;&nbsp;Templates')),
    ('spell_checking.html', Info('&nbsp;&nbsp;&nbsp;&nbsp;Spell Checking')),
])


for f in os.listdir(help_location):
    if not f.endswith('.html'):
        continue
    if f not in FILE_TO_INFO:
        raise ValueError('Not expecting: %s' % (f,))
    FILE_TO_INFO[f].filename = os.path.join(help_location, f)


#===================================================================================================
# create_manual_header
#===================================================================================================
def create_manual_header():
    lis = []
    for file_basename, file_info in FILE_TO_INFO.iteritems():
        lis.append('<p><a href="%s">%s</a></p>' % (
            os.path.basename(file_info.filename),
            file_info.title
        ))

    return '''
%(li)s<br><br><br>
<p><small>Copyright 2013 - Brainwy Software Ltda.<br/>Hosted on GitHub Pages - Theme by <a href="https://github.com/orderedlist">orderedlist</a></small></p>
''' % {'li': '\n'.join(lis)}

MANUAL_HEADER = create_manual_header()



#===================================================================================================
# create_manual_page
#===================================================================================================
def create_manual_page():


    manual_body = '''
<h3>Choose the topic you're interested in...</h3>
'''
    apply_to_contents(manual_body, 'manual.html', manual_body, MANUAL_HEADER)



#===================================================================================================
# main
#===================================================================================================
def main():
    # Manual
    create_manual_page()
    for info in FILE_TO_INFO.itervalues():
        apply_to(info.filename, header=MANUAL_HEADER)

    # Others
    apply_to(os.path.join(this_file_dir, 'index.html'))
    apply_to(os.path.join(this_file_dir, 'download.html'))
    apply_to(os.path.join(this_file_dir, 'license.html'))
    apply_to(os.path.join(this_file_dir, 'faq.html'))
    apply_to(os.path.join(this_file_dir, 'multi_edition_video.html'))
    copytree(os.path.join(help_location, 'images'), os.path.join(page_dir, 'images'))


if __name__ == '__main__':
    main()
    print 'Generation finished'
