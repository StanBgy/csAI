import nltk
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding="utf8") as f:
            dictionary[file] = f.read()
    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    tokens = nltk.word_tokenize(document)

    new_doc = []
    for word in tokens:
        if len(word) > 0 and word.isalpha():
            new_doc.append(word)

    return new_doc


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    IDFdict = {}
    total_documents = len(documents)
    for file in documents:
        words = set()
        words.update(documents[file])

        for word in words:
            nb_doc = sum(word in documents[file] for file in documents)
            idf = math.log(total_documents / nb_doc)
            IDFdict[word] = idf
    return IDFdict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    IDFS = []
    for file in files:
        IDF = 0
        for word in query:
            IDF += idfs[word] * files[file].count(word)

        IDFS.append((file, IDF))

    return [IDF for IDF, v in sorted(IDFS, key=lambda keyv: keyv[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentenceIDFS = []
    for sentence in sentences:
        sentence_scores = [sentence, 0, 0]

        for word in query:
            # matching word measure
            sentence_scores[1] += idfs[word]
            # query term density
            sentence_scores[2] += sentences[sentence].count(word) / len(sentences[sentence])

        sentenceIDFS.append(sentence_scores)

    return [sentence for sentence, x, v in sorted(sentenceIDFS, key=lambda item: (item[1], item[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
