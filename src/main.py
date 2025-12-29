from textnode import TextNode, TextType


def main():
    textN = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(textN)

if __name__ == "__main__":
    main()