import os

# Initializing empty dictionaries that will be used for mapping term, document and inverted list
term_termid = {}
dict_termid = {}
dict_documentid = {}
dict_inverted_list = {}

def build_dict():
    """
    Build the above dictionary structures for term, document and inverted list
    """
    term_id_counter = 0
    # open the tokens.txt file in read format
    file = open("tokens.txt", "r")
    for line in file.readlines():
        # get term, document id and freq by splitting string on ','
        term, document_id, freq = line.split(',')

        # if term not present in dictionary add it and map to a unique id
        if term not in dict_termid.keys():
            dict_termid[term] = {'id':term_id_counter, 'doc_freq':0}
            term_id_counter += 1
        # increment freq of that term
        dict_termid[term]['doc_freq'] += 1

        # if document id not present in documentid dictionary, add it with name, id and total number of tokens
        if document_id not in dict_documentid.keys():
            dict_documentid[document_id] = {'name':"'" + str(document_id) + "'", 'token':0}
        dict_documentid[document_id]['token'] += int(freq)
        id = dict_termid[term]['id']

        # if id not present in inverted list dictionary add it with corresponding document id and freq of tokens as list
        if id not in dict_inverted_list.keys():
            dict_inverted_list[id] = []
        dict_inverted_list[id].append([document_id, freq])
    file.close()


def getTermIDFile():
    """
    Writes the output to TermIDFile with term -> term id -> freq of the term in that document
    """
    file = open("TermIDFile.csv", "w")
    for key in dict_termid.keys():
        file.write(str(key) + ','
                + str(dict_termid[key]['id']) + ','
                + str(dict_termid[key]['doc_freq']) + '\n')
    file.close()

def getDocumentIDFile():
    """
    Writes the output to DocumentIDFile with document name -> document id -> total number of tokens
    """
    file = open("DocumentIDFile.csv", "w")
    for key in dict_documentid.keys():
        line = str(key) + ',' + str(dict_documentid[key]['name']) + ',' + str(dict_documentid[key]['token'])
        file.write(line + '\n')
    file.close()

def getInvertedIndex():
    """
    Writes the output to InvertedIndex with id -> document id and freq of tokens as list
    """
    file = open("InvertedIndex.csv", "w")
    for key in dict_inverted_list.keys():
        file.write(str(key) + ',')
        mylist = []
        for items in dict_inverted_list[key]:
            line = ' '.join(x for x in items)
            line = '[' + line.rstrip() + ']'
            mylist.append(line)
        file.write('[' + ' '.join(x for x in mylist) + ']\n')
    file.close()


def getCreateIndexStats():
    """
    First reads the content of output generated already in stats.txt and then computes and writes
    the output of total size of all the input files (in bytes), Total index size, that is total size of the three index
    files (in bytes) and ratio of the index size to the total file size
    """
    folder_path = "crawled_files"
    total_size_of_files = 0

    for file in os.listdir(folder_path):
        total_size_of_files += os.path.getsize(os.path.join(folder_path, file))
    size_of_index_files = os.path.getsize("TermIDFile.csv") + os.path.getsize("DocumentIDFile.csv") + os.path.getsize(
        "InvertedIndex.csv")
    ratio = size_of_index_files / total_size_of_files

    file = open("stats.txt", "r")
    content = file.read()
    file.close()

    file = open("stats.txt", "w")
    file.write("Total size of all the input files (in bytes): " + str(total_size_of_files))
    file.write("\n" + str(content))
    file.write("Total index size, that is total size of the three index files (in bytes): " + str(size_of_index_files))
    file.write("\nRatio of the index size to the total file size: " + str(ratio))
    file.close()


