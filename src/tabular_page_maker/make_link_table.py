#!/usr/bin/env python3

import argparse
import os.path
import re
import yaml

from expressionive.expressionive import htmltags as T
import expressionive.exprpages as exprpages

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output")
    parser.add_argument("-s", "--stylesheet")
    parser.add_argument("-t", "--title")
    parser.add_argument("inputfile")
    return vars(parser.parse_args())

def htmlize(string):
    """Convert markup to HTML."""
    return T.b[m.group(2)] if (m := re.search(r"(.*)\*(.+)\*(.*)", string)) else string

def safename(name):
    """Make a name-safe form of an incoming phrase."""
    return name.replace(' ', '').replace('-', '').lower()

def make_list(contents):
    """Convert a dictionary of links to an HTML structure."""
    return T.ul[[(T.li[T.a(href=url, target="_blank")[htmlize(title)]]
                  if isinstance(url, str)
                  else [htmlize(title),
                        make_list(url)])
                 for title, url in contents.items()]]

def make_subheads_row(group, groupname):
    """Make a row containing subheads as table headers."""
    return T.tr(class_=safename(groupname))[[T.th(class_=safename(cellname))[cellname]
                                             for cellname, _ in group.items()]]

def make_link_panels_row(group, groupname):
    """Make a row containing the panels of links."""
    return T.tr(class_=safename(groupname))[[T.td(class_=safename(cellname))[make_list(cell)]
                                             for cellname, cell in group.items()]]

def make_table(table, output, title=None, stylesheet=None):
    """Make a links table."""
    return exprpages.page_text(
        T.table(border=True)[[[T.tr(class_=safename(groupname))[T.th(colspan=max(len(group) for group in table.values()),
                                                                     class_=safename(groupname))[groupname]],
                               make_subheads_row(group, groupname),
                               make_link_panels_row(group, groupname)]
                              for groupname, group in table.items()]],
        title=title or os.path.basename(output).split('.')[0].capitalize(),
        style_text=stylesheet)

def main(inputfile, stylesheet=None, title=None, output=None):
    """Make a compact HTML links page."""
    style_text = ""
    if stylesheet:
        with open(stylesheet) as sheet:
            style_text = "<style>" + sheet.read() + "</style>\n"
    with open(inputfile) as infile, open(output, 'w') as f:
        f.write(make_table(yaml.load(infile, Loader=yaml.SafeLoader),
                           output or (inputfile.removesuffix(".yaml") + ".html"),
                           title=title,
                           stylesheet=style_text))

if __name__ == "__main__":
    main(**get_args())
