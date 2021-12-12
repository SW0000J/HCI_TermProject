import processing.comment_processing as proc
import crawling.crawling_youtube as craw

if __name__ == "__main__":
    badwords = proc.getBadWords()
    crawledComments = craw.getYoutubeComments("cCO22gPW6-4")
    # list's return value : list #