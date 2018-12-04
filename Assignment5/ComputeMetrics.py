from collections import OrderedDict

QUERY1 = "learn new music instrument"
pool_relevance_query1_result = ['Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes']
pool_relevance_query1_reason = ['Good information about top 15 musical instruments that are easy to learn',
                                'Good description on how to choose a musical instrument to play for beginners',
                                'Talks more about cons when starting to learn a new music instrument but does not mention how to learn a new music instrument or choose one',
                                'Good resources about 10 amazing apps that can help in learning a new musical instrument',
                                'Good information on why to learn a new musical instrument as an adult and how to get started',
                                'Good information on 5 easiest musical instruments for adults and which one to choose',
                                'Good step by step guide on how to learn to play a musical instrument',
                                'Good information about best 10 musical instruments for children to learn',
                                'Good resources available providing different courses to learn various musical instruments',
                                'Good description about 10 easiest musical instruments to learn and how to play',
                                'Talks about impact of playing musical instruments on mind and body but does not mention how to learn to play',
                                'Good information about 30 great resources to learn playing a new musical instrument online']

QUERY2 = "common cold home remedies"
pool_relevance_query2_result = ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']
pool_relevance_query2_reason = ['Good article on 11 cold and flu home remedies',
                                'Good information about common cold home remedies that work and those that do not work',
                                'Good description about 12 natural treatment tips that were home remedies for curing cold and flu',
                                'Good detailed description about everything there is to know about common cold along with home remedies',
                                'Good description about top 10 home remedies for the common cold',
                                'Good description on 10 doctor approved natural cold remedies',
                                'Good information about the popular natural remedies for the common cold',
                                'Good description about the 15 home remedies for common cold and cough',
                                'Good succinct points about home remedies for common cold',
                                'Good description about best 10 home remedies for the common cold',
                                'Good description about remedies and diet for common cold',
                                'Good description about how common cold is spread and home remedies for curing it',
                                'Good description about 16 remedies to cure common cold along with ingredients and how to use them efficiently']

QUERY3 = "tourist attractions in Italy"
pool_relevance_query3_result = ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']
pool_relevance_query3_reason = ['Good description about 15 top rated tourist attractions in Italy',
                                'Good description about 30 top tourist attractions in Italy along with tours and activities',
                                'Good succinct information about top 6 tourist attractions in Italy ',
                                'Good description about 10 best places to visit in Italy along with information about where to stay',
                                'Good key attractions about 10 places to visit in Italy',
                                'Good resources about tours and tickets along with sightseeing that can be done in Italy',
                                'Good succinct information about top 10 tourist attractions in Italy',
                                'Good 2-3 line description about each of the 33 amazing places to visit in Italy along with pictures',
                                'Good snippets with pictures about the top ten tourist attractions in Italy',
                                'Good description along with ranking about the top ten tourist attractions in Italy',
                                'Good description about some of the most most popular tourist attractions in Italy along with its history',
                                'Good description about 25 top tourist attractions specific to just one city Rome but it is still relevant']
