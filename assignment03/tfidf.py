#Written by Dylan Desai for CSCE578 (Text processing)
import fileinput
import operator
import glob
import os
import string
import math
import marshal

#returns tuple (docs, docWordFreq, Worddicts)
def getDocs(path):
    #variables
    files = list()
    docs = list(list())
    wordCounts = list(dict())
    docWordFreq = dict()
    words = set()
    currPath = os.getcwd()

    #get list of files
    os.chdir(path)
    for file in glob.glob("*.txt"):
                files.append(file)
    files.sort()

    #for each file add the list of words as a document
    for f in files:
        opener = open(f, "r")
        if opener.mode == 'r':
            lines = opener.readlines()
            doc = list()
            wordCount = dict()
            for line in lines:
                #strip punctuation, add to doc and wordset
                line = line.translate(str.maketrans('', '', string.punctuation))
                for word in line.split():
                    doc.append(word)
                    words.add(word)
            docs.append(doc)
            print("DOCUMENT: ", doc, "\n")
    os.chdir(currPath)

    #populate word dictionaries and document word frequencies with counts
    for doc in docs:
        wordCount = dict.fromkeys(words, 0)
        for word in doc:
            wordCount[word] += 1
        wordCounts.append(wordCount)
    docWordFreq = dict.fromkeys(words, 0)
    for word in words:
        for doc in docs:
            if word in doc:
                docWordFreq[word] += 1
    return (docs, wordCounts, docWordFreq)

#Calculates TF-IDF
def getTF_IDF(docs, dicts, docFreqs):
    #variables
    tfs = list(dict())
    idfs = dict.fromkeys(docFreqs.keys(), 0)
    n = len(docs)
    print("THE LENGTH OF THE CORPUS: ", n)
    tfidfs = list(dict())
    #ret = list(dict())

    #calculate tfs per document
    for i in range(0, n, 1):
        tf = dict()
        totalWords = len(docs[i])
        for word, num in dicts[i].items():
            tf[word] = float(num/totalWords)
        tfs.append(tf)
    print("TFS !!!!!!!!!!!")
    for tf in tfs:
        print(tf)

    #calculate idfs per word
    for word, freq in docFreqs.items():
        idfs[word] = float(math.log10(n/freq))
    print("IDFS !!!!!!!!!!!")
    print(idfs)

    #calculate tf-idf
    for tf in tfs:
        idf = dict.fromkeys(docFreqs.keys(), 0)
        for word, val in tf.items():
            idf[word] = val * idfs[word]
        tfidfs.append(idf)
    return tfidfs

    #Normalize the tfidf row wize NO NEED TO DO THIS SINCE WE NORMALIZED TFs ALREADY
    #for tfidf in tfidfs:
    #    tmp = dict.fromkeys(docFreqs.keys(), 0)
    #    squareSum = 0
    #    mag = 0
    #    #calculate magnitute (square root of components squared)
    #    for word, val in tfidf.items():
    #        squareSum += ((val)*(val))
    #    mag = math.sqrt(squareSum)
    #    #Now get normalized value and add to dict
    #    for word2, val2 in tfidf.items():
    #        newval = val2/mag
    #        tmp[word2] = newval
    #    ret.append(tmp)
    #
    #return ret


#writes results to file data/tfidf.dat
def write_file(tfidf, fileName):
    write = open(fileName, 'wb')
    marshal.dump(tfidf, write)
    write.close()

def main():
    docDictTup = ()
    tmp_path = "./data/test"
    doc_path = "./data/Datastudent/Data2014/2014_4_101_600"

    #get a list of documents (list of words per txt file) and word dictionaries
    #docDictTup = getDocs(tmp_path)
    docDictTup = getDocs(doc_path)

    #calculate the tf-idf
    tfidf = getTF_IDF(docDictTup[0], docDictTup[1], docDictTup[2])

    #write the results to a byte file (for reading in main program)
    outputPath = "./data/tfidf.dat"
    write_file(tfidf, outputPath)

if __name__ == "__main__":
    main()
