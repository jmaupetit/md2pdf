# An exhibit of Markdown

This note demonstrates some of what [Markdown][1] is capable of doing.

*Note: Feel free to play with this page. Unlike regular notes, this doesn't automatically save itself.*

## Table of Contents

- [Basic formatting](#basic-formatting)  
- [Lists](#lists)  
  - [Ordered list](#ordered-list)  
  - [Unordered list](#unordered-list)
- [Paragraph modifiers](#paragraph-modifiers)
  - [Code block](#code-block)
  - [Quote](#quote)
- [Headings](#headings)  
  - [Headings *can* also contain **formatting**](#headings-formatting)
  - [They can even contain `inline code`](#headings-inline-code)
- [URLs](#urls)  
- [Horizontal rule](#horizontal-rule)  
- [Images](#images)  
- [Finally](#finally)  

*Note: The anchor point gets definied by the name attribute of the anchor tag.*

<a name="basic-formatting"></a>

## Basic formatting

Paragraphs can be written like so. A paragraph is the basic block of Markdown. A paragraph is what text will turn into when there is no reason it should become anything else.

Paragraphs must be separated by a blank line. Basic formatting of *italics* and **bold** is supported. This *can be **nested** like* so.

<a name="lists"></a>

## Lists

<a name="ordered-list"></a>

### Ordered list

1. Item 1
2. A second item
3. Number 3
4. Ⅳ

*Note: the fourth item uses the Unicode character for [Roman numeral four][2].*

<a name="unordered-list"></a>

### Unordered list

* An item
* Another item
* Yet another item
* And there's more...

<a name="paragraph-modifiers"></a>

## Paragraph modifiers

<a name="code-block"></a>

### Code block

    Code blocks are very useful for developers and other people who look at code or other things that are written in plain text. As you can see, it uses a fixed-width font.

You can also make `inline code` to add code into other things.

<a name="quote"></a>

### Quote

> Here is a quote. What this is should be self explanatory. Quotes are automatically indented when they are used.

<a name="headings"></a>

## Headings

There are six levels of headings. They correspond with the six levels of HTML headings. You've probably noticed them already in the page. Each level down uses one more hash character.

<a name="headings-formatting"></a>

### Headings *can* also contain **formatting**

<a name="headings-inline-code"></a>

### They can even contain `inline code`

Of course, demonstrating what headings look like messes up the structure of the page.

I don't recommend using more than three or four levels of headings here, because, when you're smallest heading isn't too small, and you're largest heading isn't too big, and you want each size up to look noticeably larger and more important, there there are only so many sizes that you can use.

<a name="urls"></a>

## URLs

URLs can be made in a handful of ways:

* A named link to [MarkItDown][3]. The easiest way to do these is to select what you want to make a link and hit `Ctrl+L`.
* Another named link to [MarkItDown](http://www.markitdown.net/)
* Sometimes you just want a URL like <http://www.markitdown.net/>.

<a name="horizontal-rule"></a>

## Horizontal rule

A horizontal rule is a line that goes across the middle of the page.

---

It's sometimes handy for breaking things up.

<a name="images"></a>

## Images

Markdown can also contain images. I'll need to add something here sometime.

<a name="finally"></a>

## Finally

There's actually a lot more to Markdown than this. See the official [introduction][4] and [syntax][5] for more information. However, be aware that this is not using the official implementation, and this might work subtly differently in some of the little things.


  [1]: http://daringfireball.net/projects/markdown/
  [2]: http://www.fileformat.info/info/unicode/char/2163/index.htm
  [3]: http://www.markitdown.net/
  [4]: http://daringfireball.net/projects/markdown/basics
  [5]: http://daringfireball.net/projects/markdown/syntax
