# LabWebsiteFromMarkdown
To enable quicker and better updates to the Lab website, I set up a repository using the Markdown library to edit the content and Markdown and then automatically export the content to the lab website. I hope this enables more people in the lab to contribute to the site and keep information updated. 

## Editing Markdown

Pages can be written as markdown `.md` files place in the correct subfolder in `source`. In the markdown you can use standard heading, formating, links, etc. See this [Guide](https://www.markdownguide.org/basic-syntax/). Additionally, you can use the following elements: 

`<p>,<div>,<...>`: Any block-level html tag will be untouched and included

`{!<FILE.HTM>!}`: Includes a raw html file into the page 

`{+head:<WINDOWTITLE>:style3.css}`: Adds the header for the website with a title and CSS sheet to include 

`{+title:<TITLE>:<ICON>}`: Adds the diedrichsenlab-style header bar, the icon is optional 

`{+ref:<BIBID>: <LINK>}`: Adds a reference from the references.bib file with a pdf-link to the paper (optional)

 `{+personcell: <FIRST>: <LAST>: <ROLE>: <DETAILS> :<PICTURE>: <EMAIL>: <LINK>}`: Adds a person cell for the people's page

`{+sidebar:<ACTIVE>}`: Add the menu side bar for the mid, with a specific number icon active

New images / references should be submitted to the corresponding folder in `source`

## Deploying the webpage

A single Markdown file can be compiled to the target directory using 

`python3 build.py filename1 filename2`: From the file name, drop the `.md` extenstion 

Also possible is to build a custom list of files: 

`root`: All main pages 

`research`: All research pages 

`suit`: All suit-related pages 



