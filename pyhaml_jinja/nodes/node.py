"""Base node with all common functionality."""

__all__ = ['Node']


class Node(object):
  """Base node intended to be sub-classed (but still can be instantiated)."""

  def __init__(self):
    self.parent = None
    self.children = []

  def __repr__(self):
    return '<{node_type}: {children} children>'.format(
        node_type=self.__class__.__name__, children=len(self.get_children()))

  def get_children(self):
    """Return the list of child nodes."""

    return self.children

  def has_children(self):
    """Return whether or not this node has any children."""

    return bool(self.children)

  def add_child(self, child):
    """Safely add a child node to this node."""

    if not self.children_allowed():
      raise RuntimeError('Child nodes are not allowed on this node.')

    if not isinstance(child, Node):
      raise ValueError('Expected a Node, got %s.' % type(child))

    if child.parent:
      raise RuntimeError('Child already has a parent: %s' % child.parent)

    child.parent = self
    self.children.append(child)

  def children_allowed(self):
    """Determine whether children are allowed on this node.

    True by default, but should be overridden by other node types.
    """

    return True

  def get_previous_sibling(self):
    """Get the sibling previous to this node, if it exists."""

    if not self.parent:
      return None

    index = self.parent.get_children().index(self)
    if index > 0:
      return self.parent.get_children()[index - 1]

  def get_next_sibling(self):
    """Get the sibling next to this node, if it exists."""

    if not self.parent:
      return None

    index = self.parent.get_children().index(self)
    if index < len(self.parent.get_children()) - 1:
      return self.parent.get_children()[index + 1]

  def render_lines(self, indent_string=None, indent_level=0):
    """Render the node as a tree, returning a list of lines."""

    lines = []
    start, end = self.render_start(), self.render_end()
    indent = indent_level * (indent_string or '')

    if start is not None:
      lines.append(indent + self.render_start())

    for child in self.get_children():
      child_lines = child.render_lines(indent_string=indent_string,
                                       indent_level=indent_level + 1)
      lines.extend(child_lines)

    if end is not None:
      lines.append(indent + self.render_end())

    return lines

  def render_start(self):
    """Render the string representation of the opening of this node."""

    return None

  def render_end(self):
    """Render the string representation of the closing of this node."""

    return None

