#written by Dylan Desai for CSCE578
import nltk
from nltk import word_tokenize
from nltk import pos_tag

#function to make the pos token output like stanfords "'word'_'pos'"
def clean(tokens):
    ret = list()
    obj = type(tokens)
    sentence = ""
    for token in tokens:
        #seperate the word and its tag
        word = str(''.join(token[0]))
        pos = str(''.join(token[1]))

        #join them together in a sentence and push to result
        new_token = str(word + '_' + pos + ' ')
        if new_token != "._. ":
            sentence += str(new_token)
        else:
            new_token = "._."
            sentence += str(new_token)
            ret.append(sentence)
            sentence = ""
    return ret

def write_file(things, fileName):
    writeString = ""
    w = open(fileName, "w")

    for thing in things:
        writeString += thing + "\n"
    w.write(writeString)

def main():
    #define and get POS tags for the file
    f = open('./data/whitefang.txt')
    text = f.read();
    tokens = word_tokenize(text)
    out = nltk.pos_tag(tokens)

    #clean the output
    clean_out = clean(out)

    #write it to a file
    output_file = './data/nltk.txt';
    write_file(clean_out, output_file)
if __name__ == "__main__":
    main()
