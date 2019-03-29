#Written by Dylan Desai for CSCE578 (Text processing)
import fileinput
import operator
import glob
import os
import string
import math
import marshal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

#returns corpus of documents
def getDocs(path):
    #variables
    files = list()
    docs = list()
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
            doc = ""
            wordCount = dict()
            for line in lines:
                #strip punctuation, add to doc
                line = (line.translate(str.maketrans('', '', string.punctuation))).lower()
                for word in line.split():
                    doc += word + " "
            docs.append(doc)
            #print(doc)
    os.chdir(currPath)
    return docs

#Uses scikit-learn to return kmean clusters given the vectorizor, tifidf matrix, and number of clusters
def doKMeans(vectorizer, tfidfs, clusterNum):
    ret = list()
    kmeans = KMeans(n_clusters=clusterNum, init='k-means++', max_iter=100)
    kmeans.fit(tfidfs)

    #sort centroids
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    #get and return features in each cluster
    terms = vectorizer.get_feature_names()
    for i in range(clusterNum):
        cluster = list()
        #order by features closest to centroid
        for ind in order_centroids[i, :15]:
            cluster.append(terms[ind])
        ret.append(cluster)

    return ret

#writes results to file 'results.txt' and standard output
def write_file(data, fileName):
    w = open(fileName, 'w')
    i = 1
    writestring = ""

    for cluster in data:
        tmp = str(i)
        writestring += "\nCluster " + tmp + ":\n"
        for feature in cluster:
            writestring += feature + "\n"
        i += 1
    print(writestring)
    w.write(writestring)
    w.close()

def main():
    tmp_path = "./data/test"
    doc_path = "./data/Datastudent/Data2014/2014_4_101_600"

    #docDictTup = getDocs(tmp_path)
    corpus = getDocs(doc_path)

    #prepare the tf-idf matrix by initializing the vectorizer for the kmeans model
    vectorizor = TfidfVectorizer(stop_words = 'english')
    tfidfs = vectorizor.fit_transform(corpus)
    print("Dimensions of tfidf matrix: ", tfidfs.shape)

    #do the kmeans clustering
    clusterNum = 5
    clusters = doKMeans(vectorizor, tfidfs, clusterNum)

    #write the results to a byte file (for reading in main program)
    outputPath = "results.txt"
    write_file(clusters, outputPath)

if __name__ == "__main__":
    main()
