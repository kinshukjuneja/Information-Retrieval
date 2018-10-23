import re
from sys import argv, getsizeof
import os
import CreateIndex

# get the present working directory
pwd = os.path.join(os.getcwd())

# regex to get the body content of the document
BODY_PATTERN = "<body.*?>(.*)<\/body>"

# regex to get all the words and numbers in the body
WORD_PATTERN = ">(?!<)(.*?)<"

# regex to filter out the words and numbers based on rules defined
TOKEN_PATTERN = "(\w+\.?)+"

# class named as RunDataTransformer
class RunDataTransformer:

    # Initialization of the object
    def __init__(self, FolderName, NumFilesToProcess):
        # default folder name
        self.FolderName = FolderName
        # default number of files to process
        self.NumFilesToProcess = NumFilesToProcess

    def dict_tokens(self, tokens, file_id):
        """
        :param tokens: as a list
        :param file_id: current file as int that is being process
        :return: a dictionary that computes the frequency with corresponding file id
        """
        dict = {}
        for token in tokens:
            if token not in dict.keys():
                dict[token] = {'count':0, 'file_id':file_id}
            dict[token]['count'] += 1
        return dict

    def getTokens(self):
        """
        Function to compute the tokens file by using regex to filter out tokens
        with corresponding file id and frequency
        """
        filewise_tokens = []
        total_file_size = 0
        total_tokens = 0
        total_tokens_list = []

        for file_id in range(1, self.NumFilesToProcess + 1):
            # path to process files
            path = os.path.join(self.FolderName, str(file_id) + '.txt')
            file = open(path, 'r')
            document = file.read()

            # compute total size of the file
            total_file_size += getsizeof(document)

            # regex to get the body content from the document
            body_content = re.findall(BODY_PATTERN, document)
            # convert the body content to a string to apply regex again
            body_content = ' '.join(body_content)

             # regex to get all the words and numbers in body content
            words_in_body = re.findall(WORD_PATTERN, body_content)
            # convert the words content to a string to apply regex again
            words_in_body = ' '.join(words_in_body)

            # regex to get all the tokens based on rules defined in assignment
            curr_token_list = re.findall(TOKEN_PATTERN, words_in_body)
            total_tokens_list.extend(curr_token_list)

            # compute the total length of tokens
            total_tokens += len(curr_token_list)
            filewise_tokens.append(self.dict_tokens(curr_token_list, file_id))
            file.close()

        # compute all the unique tokens using set data structure
        total_unique_tokens = set(total_tokens_list)

        # write the tokens to output using token term -> file_id -> frequency
        file = open("tokens.txt", "w")
        for dictionary in filewise_tokens:
            for token in dictionary.keys():
                msg = token + ',' \
                      + str(dictionary[token]['file_id']) + ',' \
                      + str(dictionary[token]['count']) \
                      + '\n'
                file.write(msg)
        file.close()

        # compute the stats by writing out the output to stats.txt file
        self.getStats("stats.txt", total_tokens, total_unique_tokens)


    def getStats(self, file_name, total_tokens, total_unique_tokens):
        """
        :param file_name: name of the file: "stats.txt"
        :param total_tokens: total number of tokens to write in output
        :param total_unique_tokens: total number of unique tokens to write in out
        :return: writes an output file into the file name specified as first argument
        """
        file = open(file_name, "w")
        file.write("Total number of tokens across all input files: " + str(total_tokens) + "\n")
        file.write("Total number of unique tokens across all input files: " + str(len(total_unique_tokens)) + "\n")
        file.close()


if __name__ == "__main__":
    FolderName = (input("Please enter the folder name: "))

    if FolderName != "crawled_files":
        FolderName = ""

    NumFilesToProcess = (int(input("Please enter number of files to process: ")))

    runDataTransformer = RunDataTransformer(FolderName, NumFilesToProcess)

    runDataTransformer.getTokens()

    createIndex = CreateIndex

    createIndex.build_dict()

    createIndex.getTermIDFile()

    createIndex.getDocumentIDFile()

    createIndex.getInvertedIndex()

    createIndex.getCreateIndexStats()
