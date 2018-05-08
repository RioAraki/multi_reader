A note to remind me knowledges about epubs. It does not include all details, just those I did not quite familiar with. For original resource please refers to https://zhuanlan.zhihu.com/p/29954562

# Epub organization
```
XXX.epub
| mimetype
|- META-INF
	container.xml
|-OEBPS
	| content.opf
	| toc.ncx
	| - Audio
	|	xxx.mp3
	| - Fonts
	|	xxx.ttf
	| - Images
	|	xxx.png
	| - Styles
	|	Stylesheet.css
	| - Text
	|	xxx.html
	| - Video
	|	xxx.mp4
```

## mimetype and container.xml

Both are necessary

### mimetype

Short for media type.
> A media type (formerly known as MIME type or content type) is a two-part identifier for file formats and format contents transmitted on the Internet. The Internet Assigned Numbers Authority (IANA) is the official authority for the standardization and publication of these classifications. Media types were originally defined in Request for Comments 2045 in November 1996 as a part of MIME (Multipurpose Internet Mail Extensions) specification, for denoting type of email message content and attachments;

Tell the system the content is in epub format. The content of epub should be `application/epub+zip`.

Here is a reference for different available mimetypes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types

### container.xml

This file would **direct** the parser to the package file `content.opf`. Every epub must have a unique package file named `content.opf`, it specifies everything you need for an epub including all content files, the related resources, meta info, navigation info, reading order and so on. 

### content.opf

As mentioned before, `opf` shorts for open package formats which is essentially an xml file. It normally contains 5 parts:

- The package element: it is the biggest container which contains all other elements in the file. The package element has an important property called `unique-identifier=book-id` which could be used to identify a book.

- The metadata element: As the name suggests, used to save metadata including:
    - language
    - title
    - author
    - date: with options like creation, modification and publication
    - identifier:could be [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier#Encoding)
    - subject
    - description
    - contributor
    - source
    - rights
These metadata could be used on book's cover or frontpage to display related information.