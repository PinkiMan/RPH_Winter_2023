import corpus
import os
import utils
import re


def parseEmail(loadedEmail):
    """
    Remove unwanted characters
    split into header, body, footer
    :returns (str, str, str)
    """
    email_into_lines = loadedEmail.splitlines()

    break_head_body = 0
    for line in email_into_lines:
        break_head_body += 1
        if line == "":
            break

    header = '\n'.join(email_into_lines[:break_head_body])
    body = '\n'.join(email_into_lines[break_head_body:])
    footer = ""

    return header, body, footer

def getAddress(loadedEmail):
    """:returns list()"""
    return re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', loadedEmail)

def getURLs(loadedEmail):
    """:returns list()"""
    return re.findall(r'(https?://[^\s]+)', loadedEmail)

def firstNletters(loadedEmail, n):
    """:returns string"""
    if len(loadedEmail) < n:
        return loadedEmail
    return loadedEmail[0:n]


class MyFilter():
    """ URL blacklists and banned words """

    def __init__(self):
        """
        Create URLs dict
        Create address, company, sender dict
        Create specialWorlds dict
        """
        self.keywords = {}
        self.blacklistedURLs = set()
        self.blockListedAddresses = set()
        self.badBeginings = set()
        self.count = 0
        self.tolerance = 26


    def train(self, path): #learns from mails in path
        classification = utils.read_classification_from_file(path + "/!truth.txt")

        file = corpus.Corpus(path)

        all_spam_urls = set()
        all_ok_urls = set()
        all_spam_addresses = set()
        all_ok_addresses = set()

        self.badBeginings = set()

        for x in file.emails(): #blocklist URL
            urls_in_mail = getURLs(x[1])
            addresses_in_mail = getAddress(x[1])

            if classification[x[0]] == "SPAM":
                parsed = parseEmail(x[1])
                self.badBeginings.add(firstNletters(parsed[1], self.tolerance))
                all_spam_urls = all_spam_urls.union(set(urls_in_mail))
                all_spam_addresses = all_spam_addresses.union(set(addresses_in_mail))
            else:
                all_ok_urls = all_ok_urls.union(set(urls_in_mail))
                all_ok_addresses = all_ok_addresses.union(set(addresses_in_mail))
        self.blacklistedURLs = all_spam_urls - all_ok_urls
        self.blockListedAddresses = all_spam_addresses - all_ok_addresses
        


    def test(self, path): #creates !prediction in path
        file = corpus.Corpus(path)
        dic = {}
        for x in file.emails():
            dic[x[0]] = self.evaluateEmail(parseEmail(x[1]))
        utils.write_classification_to_file(os.path.join(path, "!prediction.txt"), dic)

    def evaluateEmail(self, parsedEmail):
        """
        Evaluate HAM/SPAM
        """

        urls_in_header = getURLs(parsedEmail[0])
        urls_in_body = getURLs(parsedEmail[1])
        urls_in_mail = urls_in_header + urls_in_body

        addresses_in_header = getAddress(parsedEmail[0])
        addresses_in_body = getAddress(parsedEmail[1])
        addresses_in_mail = addresses_in_header + addresses_in_body

        for url in urls_in_mail:
            if url in self.blacklistedURLs:
                return "SPAM"

        for address in addresses_in_mail:
            if address in self.blockListedAddresses:
                return "SPAM"

        for begining in self.badBeginings:
            if len(parsedEmail[1]) < self.tolerance:
                continue
            if begining == parsedEmail[1][0:self.tolerance]:
                return "SPAM"
                
        return "OK"