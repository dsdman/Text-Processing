#written by Dylan Desai for CSCE578
import fileinput
import operator

#returns a dictionary of word -> pos
def buildDict(path):
    ret = dict()
    opener = open(path, "r", encoding='utf-8-sig')

    if opener.mode == 'r':
        lines = opener.readlines()
        for line in lines:
            tokens = line.split()
            for token in tokens:
                tokensplit = token.split('_')
                word = str(tokensplit[0]).strip()
                pos = str(tokensplit[1]).strip()
                ret[str(word.strip())] = pos
    return ret

#compares to see which words were tagged differently
def doCompare(dic1, dic2):
    ret = list()
    keylist1 = list()
    keylist2 = list()
    keylist3 = list()
    
    #take only common words (intersection)
    for key, value in dic1.items():
        keylist1.append(key)
    for key, value in dic2.items():
        keylist2.append(key)
    keylist3 = list(set(keylist1)&set(keylist2))

    #create lists of tuples with differently tagged words and return it
    for key in keylist3:
        if dic1[key] != dic2[key]:
            result = (key, dic1[key], dic2[key])
            ret.append(result)
    return ret

#writes results to file
def write_file(things, fileName):
    writeString = ""
    w = open(fileName, "w")

    writeString += "File format:\'Word\' \'STANFORDPOS\' \'NLTKPOS\'\n"
    for tup in things:
        writeString += str(''.join(tup[0])) + " " + str(''.join(tup[1])) + " " + str(''.join(tup[2])) + "\n"
    w.write(writeString)

#main function
def main():
    #maps of words corresponding to POS for each POS tagger
    stanfordMap = dict()
    nltkMap = dict()

    #set paths of the files to read
    stanfordPath = "./data/stanford.txt"
    nltkPath = "./data/nltk.txt"
    
    #build the maps given each output of parsers
    stanfordMap = buildDict(stanfordPath)
    nltkMap = buildDict(nltkPath)

    #do comparisons
    differentPOS = doCompare(stanfordMap, nltkMap)

    #write results to file 'results.txt'
    outputPath = "./results.txt"
    write_file(differentPOS, outputPath)

if __name__ == "__main__":
    main()
