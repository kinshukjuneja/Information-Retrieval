import re

class UseIndex:

    def getTermID(self, term):
        """
        param: term
        return: the corresponding TermID
        """
        term  = str(term)
        file = open("IndexFolder/TermIDFile.csv", "r")
        for line in file.readlines():
            line = line.split(',')
            if line[0] == term:
                return line[1]
        file.close()

    def getInvertedList(self, term_id):
        """
        param: term id
        return: it's inverted list
        """
        term_id = str(term_id)
        file = open("IndexFolder/InvertedIndex.csv", "r")
        for line in file.readlines():
            line = line.split(',')
            if line[0] == term_id:
                return line[1]
        file.close()

    def getDocumentIDList(self, term):
        """
        param: term
        return: takes a term, find the TermID and the corresponding inverted list,
                and return the DocumentIDs where this term occurs
        """
        term = str(term)
        term_id = self.getTermID(term)
        inverted_list = self.getInvertedList(term_id)
        inverted_list = re.findall('''\d+ \d+''', inverted_list)
        document_ids = []
        for item in inverted_list:
            document_ids.append(item.split(' ')[0])
        return document_ids

    def getDocumentName(self, doc_id):
        """
        param: document id
        return: takes a DocumentID and returns the document name it corresponds to
        """
        doc_id = str(doc_id)
        file = open("IndexFolder/DocumentIDFile.csv", "r")
        for line in file.readlines():
            line = line.split(',')
            if line[0] == doc_id:
                return line[1]
        file.close()

if __name__ == "__main__":
    useIndex = UseIndex()

    term = (input("Please enter the Term to get it's corresponding Term ID (example: National): "))
    print(useIndex.getTermID(term))

    term_id = (input("\nPlease enter the Term ID to get the Inverted List (example: 2): "))
    print(useIndex.getInvertedList(term_id))

    term = (input("Please enter the Term to get the Document IDs where this term occurs (example: park): "))
    print(useIndex.getDocumentIDList(term))

    doc_id = (input("\nPlease enter the Document ID to get it's corresponding document name (example: 56): "))
    print(useIndex.getDocumentName(doc_id))