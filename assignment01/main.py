#Written by Dylan Desai for CSCE578 (Text processing)

import fileinput
import operator
import glob
import os

def getReportingVerbs(fileName):
    #read the file and return the dictionary of verbs
    ret = dict()
    f = open(fileName, "r")

    if f.mode == 'r':
        f1 = f.readlines()
        for l in f1:
            ret[l.strip()] = 0 

    return ret

def read(path):
    #variables
    files = list()
    ret = list()
    currPath = os.getcwd()

    #get list of files
    os.chdir(path)
    for file in glob.glob("*.txt"):
                files.append(file)

    #sort list of files and read
    files.sort()
    for f in files:
        opener = open(f, "r")
        if opener.mode == 'r':
            lines = opener.readlines()
            for line in lines:
                splitline = line.split()
                if splitline[3] == 'B':
                    ret.append(splitline)

    #go back and return list of tokens
    os.chdir(currPath)
    return ret

def freq(tokens, dictionary):
    #Filter tokens by verbs and see if they match the reporting verbs
    for tokenList in tokens:
        for token in tokenList:
            if "_V" in token:
                verbWithTag = token
                verb = verbWithTag.split("_")[0].lower().strip()
                if verb in dictionary:
                    dictionary[verb] += 1
    return dictionary

def getTop(dictionary):
    #tuplelist > sorted list of tuples so that we get top 20 reporting verbs
    ret = list()
    temp_tuple = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(0,20,1):
            ret.append(temp_tuple[i])
    return ret

def writeResult(top1, top2, fileName):
    #Write top 20 reporting verbs to output filename
    writeString = ""
    w = open(fileName, "w")
    writeString += "COCA Top 20 verbs with count:\n"

    for i in range(0,len(top1), 1):
        writeString += ''.join(str(top1[i]) + "\n")

    writeString += "\n\nStudent data Top 20 verbs with count:\n"
    for i in range(0,len(top2), 1):
        writeString += ''.join(str(top2[i]) + "\n")
    w.write(writeString)

def main():
    #maps of verbs and count of frequency
    reportingCoca = dict()
    reportingStudent = dict()

    #get maps of reporting verbs for each set
    reportingCoca = getReportingVerbs("reportingverbs.txt")
    reportingStudent = getReportingVerbs("reportingverbs.txt")

    #first, read cocoa in bulk, and get list of tokens
    cocoa_path = "./COCA/sentpos/2009-1"
    cocaTolkens = read(cocoa_path)

    #next, read student data in bulk, and add that to previous list
    student_path = "./Student"
    studentTolkens = read(student_path)

    #do frequency counts
    reportingCoca = freq(cocaTolkens, reportingCoca)
    reportingStudent = freq(studentTolkens, reportingStudent)

    #get top 20 most frequently used
    cocaTop = getTop(reportingCoca)
    studentTop = getTop(reportingStudent)

    #finally, write the results to a file
    output_file = "results.txt"
    writeResult(cocaTop, studentTop, output_file)


if __name__ == "__main__":
    main()
