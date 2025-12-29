from htmlnode import LeafNode, HTMLNode, ParentNode
import unittest


class TestHTMLNode(unittest.TestCase):

    def test_leaf_to_html_with_tag_and_props(self):
        node = LeafNode("p", "Hello, World!", {"class": "intro"})
        self.assertEqual(node.to_html(), '<p class="intro"> Hello, World! </p>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    



if __name__ == "__main__":
    unittest.main()