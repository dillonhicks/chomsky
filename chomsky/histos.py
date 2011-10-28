from pprint import pprint
import nltk

from chomsky import db

def sort_histo(a, b):
    return cmp(a[1], b[1])

def histograms(articles):
    for article in articles:
        print 'Histogram: ', article
        print 

        # Case doesnt matter we just care about the words.
        text = article.text.lower()
        histo = {}
        tokens = set(nltk.word_tokenize(text))
        
        for token in tokens:
            if token.endswith('.') and \
                    token[:-1] in tokens:
                # If there is a token that happens to be 'blarg.' and
                # also 'blarg' just add the count of 'blarg.' to
                # 'blarg' Since the tokenizer doesnt account for '.'
                # at the moment.
                conunt = text.count(token)
                token = token[:-1]

            else:
                count = text.count(token)

            try:
                histo[token] += count
            except KeyError:
                histo[token] = count
        

        yield histo

def aggregate_counts(histograms, min_len=5, sort=False):
    # TODO: Change min_len to something about functional morphemes
    # (in, a, the, through, etc.)
    aggregate_histo = {}
    for histogram in histograms:
        for key, value in histogram.items():
            if len(key) < min_len:
                continue
            try:
                aggregate_histo[key] += value
            except KeyError:
                aggregate_histo[key] = value
    if not sort:
        return aggregate_histo
    else:
        return sorted(aggregate_histo.items(), cmp=sort_histo)


if __name__ == "__main__":
    
    
    tokenized_texts = tokenize(texts)
    histos = histograms(tokenized_texts)
    aggregate = aggregate_counts(histos)
    aggregate = sorted(aggregate.items(), cmp=sort_histo)
    
    print yaml.dump(aggregate)
    print len(aggregate)

    # sorted_histos = sort_histograms(histos)
    # merged_histos = merge_histograms(sorted_histos)
    
    # print yaml.dump(merged_histos)
    

