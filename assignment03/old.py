#written by Dylan Desai for CSCE578
import fileinput
import operator
import glob
import os
import string
import math
import marshal

def getData(path):
    ret = list()
    f = open(path, 'rb')
    ret = marshal.load(f)
    f.close()
    return ret

#returns list of cosine similarities
def doCalc(vect1, vect2):
    dot = 0.0
    mag1 = 0.0
    mag2 = 0.0
    ret = 0.0

    for word in vect1.keys():
        #calculate dot product
        dot += float(vect1[word]*vect2[word])
        #calcuate magnitudes
        mag1 += float(vect1[word]*vect1[word])
        mag2 += float(vect2[word]*vect2[word])

    #get the cos val by dividing dot products by magnitudes (rooted for mathematical magnitude)
    mag1 = math.sqrt(mag1)
    mag2 = math.sqrt(mag2)
    ret = float((dot/(mag1*mag2)))
    ang = math.degrees(math.acos(ret))
    print("COSINE similarity:", ret, ang)

#returns a list of cosine similarity lists (n^2)
def cosineSimilarity(tfidfs):
    ret = list(dict())
    n = len(tfidfs)
    print("# of docs: ", n)
    for tfidf in tfidfs:
        print(tfidf)
        print("\n")

    #1st ith document
    for i in range(0, n-1) :
        #i+1 document
        for j in range(i+1, n):
            #do calculation (help func so I don't deal with quad for loops)
            #print("DOING NEW CALCULATION")
            print("\nNOW calculating cos between docs: ", i, j)
            result = doCalc(tfidfs[i], tfidfs[j])

#converts tfidfs to a matrix (for clustering)
def toMatrix(tfidfs):
    
def main():
    #retrieve tfidfs from file
    read_path = "./data/tfidf.dat"
    tfidf = getData(read_path)

    #get list of cosine similarities
    cosineSimilarity(tfidf)

    #convert tfidf to a matrix
    toMatrix(tfidf)

if __name__ == "__main__":
    main()
