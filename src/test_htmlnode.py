import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, TextNode, text_node_to_html_node

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_printing_nodes(self):
        node = HTMLNode("h1", "150", ("h1") , {"href": "https://www.google.com"})
        node2 = HTMLNode(
            "h1",
            "150",
            ("h1"),
            {
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "highlighted"
            }
        )
        node.props_to_html()
        node2.props_to_html()
        #self.assertEqual(node, node2)
        #self.assertNotEqual(node, node3)

    def test_leaf_to_html_p(self):
        node3 = LeafNode("p", "Hello, world!")
        node4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node3.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node4.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_single_leaf_node(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_parent_with_multiple_leaf_children(self):
        child1 = LeafNode("span", "First")
        child2 = LeafNode("span", "Second")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>First</span><span>Second</span></div>")

    def test_to_html_nested_mixed_nodes(self):
        grandchild1 = LeafNode("em", "Italic")
        grandchild2 = LeafNode("strong", "Bold")
        child = ParentNode("p", [grandchild1, grandchild2])
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), "<section><p><em>Italic</em><strong>Bold</strong></p></section>")

    def test_to_html_deeply_nested_nodes(self):
        level4 = LeafNode("u", "deep")
        level3 = ParentNode("span", [level4])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])
        root = ParentNode("article", [level1])
        self.assertEqual(root.to_html(), "<article><section><div><span><u>deep</u></span></div></section></article>")

    def test_to_html_with_empty_parent(self):
        empty = ParentNode("div", [])
        self.assertEqual(empty.to_html(), "<div></div>")

    def test_to_html_mixed_leaf_and_parent_children(self):
        leaf = LeafNode("h1", "Title")
        nested_leaf = LeafNode("p", "Paragraph")
        nested_parent = ParentNode("div", [nested_leaf])
        root = ParentNode("section", [leaf, nested_parent])
        self.assertEqual(root.to_html(), "<section><h1>Title</h1><div><p>Paragraph</p></div></section>")

    def test_to_html_with_multiple_nested_parents(self):
        inner_most = LeafNode("code", "x = 42")
        inner = ParentNode("pre", [inner_most])
        middle = ParentNode("div", [inner])
        outer = ParentNode("section", [middle])
        self.assertEqual(outer.to_html(), "<section><div><pre><code>x = 42</code></pre></div></section>")

    def test_to_html_leaf_with_special_characters(self):
        node = LeafNode("p", "This & that < those > these")
        self.assertEqual(node.to_html(), "<p>This & that < those > these</p>")

    def test_to_html_nested_lists(self):
        li1 = LeafNode("li", "Item 1")
        li2 = LeafNode("li", "Item 2")
        ul = ParentNode("ul", [li1, li2])
        div = ParentNode("div", [ul])
        self.assertEqual(div.to_html(), "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_bold(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")


if __name__ == "__main__":
    unittest.main()