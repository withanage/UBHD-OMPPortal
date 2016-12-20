__author__ = "Nils Weiher, Dulip Withanage"


from gluon.contrib.webclient import WebClient
import os, json, sys



class IntegrationTests:
    def __init__(self):
        self.web_application = myconf.take("web.application")
        self.web_url = myconf.take("web.url")
        self.config = self.read_json("applications/" + self.web_application + "/static/tests/heibooks.json")

    def get_host(self, url):
        return url.split('//')[-1]


    def read_json(self, f):
        if os.path.isfile(f):
            print f
            with open(f) as j:
                return json.load(j)
        else:
            sys.exit(1)


    def run(self):
        tests = self.config.get("tests")
        if tests:
            # Sort tests by key
            for t in tests:
                self.run_test(t, tests[t])


    def run_test(self, test_num, test):
        print "num: " + test_num, test
        url_parts = [self.web_url, self.web_application, test.get('controller')]

        request_url = test.get('function')
        for arg in test.get('arguments'):
            url_parts.append(arg)
        url = self.make_w2py_url(test)
        print "RUN TEST FOR url=" + url
        try:
            client = WebClient(url, postbacks=True)
            client.get("")
        except Exception as e:
            print e
            print "Test failed!"
        print client.text
        print client.status

    def make_w2py_url(self, test):
        url = URL(c=test.get('controller'), f=str(test.get('function')), args=test.get('arguments'),
                  vars=test.get('vars'),
                  host=self.get_host(self.web_url))
        return url


def main():
    it = IntegrationTests()
    it.run()


main()


