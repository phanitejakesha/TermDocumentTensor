
import csv
import os
import re
import textmining
from tensorly.decomposition import parafac
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

class TermDocumentTensor():
    def __init__(self, directory, type="binary"):
        self.tdt = []
        self.directory = directory
        self.type = type
        
    def create_corpus(self, **kwargs):
        if self.type == "binary":
            return self.create_binary_text_corpus(**kwargs)
        else:
            return self.create_text_corpus(**kwargs)

    def create_text_corpus(self, **kwargs):
        doc_names = os.listdir(self.directory)
        doc_content = [open(os.path.join(self.directory, file)).read() for file in os.listdir(self.directory)]
        # Convert a collection of text documents to a matrix of token counts
        vectorizer = CountVectorizer(**kwargs)
        # Learn the vocabulary dictionary and return term-document matrix.
        x1 = vectorizer.fit_transform(doc_content).toarray()
        vocab = ["vocab"]
        vocab.extend(vectorizer.get_feature_names())
        tdm = [vocab]
        for i in range(len(doc_names)):
            row = [doc_names[i]]
            row.extend(x1[i])
            tdm.append(row)
        return tdm
    
    def create_binary_text_corpus(self, **kwargs):
        doc_content = []
        for file in os.listdir(self.self.directory):
            with open(self.directory + "/" + file, "rb") as file:
                my_string = ""
                while True:
                    byte_hex = file.read(1).hex()
                    if not byte_hex:
                        print(byte_hex)
                        break
                    my_string += byte_hex + " "
            doc_content.append(my_string)
        doc_names = os.listdir(self.directory)

        # Convert a collection of text documents to a matrix of token counts
        vectorizer = CountVectorizer(**kwargs)
        # Learn the vocabulary dictionary and return term-document matrix.
        x1 = vectorizer.fit_transform(doc_content).toarray()
        vocab = ["vocab"]
        vocab.extend(vectorizer.get_feature_names())
        tdm = [vocab]
        for i in range(len(doc_names)):
            row = [doc_names[i]]
            row.extend(x1[i])
            tdm.append(row)
        self.tdt = tdm
        return self.tdt
        
    def convertToCSV(self):
        # Converts a tdm to csv
        with open("test.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            for entry in self.tdt:
                num_list = map(str, entry)
                writer.writerow(num_list)

    def create_term_document_tensor_text(self):
        mydoclist = []
        tdm = textmining.TermDocumentMatrix()
        files = []
        first_occurences_corpus = {}
        text_names = []
        number_files = 0
        for file in os.listdir(self.directory):
            number_files += 1
            first_occurences = {}
            words = 0
            with open(self.directory + "/" + file, "r") as shake:
                files.append(file)
                lines_100 = ""
                for i in range(2):
                    my_line = shake.readline()
                    re.sub(r'\W+', '', my_line)
                    for word in my_line.split():
                        words += 1
                        if word not in first_occurences:
                            first_occurences[word] = words
                    lines_100 += my_line
            first_occurences_corpus[file] = first_occurences
            tdm.add_doc(lines_100)
            mydoclist.append(file)
            text_names.append(file)
        tdm = list(tdm.rows(cutoff=1))
        tdt = [0, 0]
        tdm_first_occurences = []
        # tdm_first_occurences[0] = tdm[0]
        # Create a first occurences matrix that corresponds with the tdm
        for j in range(len(text_names)):
            item = text_names[j]
            this_tdm = []
            for i in range(0, len(tdm[0])):
                word = tdm[0][i]
                try:
                    this_tdm.append(first_occurences_corpus[item][word])
                except:
                    this_tdm.append(0)
            # print(this_tdm)
            tdm_first_occurences.append(this_tdm)
        tdm.pop(0)
        tdt[0] = tdm
        tdt[1] = tdm_first_occurences
        tdt = np.asanyarray(tdt)
        self.tdt = tdt
        return tdt

    def create_ngram_file_tensor(self):
        mydoclist = []
        tdm = textmining.TermDocumentMatrix()
        files = []
        first_occurences_corpus = {}
        text_names = []
        number_files = 0
        for file in os.listdir(self.directory):
            number_files += 1
            first_occurences = {}
            words = 0
            with open(self.directory + "/" + file, "rb") as file:
                my_string = ""
                while True:
                    byte_hex = file.read(1).hex()
                    if not byte_hex:
                        print(byte_hex)
                        break
                    my_string += byte_hex + " "
                tdm.add_doc(my_string)
            break
        tdm = list(tdm.rows(cutoff=1))
        print(tdm)
        print(len(tdm[0]))
                    #print(line)

def main():
    tdt = TermDocumentTensor("zeus_binaries")
    tdt.create_text_corpus(stop_words=None)

main()
