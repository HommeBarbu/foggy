# Download fogbugz wikis

from fogbugz import FogBugz
import fbSettings
import os
import pypandoc

# Get an array of wiki ids
def get_wiki_ids(fb):
    wikis = fb.listWikis()
    wiki_ids = []
    for wiki_id in wikis.findAll('ixWiki'):
        wiki_ids.append(wiki_id.string)
    return wiki_ids

# Get an array of article ids
def get_article_ids(fb, wiki_id):
    articles = fb.listArticles(ixWiki=wiki_id)
    article_ids = []
    for article_id in articles.findAll('ixWikiPage'):
        article_ids.append(article_id.string)
    return article_ids

# Loop through all articles across all wikis and save
# them to the filesystem as markdown.
def download_wikis(fb):
    resp = fb.listWikis()

    for wiki in resp.wikis.childGenerator():
        wiki_id = wiki.ixWiki.string
        wiki_name = wiki.sWiki.string
        print(wiki_id, wiki_name)

        # Create a subdirectory with the name of the wiki
        if not os.path.exists(wiki_name):
            os.mkdir(wiki_name)

        article_ids = get_article_ids(fb, wiki_id)
        for article_id in article_ids:
            article = fb.viewArticle(ixWikiPage=article_id)

            headline = article.wikipage.sHeadline.string
            body = article.wikipage.sBody.string
            print(headline)

            filename = headline.replace('/', '') + '.html'
            path = os.path.join(wiki_name, filename)

            # Block for just writing out HTML
            if False:
                with open(path, 'w') as f:
                    try:
                        f.write(body)
                    except:
                        print("Unable to write {} - {}".format(wiki_name, headline))

            # Convert to markdown and write
            try:
                output = pypandoc.convert_text(body, to='md', format='html',
                                               outputfile=path)
            except:
                print("Unable to write {} - {}".format(wiki_name, headline))

if __name__ == '__main__':
    fb = FogBugz(fbSettings.URL, fbSettings.TOKEN)
    download_wikis(fb)
