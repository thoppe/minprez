import copy, re, itertools
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown
from mistune import BlockGrammar, BlockLexer, Markdown
import logging

logger = logging.getLogger("miniprez")


def get_classnames(class_string):
    s = " ".join(class_string.strip().lstrip(".").split("."))
    return s if s else None


class DivClassRenderer(Renderer):
    def OpenBlock(self, names):
        return f"<div class='{names}'>"

    def CloseBlock(self):
        return f"</div>"

    def LineBlock(self, names, remaining):
        remaining = remaining.lstrip()
        return f"<span class='{names}'>{remaining}</span>"

    def SectionTags(self, names):
        return f"<meta data-slide-classes='{names}'/>"

    def Emoji(self, name):
        return f"<emoji data-emoji-alias='{name}'/></emoji>"

    def FontAwesome(self, name):
        return f"<span class='fa fa-{name}' aria-hidden=true></i>"

    def InlineLaTeX(self, expression):
        return f'<span class="inline-equation" data-expr="{expression}"></span>'

    def BlockLaTeX(self, expression):
        expression = " ".join(expression.strip().split())
        return f'<div class="block-equation" data-expr="{expression}"></div>'


class DivClassInlineLexer(InlineLexer):
    def enable(self):

        self.default_rules.remove("escape")
        self.default_rules.remove("linebreak")

        rule_n = itertools.count()

        # SectionTags, ...align-center.bg-black
        grammar = r"[\s]*\.\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.SectionTags = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "SectionTags")

        # OpenBlock, ..align-center.bg-black
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"[\s]*\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.OpenBlock = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "OpenBlock")

        # CloseBlock, ..
        grammar = r"[\s]*[^\\]\.\."
        self.rules.CloseBlock = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "CloseBlock")

        # LineBlock, .text-data
        grammar = r"[\s]*\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)"
        self.rules.LineBlock = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "LineBlock")

        # Short image link
        # grammar = (r'''^!\s*(<)?([\s\S]*?)(?(2)>)(?:\s+['"]([\s\S]*?)['"])?\s*\)''')
        # self.rules.ShortImageLink = re.compile(grammar)
        # self.default_rules.insert(next(rule_n), "ShortImageLink")

        # Emoji, :stuck_out_tongue_closed_eyes:
        grammar = r"::([\w\_]+)::"
        self.rules.FontAwesome = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "FontAwesome")

        # Emoji, :stuck_out_tongue_closed_eyes:
        grammar = r"(:[\w\_]+:)"
        self.rules.Emoji = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "Emoji")

        # Block LaTeX, $$\int_{-\infty}^\infty \n \hat \f\xi\,e^{2 \pi i \xi x} \,d\xi$$
        grammar = "\$\$([^\$]*)\$\$"
        self.rules.BlockLaTeX = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "BlockLaTeX")

        # Single line LaTeX, $\int_{-\infty}^\infty \hat \f\xi\,e^{2 \pi i \xi x} \,d\xi$
        grammar = r"\$([^\n]+)\$"
        self.rules.InlineLaTeX = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "InlineLaTeX")

        # SlashDotEscape, \.
        grammar = r"\\\."
        self.rules.SlashDotEscape = re.compile(grammar)
        self.default_rules.insert(-1, "SlashDotEscape")

        # AlmostText1 matches \w\d and then things with a token
        tokens = r"\\<!\[_*`~@.:\$"
        grammar = r"^[\s]+[a-zA-Z0-9.-][\w\d%s]+" % tokens
        self.rules.AlmostText1 = re.compile(grammar)
        self.default_rules.insert(-1, "AlmostText1")

        # AlmostText2 matches up to a special token
        grammar = r"^[\s\S]+?(?=[%s ]|$)" % tokens
        self.rules.AlmostText2 = re.compile(grammar)
        self.default_rules.insert(-1, "AlmostText2")

    def output_LineBlock(self, m):
        tags = get_classnames(m.group(1))

        # Run the parser over what's inside
        remaining = self.output(m.group(2))
        return self.renderer.LineBlock(tags, remaining)

    def output_SectionTags(self, m):
        tags = get_classnames(m.group())
        return self.renderer.SectionTags(tags)

    def output_OpenBlock(self, m):
        tags = get_classnames(m.group())
        return self.renderer.OpenBlock(tags)

    def output_CloseBlock(self, m):
        return self.renderer.CloseBlock()

    def output_Emoji(self, m):
        return self.renderer.Emoji(m.group(1))

    def output_FontAwesome(self, m):
        return self.renderer.FontAwesome(m.group(1))

    def output_InlineLaTeX(self, m):
        return self.renderer.InlineLaTeX(m.group(1).strip())

    def output_BlockLaTeX(self, m):
        return self.renderer.BlockLaTeX(m.group(1).strip())

    def output_SlashDotEscape(self, m):
        return "."

    def output_AlmostText1(self, m):
        # logger.debug(f"AlmostText1 {m.group(0)}")
        return m.group()

    def output_AlmostText2(self, m):
        # logger.debug(f"AlmostText1 {m.group(0)}")
        return m.group()

    def output_text(self, m):
        # We normally shouldn't be here, but return even if we do
        return m.group()


# Monkeypatch the paragraph
class Markdown_NP(Markdown):
    def output_paragraph(self):
        text = self.token["text"].strip()
        return self.inline(text + " ")


# Globally build the parser

renderer = DivClassRenderer()
inline = DivClassInlineLexer(renderer)

# Enable the features
inline.enable()

parser = Markdown_NP(renderer, inline=inline)


if __name__ == "__main__":
    tx0 = r"""
...bg-black

..aligncenter.black
# fool.
the :smile: ::igloo::
words
on
the table 
.wtf Out *of* center
here *we* go

$$ \int_{-\infty}^\infty \hat \f\xi\,e^{2 \pi i \xi x} 
\,d\xi $$ 
"""

    # tx0 = "The end _of_ the *world* ."

    # import coloredlogs, logging
    # logger = logging.getLogger("miniprez")
    # fmt = "%(message)s"
    # coloredlogs.install(level="DEBUG", logger=logger, fmt=fmt)
    # logger.setLevel(logging.DEBUG)

    print(inline.default_rules)
    print(tx0)
    print("MARKDOWNED")
    tx1 = parser(tx0)
    print(tx1)
