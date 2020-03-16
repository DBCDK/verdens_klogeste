
The file 1000_links.xml contains a snip of the html of: https://simple.wikipedia.org/wiki/Wikipedia:List_of_articles_all_languages_should_have
The snippet contains the links to the 1000 articles. To extract the article-names do this:

  cat 1000_links.xml | grep href | cut -d\" -f 2 | cut -d/ -f 3 > 1000_links.txt

----

The file 10000_links.xml contains a snip of the html of: https://simple.wikipedia.org/wiki/Wikipedia:List_of_articles_all_languages_should_have/Expanded
The snippet contains the links to the 10000 articles. To extract the article-names do this:

  cat 10000_links.xml | egrep "href=\"/wiki" | cut -d\" -f 2 | cut -d/ -f 3 > 10000_links.txt

Notice: In reality it is only 8508 since not all the articles are in simple.wikipedia.com