# class named as ComputeMetrics
class ComputeMetrics:

    # Initialization of the object
    def __init__(self, max_pool_URLs_from_one_engine, resultant_pool_URLs=OrderedDict()):
        # maximum pool size for URLs to merge from each engine
        self.max_pool_URLs_from_one_engine = max_pool_URLs_from_one_engine
        # resultant pool URLs after deduplication stored as ordered dictionary where key is URL and value is relevance (Yes/No)
        self.resultant_pool_URLs = resultant_pool_URLs


    def get_all_URLs_pool(self, google_file_name, bing_file_name):
        """
        :param google_file_name: name of the Google file where top 15 URLs are extracted for each query
        :param bing_file_name: name of the Bing file where top 15 URLs are extracted for each query
        :return: combined URLs as list
        """
        combined_URLs = []
        self.get_URLs(google_file_name, combined_URLs)
        self.get_URLs(bing_file_name, combined_URLs)
        return combined_URLs

    def get_URLs(self, file_name, combined_URLs):
        """
        Helper method to get all URLs
        :param file_name: name of the file name from where top 8 URLs are to be extracted
        :param combined_URLs: empty URLs list initially which is then appended with the top 8 URLs result
        :return: top 8 URLs result from the given file
        """
        count = 0
        file = open(file_name, "r")
        for URL in file:
            if count == self.max_pool_URLs_from_one_engine:
                break
            count = count + 1
            combined_URLs.append(URL)
        file.close()


    def get_resultant_pool_URLs(self, query_num):
        """
        Method that calls other helper methods to deduplicate combined 30 URLs from Google and Bing
        :param query_num: query number for which this unique resultant pool is populated
        """
        all_URLs_pool = self.get_all_URLs_pool("GoogleTop15Query" + str(query_num) + ".txt",
                                                    "BingTop15Query" + str(query_num) + ".txt")

        if query_num == 1:
            pool_relevance_query_result = pool_relevance_query1_result
        elif query_num == 2:
            pool_relevance_query_result = pool_relevance_query2_result
        else:
            pool_relevance_query_result = pool_relevance_query3_result

        self.populate_unique_URLS_pool_with_relevance_result(all_URLs_pool, pool_relevance_query_result)

        self.write_resultant_pool_URLs("ResultantPoolURLsQuery", query_num)

    def write_resultant_pool_URLs(self, file_name, query_num):
        """
        :param file_name: name of the file to write unique combined pool of URLs from Google and Bing
        :param query_num: query number for which this output is written to a file
        """
        file = open(file_name + str(query_num) + ".txt", "w")
        for URL in self.resultant_pool_URLs:
            file.write(URL)
        file.close()

    def populate_unique_URLS_pool_with_relevance_result(self, all_URLs_pool, pool_relevance_query_result):
        """
        :param all_URLs_pool: list of all unique URLs from Google and Bing
        :param pool_relevance_query_result: relevance result which is to be populated to an ordered dictionary as value
                                            against URL as key
        """
        self.resultant_pool_URLs = OrderedDict()
        index = 0
        for URL in all_URLs_pool:
            if URL in self.resultant_pool_URLs:
                continue
            self.resultant_pool_URLs[URL] = pool_relevance_query_result[index]
            index = index + 1

    def get_relevance_stats(self, file_name, query_num):
        """
        :param file_name: name of the file where relevance table is to be appended, Step 2.2 (c)
        :param query_num: query number for which this relevance table will be appended, Step 2.2 (c)
        """
        file = open(file_name, "a")
        file.write(",Number," + "Result URL," + "Is it relevant?," + "Relevance: Why?" + "\n")
        file.close()
        if query_num == 1:
            pool_relevance_query_reason = pool_relevance_query1_reason
        elif query_num == 2:
            pool_relevance_query_reason = pool_relevance_query2_reason
        else:
            pool_relevance_query_reason = pool_relevance_query3_reason
        self.write_relevance_stats(file_name, pool_relevance_query_reason)

    def write_relevance_stats(self, file_name, pool_relevance_reason_query):
        """
        Helper method to write the generated relevant results in the file table, Step 2.2 (c)
        :param file_name: name of the file where relevance result is to be appended
        :param pool_relevance_reason_query: list containing relevance reason against the URL marked as
                                            Yes(relevant) or No(not relevant)
        """
        number = 1
        index = 0
        file = open(file_name, "a")
        for URL, relevance_result in self.resultant_pool_URLs.items():
            file.write("," + str(number) + "," + str(URL).rstrip() + "," + relevance_result + "," + pool_relevance_reason_query[index] + "\n")
            number = number + 1
            index = index + 1
        file.close()

    def get_relevant_URLs(self, file_name, pool_relevance_query_result):
        """
        :param file_name: Name of the file where pool of unique URLs are to be read from
        :param pool_relevance_query_result: relevance result for each URL in order corresponding to URLs present in the file
        :return: list of relevant URLs
        """
        relevant_URLs = []
        file = open(file_name, "r")
        index = 0
        for URL in file:
            if pool_relevance_query_result[index] == "Yes":
                relevant_URLs.append(URL)
            index = index + 1
        return relevant_URLs

    def get_precision_results(self, relevance_result_query_list):
        """
        A generalized method to compute Precision at rank 5, Precision at rank 8, Precision at rank 12 for Google/Bing
        :param relevance_result_query_list: Relevance score list i.e. Yes (relevant) or No (not relevant) for the
                                            corresponding search engine (Google or Bing)
        :return: Precision at rank 5, Precision at rank 8, Precision at rank 12 for Google/Bing
        """
        P5 = 0
        P8 = 0
        P12 = 0
        relevant_precision_sum = 0
        relevant_running_sum = 0
        retrieved_count = 0
        relevant_retrieved_count = 0

        for relevant_result in relevance_result_query_list:
            retrieved_count = retrieved_count + 1

            if relevant_result == "Yes":
                relevant_running_sum = relevant_running_sum + 1
                if retrieved_count <= 8:
                    relevant_retrieved_count = relevant_retrieved_count + 1
                    relevant_precision_sum = relevant_precision_sum + (relevant_running_sum / retrieved_count)

            if retrieved_count == 5:
                P5 = relevant_running_sum / retrieved_count

            elif retrieved_count == 8:
                P8 = relevant_running_sum / retrieved_count

            elif retrieved_count == 12:
                P12 = relevant_running_sum / retrieved_count

        avg_precision_rank8 = relevant_precision_sum / relevant_retrieved_count

        return P5, P8, P12, avg_precision_rank8

    def get_total_relevant_results(self, pool_relevance_query_result):
        """
        Method that computes the total number of relevant results
        :param pool_relevance_query_result: list of pre-ranked relevance score as "Yes" for relevant and "No" for not relevant
        :return: total number of relevant results
        """
        relevant_results_count = 0
        for result in pool_relevance_query_result:
            if result == "Yes":
                relevant_results_count = relevant_results_count + 1
        return relevant_results_count


    def score_each_engine(self, file_name, query_num):
        """
        Method that stores the precision results and total relevant results by calling the appropriate helper methods
        and then passes those results to generate the output appended to the QueryMetrics.csv file
        :param file_name: name of the resultant pool of unique URLs file for each query
        :param query_num: query number being processed
        """
        if query_num == 1:
            relevant_URLs = self.get_relevant_URLs("ResultantPoolURLsQuery1.txt", pool_relevance_query1_result)
            google_relevance_result_query = self.populate_all_relevance_result("GoogleTop15Query1.txt", relevant_URLs)
            bing_relevance_result_query = self.populate_all_relevance_result("BingTop15Query1.txt", relevant_URLs)
            pool_relevance_query_result = pool_relevance_query1_result
        elif query_num == 2:
            relevant_URLs = self.get_relevant_URLs("ResultantPoolURLsQuery2.txt", pool_relevance_query2_result)
            google_relevance_result_query = self.populate_all_relevance_result("GoogleTop15Query2.txt", relevant_URLs)
            bing_relevance_result_query = self.populate_all_relevance_result("BingTop15Query2.txt", relevant_URLs)
            pool_relevance_query_result = pool_relevance_query2_result
        else:
            relevant_URLs = self.get_relevant_URLs("ResultantPoolURLsQuery3.txt", pool_relevance_query3_result)
            google_relevance_result_query = self.populate_all_relevance_result("GoogleTop15Query3.txt", relevant_URLs)
            bing_relevance_result_query = self.populate_all_relevance_result("BingTop15Query3.txt", relevant_URLs)
            pool_relevance_query_result = pool_relevance_query3_result

        google_P5, google_P8, google_P12, google_avg_precision_rank8 = \
            self.get_precision_results(google_relevance_result_query)

        bing_P5, bing_P8, bing_P12, bing_avg_precision_rank8 = \
            self.get_precision_results(bing_relevance_result_query)

        total_relevant_results = self.get_total_relevant_results(pool_relevance_query_result)

        self.output_score_each_engine_stats(file_name, query_num, google_P5, google_P8, google_P12, google_avg_precision_rank8,
                                       bing_P5, bing_P8, bing_P12, bing_avg_precision_rank8, total_relevant_results)

    def populate_all_relevance_result(self, file_name, relevant_URLs):
        """
        Helper method that builds a list of all revelant results in the top 15 URL file of Google and Bing by checking
        against the pool of unique relevant URL results
        :param file_name: name of the Google or Bing file containing top 15 URLs
        :param relevant_URLs: list of relevant URLs which are in the pool of unique relevant URL results
        :return: list of relevant URLs in the top 15 matched against the pool of unique relevant URL results
        """
        all_relevance_result_list = []
        file = open(file_name, "r")
        for URL in file:
            if URL in relevant_URLs:
                all_relevance_result_list.append("Yes")
            else:
                all_relevance_result_list.append("No")
        return all_relevance_result_list

    def output_score_each_engine_stats(self, file_name, query_num, google_P5, google_P8, google_P12, google_avg_precision_rank8,
                                       bing_P5, bing_P8, bing_P12, bing_avg_precision_rank8, total_relevant_results):
        """
        Method to append the Metrics table, Step 2.4 (g)
        :param file_name: name of the file where output is appended (QueryMetrics.csv)
        :param query_num: query number for which the output is appended to make this method general to support each query result
        :param google_P5: Precision at rank 5 for Google
        :param google_P8: Precision at rank 8 for Google
        :param google_P12: Precision at rank 12 for Google
        :param google_avg_precision_rank8: Average Precision at rank 8 for Google
        :param bing_P5: Precision at rank 5 for Bing
        :param bing_P8: Precision at rank 8 for Bing
        :param bing_P12: Precision at rank 12 for Bing
        :param bing_avg_precision_rank8: Average Precision at rank 8 for Bing
        :param total_relevant_results: total combined relevant results count for Google and Bing
        """
        if query_num == 1:
            query = QUERY1
        elif query_num == 2:
            query = QUERY2
        else:
            query = QUERY3
        duplicates_removed = (self.max_pool_URLs_from_one_engine * 2) - len(self.resultant_pool_URLs)
        file = open(file_name, "a")
        file.write("a., Query:," + query + "\n" +
                   "b., Search engines that you queried:," + "Google & Bing \n" +
                   "c., The number of duplicates removed when results were pooled:," + str(duplicates_removed) + "\n" +
                   "d., The final pool size after duplicates are removed:," + str(len(self.resultant_pool_URLs)) + "\n" +
                   "e., The total number of relevant results:," + str(total_relevant_results) + "\n" +
                   "f., The table with the pooled and deduplicated result URLs along with information about their relevance:" + "\n")
        file.close()
        self.get_relevance_stats(file_name, query_num)
        self.write_precision_metrics(file_name, google_P5, google_P8, google_P12, google_avg_precision_rank8,
                                     bing_P5, bing_P8, bing_P12, bing_avg_precision_rank8)

    def write_precision_metrics(self, file_name, google_P5, google_P8, google_P12, google_avg_precision_rank8,
                                     bing_P5, bing_P8, bing_P12, bing_avg_precision_rank8):
        """
        Helper method to write the precision metrics table, Step 2.4 (g)
        :param file_name: name of the file where Precision metrics table is to be appended (QueryMetrics.csv)
        :param google_P5: Precision at rank 5 for Google
        :param google_P8: Precision at rank 8 for Google
        :param google_P12: Precision at rank 12 for Google
        :param google_avg_precision_rank8: Average Precision at rank 8 for Google
        :param bing_P5: Precision at rank 5 for Bing
        :param bing_P8: Precision at rank 8 for Bing
        :param bing_P12: Precision at rank 12 for Bing
        :param bing_avg_precision_rank8: Average Precision at rank 8 for Bing
        """
        file = open(file_name, "a")
        file.write("g., A table with the metrics computed for the search engines we're evaluating: \n" +
                   ",Metric,"+ "Search Engine 1 = Google," + "Search Engine 2 = Bing \n" +
                   ",Precision at rank 5," + str(google_P5) + "," + str(bing_P5) + "\n" +
                   ",Precision at rank 8," + str(google_P8) + "," + str(bing_P8) + "\n" +
                   ",Precision at rank 12," + str(google_P12) + "," + str(bing_P12) + "\n" +
                   ",Average Precision at rank 8," + str(google_avg_precision_rank8) + "," +
                   str(bing_avg_precision_rank8) + "\n\n\n\n\n")
        file.close()

    def create_output_file(self, file_name):
        """
        :param file_name: name of the file (QueryMetrics.csv) which is initially created for generating all output
                          results and is appended later by different helper methods
        """
        file = open(file_name, "w")
        file.close()

    def get_query_metrics(self, file_name):
        """
        This is the method called from the main program, which in turn calls all the other methods to get the desired
        output for each query from 1 to 3
        :param file_name: name of the output file (QueryMetrics.csv)
        :return:
        """
        self.create_output_file(file_name)
        self.get_resultant_pool_URLs(1)
        self.score_each_engine(file_name, 1)
        self.get_resultant_pool_URLs(2)
        self.score_each_engine(file_name, 2)
        self.get_resultant_pool_URLs(3)
        self.score_each_engine(file_name, 3)


if __name__ == "__main__":
    computeMetrics = ComputeMetrics(8)
    computeMetrics.get_query_metrics("QueryMetrics.csv")

