import numpy as np
import math
import UseIndex
import ast
import re
import heapq

useIndex = UseIndex.UseIndex()
IndexFolderPath = "IndexFolder"
CONTENT_PATTERN = "<p>.*?</p>"
N = 900

class RunRankedRetrieval:
    # Initialization of the object
    def __init__(self, IndexFolderName, ContentFolderName, QueryFileName, K):
        # default index folder name
        self.IndexFolderName = IndexFolderName
        # default content folder name
        self.ContentFolderName = ContentFolderName
        # default query file name
        self.QueryFileName = QueryFileName
        # default number of results to return for each query
        self.K = K

    def get_snippet(self, crawled_page_content):
        """
        :param crawled_page_content
        :return: snippet to output using regex pattern matcher
        """
        return re.findall(CONTENT_PATTERN, crawled_page_content)[:1]


    def get_total_tokens(self, matched_id_name):
        """
        :param matched_id_name of the document
        :return: corresponding total number of tokens
        """
        doc_id = str(matched_id_name)
        file = open(IndexFolderPath + "/DocumentIDFile.csv", "r")
        for line in file.readlines():
            line = line.split(',')
            if line[0] == doc_id:
                return line[2]
        file.close()

    def deserialize_as_list(self, line):
        """
        :param line of any file as string
        :return: deserialize list
        """
        return ast.literal_eval(line)


    def normalize_2d_matrix(self, matrix_2d, matched_id_names):
        """
        :param matrix_2d: 2 dimensional matrix to normalize the result
        :param matched_id_name of the document
        :return: 2d matrix with result normalized
        """
        for index in range(len(matched_id_names)):
            matrix_2d[:, index] = matrix_2d[:, index] / math.sqrt(sum(x ** 2 for x in matrix_2d[:, index]))
        return matrix_2d

    def get_posting(self, transformed_queries):
        """
        :param transformed_queries derived from input raw queries
        :return: map of posting of term to inverted list of matching that term
        """
        posting = {}
        for transformed_query in transformed_queries:
            posting[transformed_query] = self.format_list(useIndex.getInvertedList(str(useIndex.getTermID(transformed_query))))
        return posting

    def compute_dft(self, posting):
        """
        :param posting
        :return dft map
        """
        dft_map = {}
        for key, values in posting.items():
            dft_map[key] = len(posting[key])
        return dft_map

    def get_matched_id_names(self, posting):
        """
        :param posting
        :return: matched document ids as list
        """
        matched_id = set()
        for key, values in posting.items():
            for value in values:
                matched_id.add(value[0])
        return list(matched_id)

    def format_list(self, input):
        """
        :param input: string
        :return: list of list formatted with comma separated for ease in computation
        """
        list = []
        list_of_list = []
        input = input.replace("[", "").replace("]", "").split(" ")
        curr_index = 0
        max_index = 0
        while curr_index < len(input):
            list.append(int(input[curr_index]))
            curr_index += 1
            max_index += 1
            if max_index is 2:
                max_index = 0
                list_of_list.append(list)
                list = []
        return list_of_list

    def populate_query_cosine(self, posting, dft_map):
        """
        :param posting
        :param dft_map
        :return: cosine scores of all words in a query
        """
        query_cosine = np.zeros(len(posting), dtype=np.float64)
        curr_index = 0
        for query in posting:
            query_cosine[curr_index] = math.log10(1 + 1 / len(posting)) * math.log10(N / dft_map[query])
            curr_index += 1
        return query_cosine

    def populate_matrix_2d(self, posting, matched_id_names, dft_map, id_total_tokens):
        """
        :param posting: map
        :param matched_id_names: list of matched document ids
        :param dft_map: map
        :param id_total_tokens: document id corresponding with total tokens
        :return: 2d matrix with results of computation
        """
        query_cosine = np.zeros((len(posting), len(matched_id_names)), dtype=np.float64)
        curr_index = 0
        for key, values in posting.items():
            for value in values:
                if value[0] in matched_id_names:
                    query_cosine[curr_index][matched_id_names.index(value[0])] = self.compute_formula(value, id_total_tokens) * math.log10(N / dft_map[key])
            curr_index += 1
        return query_cosine

    def compute_formula(self, value, id_total_tokens):
        return math.log10(1 + int(value[1]) / int(id_total_tokens[value[0]]))

    def sort(self, query_cosine, matrix_2d, matched_id_names):
        """
        :param query_cosine
        :param matrix_2d
        :param matched_id_names
        :return: top k cosine similarity score between the document and the current query in descending order
        """
        cosine = {}
        for index in range(len(matched_id_names)):
            score = 0
            for wtd, wtq in zip(query_cosine, matrix_2d[:, index]):
                score += wtd * wtq
            cosine[matched_id_names[index]] = score
        top_k_desc = sorted(cosine.items(), key=lambda x: x[1])[::-1][:self.K]
        return top_k_desc

    def get_query_results(self, transformed_queries):
        """
        :param transformed_queries: derived from raw query which was input
        :return: cosine score of all the words in quert, 2d matrix computed and matched id names of documents
        """
        posting = self.get_posting(transformed_queries)
        dft_map = self.compute_dft(posting)
        matched_id_names = self.get_matched_id_names(posting)
        id_total_tokens = {}
        for matched_id_name in matched_id_names:
            id_total_tokens[matched_id_name] = self.get_total_tokens(matched_id_name)
        matrix_2d = self.populate_matrix_2d(posting, matched_id_names, dft_map, id_total_tokens)
        query_cosine = self.populate_query_cosine(posting, dft_map)
        # "|A intersection B| / sqrt|A union B|"
        query_cosine = query_cosine / math.sqrt(sum(x ** 2 for x in query_cosine))
        matrix_2d = self.normalize_2d_matrix(matrix_2d, matched_id_names)
        return query_cosine, matrix_2d, matched_id_names


    def get_query_outputs(self):
        """
        :return: writes the raw query in first line followed by transformed query as stated in requirement
        """
        transormed_queries = []
        raw_queries = []
        file = open(self.QueryFileName, "r")
        for line in file.readlines():
            line = line.strip("\n")
            raw_queries.append(line)
            line_splitted = line.split(" ")
            transormed_queries.append(line_splitted)
        file.close()
        return raw_queries, transormed_queries

    def write_content_stats(self, top_k_desc, output_file):
        """
        :param top_k_desc: top k descending query cosine score results with document name
        :param output_file: file name to output result ("Queries.txt")
        """
        for matched_id_name, cosine in top_k_desc:
            if len(ContentFolderName) != 0:
                content_file = open("crawled_files" + '/' + str(matched_id_name) + '.txt', "r")
                crawled_page_content = content_file.read()
                snippet = self.get_snippet(crawled_page_content)
            output_file.write("\n" + str(matched_id_name) + "\t\t" + str(useIndex.getDocumentName(matched_id_name)) + ".txt" + "\n")
            if len(ContentFolderName) != 0:
                output_file.write(snippet[0][:200])
            output_file.write("\nCosine:" + str(cosine) + "\n")
            if len(ContentFolderName) != 0:
                content_file.close()

    def populate_result(self, output_file, transformed_query, query_cosine):
        """
        :param output_file: file name to output result ("Queries.txt")
        :param transformed_query: derived from raw query
        :param query_cosine: cosine score of queries
        """
        query_cosine_map = {}
        output_file.write("\n")
        for curr_index in range(len(transformed_query)):
            query_cosine_map[transformed_query[curr_index]] = query_cosine[curr_index]
        for key, value in query_cosine_map.items():
            output_file.write(str(key) + ": " + str(value) + "; ")
        output_file.write("\n\n\n\n")



    def get_ranked_retrieval(self, output_file_name):
        """
        :param output_file_name: file name to output result ("Queries.txt") and calls all other methods
               to write the result
        """
        output_file = open(output_file_name, "w")
        raw_queries, transformed_queries = self.get_query_outputs()
        for raw_query, transformed_query in zip(raw_queries, transformed_queries):
            query_cosine, matrix_2d, matched_id_names = self.get_query_results(transformed_query)
            top_k_desc = self.sort(query_cosine, matrix_2d, matched_id_names)
            output_file.write(raw_query + "\n")
            output_file.write(str(transformed_query) + "\n")
            self.write_content_stats(top_k_desc, output_file)
            self.populate_result(output_file, transformed_query, query_cosine)
        output_file.close()

if __name__ == "__main__":
    IndexFolderName = (input("Please enter the index folder name: "))
    if IndexFolderName is not "IndexFolder":
        IndexFolderName = "IndexFolder"
    ContentFolderName = (input("Please enter the content folder name or press enter to skip: "))
    if len(ContentFolderName) == 0:
        ContentFolderName = ""
    elif ContentFolderName is not "crawled_pages":
        ContentFolderName = "crawled_pages"
    QueryFileName = "Query.txt"
    K = (int(input("Please enter the maximum number of results to return for each query (K): ")))
    if K is None:
        K = 5
    runRankedRetrieval = RunRankedRetrieval(IndexFolderName, ContentFolderName, QueryFileName, K)
    runRankedRetrieval.get_ranked_retrieval("Output.txt")