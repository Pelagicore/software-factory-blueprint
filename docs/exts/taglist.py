'''Taglist extension for Sphinx Documentation Generator.

Use this module to tag documents and to generate a list of links to tagged
documents anywhere in your documentation.

.. warning::

    Only tested with the html builder.

Directives
----------

tag:
    Add a tag to the current document. Tags are provided as a comma separated
    list.

    Example: ::
        .. tag:: tag1, tag2

    or: ::
        .. tag:: tag1

taglist:
    Generate a list of links to tagged documents. The first argument is the tag
    to match against.

    It outputs a bullet list of references to tagged documents. The title
    of the linked document will be used for the link text.

    Example: ::
        ..taglist: tag1

'''
from sphinx.util import logging
from docutils.parsers.rst import Directive
from docutils import nodes
from sphinx.environment import NoUri


def initialize(app):
    env = app.builder.env
    if not hasattr(env, 'tags'):
        env.tags = dict()
    if not hasattr(env, 'taglist_docs'):
        env.taglist_docs = []


class tag_node(nodes.General, nodes.Element):
    #: list(str): Tags associated with the node
    tags = []


class taglist(nodes.General, nodes.Element):
    #: list(str): Tags associated with the node
    tags = []


class TagDirective(Directive):
    '''Directive for adding tags to a document.

    This class represents a tag directive in rst. A tag can have multiple tags
    as arguments (up to 25) supplied by a comma separated list.
    '''
    #: int: Minimum number of tags allowed
    required_arguments = 0
    #: int: Maximum number of tags allowed
    optional_arguments = 25

    def run(self):
        '''Function to process tags from the arguments.

        This function is called to process arguments and returns a list of tag
        nodes that will be inserted into the document tree at the point where
        the directive was encountered.
        '''
        env = self.state.document.settings.env

        tag = tag_node()
        tag.tags = [tagname.strip().replace(',', '') for tagname in self.arguments]

        return [tag]


class TagListDirective(Directive):
    '''Directive for generating a list of tagged articles.

    This class represents a taglist directive in rst. A taglist generates a
    list of links to tagged documents.
    '''
    #: int: Minimum number of tags allowed
    required_arguments = 0
    #: int: Maximum number of tags allowed
    optional_arguments = 25

    def run(self):
        '''Function to process tags from the arguments.

        This function is called to process arguments and returns a list of tag
        nodes that will be inserted into the document tree at the point where
        the directive was encountered.
        '''
        tl = taglist('')
        tl.tags = self.arguments

        env = self.state.document.settings.env
        if env.docname not in env.taglist_docs:
            env.taglist_docs.append(env.docname)

        return [tl]


def process_tags(app, doctree):
    '''Tracerse tag nodes and save metadata.

    Save metadata here instead of the directive because of unfinished
    processing when the directive is called. For e.g. titles not generated.
    Finally remove node from the doctree as it's not supposed to render.

    Args:
        app (Sphinx): The sphinx application object.
        doctree(nodes.Node): The document tree

    '''
    env = app.builder.env

    for node in doctree.traverse(tag_node):
        for tagname in node.tags:
            if tagname not in env.tags:
                env.tags[tagname] = []
            env.tags[tagname].append({
                'docname': env.docname,
                'title': env.titles[env.docname][0].rawsource
            })
        node.replace_self([])


def generate_list_items(app, tagname, fromdocname, sort=True):
    '''Generate list items with link to every document tagged with tagname.

    List items concists of a inner paragraph. The paragraph then contains a
    reference to the tagged document.

    Args:
        app (Sphinx): The sphinx application object.
        tagname (str): The tag to generate list items for.
        fromdocname (str): The source document.

    Yields:
        docutils.nodes.list_item

    '''
    env = app.builder.env

    if sort:
        docs = sorted(env.tags[tagname], key=lambda doc: doc['title'].lower())
    else:
        docs = env.tags[tagname]

    for doc_info in docs:
        item = nodes.list_item()
        innerpara = nodes.paragraph()

        description = '%s' % doc_info['title']

        item += innerpara

        # Create a reference
        refnode = nodes.reference('', '', internal=True)

        try:
            refnode['refuri'] = app.builder.get_relative_uri(fromdocname, doc_info['docname'])
        except NoUri:
            logging.getLogger(__name__).warning('%s.%s: URI cannot be determined' % (fromdocname, node.line))

        refnode.append(nodes.Text(description, description))

        innerpara += refnode

        yield item


def get_bullet_list(app, tagname, fromdocname):
    '''Create a bullet list of links to documents tagged with tagname.

    Args:
        app (Sphinx): The sphinx application object.
        tagname (str): The tag to generate list items for.
        fromdocname (str): The source document.

    Returns:
        docutils.nodes.bullet_list

    '''
    bullet_list = nodes.bullet_list('')

    for list_item in generate_list_items(app, tagname, fromdocname):
        bullet_list.append(list_item)

    return bullet_list


def process_taglist_nodes(app, doctree, fromdocname):
    '''Replace taglist nodes with a bullet list.

    Traverse all taglist nodes and replace with a bullet list of matching
    articles.

    Args:
        app (Sphinx): The sphinx application object.
        doctree (nodes.Node): The document tree.
        fromdocname (str): The source document.

    '''
    env = app.builder.env

    for node in doctree.traverse(taglist):
        content = []

        for tagname in env.tags:
            if tagname not in node.tags:
                continue

            bullet_list = get_bullet_list(app, tagname, fromdocname)

            content.append(bullet_list)

        node.replace_self(content)


def purge_doc(app, env, docname):
    '''Called whenever a document is changed or removed.

    Remove all occurences of the document from all tags. The document will be
    re-added when the source is read if the tag still persists.

    Args:
        app (Sphinx): The sphinx application object.
        env (dict): The build environment.
        fromdocname (str): The source document.

    '''
    tags = dict()
    for tagname in env.tags:
        newdocs = [doc for doc in env.tags[tagname] if doc['docname'] != docname]
        if newdocs:
            tags[tagname] = newdocs

    env.tags = tags

    if docname in env.taglist_docs:
        env.taglist_docs.remove(docname)


def reread_taglist_docs(app, env, added, changed, removed):
    '''Called when sphinx has determined which source files have changed.

    Returns:
        A list of docnames to re-read in addition to what has already been
        determined by sphinx.

    '''
    return env.taglist_docs


def setup(app):
    app.add_node(taglist)
    app.add_node(tag_node)

    app.add_directive('tags', TagDirective)
    app.add_directive('taglist', TagListDirective)

    app.connect('builder-inited', initialize)
    app.connect('doctree-read', process_tags)
    app.connect('doctree-resolved', process_taglist_nodes)
    app.connect('env-purge-doc', purge_doc)
    app.connect('env-get-outdated', reread_taglist_docs)

    return {'version': '0.2'}  # identifies the version of the extension
