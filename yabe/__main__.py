from yabe import yabe, db
from .models import Post, Admin, Comment, Tag, Category
import os
import click


@click.group()
def cli():
    """ Yabe CLI """
    pass


@cli.command()
def drop_all_database():
    db.session.remove()
    db.drop_all()


@cli.command()
def create_all_database():
    db.create_all()


@cli.command()
def fill_test_data():
    c = '''# h1 Heading 8-)
<h2> h2 Heading by HTML</h2>
## h2 Heading
### h3 Heading

## Horizontal Rules

___

---

***

## Typographic replacements

Enable typographer option to see result.

(c) (C) (r) (R) (tm) (TM) (p) (P) +-

test.. test... test..... test?..... test!....

!!!!!! ???? ,,  -- ---

"Smartypants, double quotes" and 'single quotes'


## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## Code

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code


Block code "fences"

```
Sample text here...
```
Syntax highlighting

``` javascript
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```

``` go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

## Tables

| Option | Description |
| ------ | ----------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

Right aligned columns

| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

## Links

[vue-markdown](https://github.com/miaolz123/vue-markdown)

[link with title](https://github.com/miaolz123/vue-markdown "VueMarkdown")

Autoconverted link https://github.com/miaolz123/vue-markdown (enable linkify to see)


## Images

![Minion](dist/img/minion.png)

Like links, Images also have a footnote style syntax

![Alt text][id]

With a reference later in the document defining the URL location:

[id]: dist/img/minion.png  "The Dojocat"


### Emojies

> Classic markup: :wink: :cry: :laughing: :yum:
>
> Shortcuts (emoticons): :-) :-( 8-) ;)


### Subscript / Superscript

- 19^th^
- H~2~O


### \<ins>

++Inserted text++


### \<mark>

==Marked text==


### Footnotes

Footnote 1 link[^first].

Footnote 2 link[^second].

Inline footnote^[Text of inline footnote] definition.

Duplicated footnote reference[^second].

[^first]: Footnote **can have markup**

    and multiple paragraphs.

[^second]: Footnote text.


### Definition lists

Term 1

:   Definition 1
with lazy continuation.

Term 2 with *inline markup*

:   Definition 2

        { some code, part of Definition 2 }

    Third paragraph of definition 2.

_Compact style:_

Term 1
  ~ Definition 1

Term 2
  ~ Definition 2a
  ~ Definition 2b


### Abbreviations

This is HTML abbreviation example.

It converts "HTML", but keep intact partial entries like "xxxHTMLyyy" and so on.

*[HTML]: Hyper Text Markup Language
    '''
    p1 = Post(
        title='Test Post 1',
        content=
        '<h1>Hello World!</h1><p/>This is a test post, remove it after development<p/>YABE - Yet Another Blog Engine'
    )
    p2 = Post(
        title='Test Post 2',
        content=c,
        author="Shiroko",
        summary="test summary test sumary这是一则测试摘要, 其中不能使用任何标签<h1>比如说这个</h1>")
    admin = Admin(username='admin', has_power=True)
    admin.set_passwd('123456')
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(admin)
    c1 = Comment(
        username="TestUser1",
        email="test@email.com",
        content="fuckyouasijkad测试测试测试测试as蛋壳阿萨德;jaguar;东京坑")
    c2 = Comment(
        username="Shiroko",
        email="hhx.xxm@gmail.com",
        content="测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容Test content")
    db.session.add(c1)
    db.session.add(c2)
    p2.add_comment(c1)
    p2.add_comment(c2)
    ct1 = Category(title="测试用分类", summary="这个分类是测试用分类, 不应该出现在生产数据库中.")
    t1 = Tag(content="测试标签1")
    t2 = Tag(content="T2")
    t3 = Tag(content="for test 33333")
    db.session.add(ct1)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)

    p2.add_tag(t1)
    p2.add_tag(t2)
    p2.add_tag(t3)
    ct1.add_post(p2)

    db.session.commit()
    db.session.close()


@cli.command()
def allinone():
    drop_all_database()
    create_all_database()
    fill_test_data()


if __name__ == '__main__':
    cli()
