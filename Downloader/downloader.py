class Downloader(object):
    def __init__(self):
        self.url = None
        self.file_name = None

    def start(self):
        import os
        import sys
        import urllib2

        if len(sys.argv) == 1:
            print('Usage: {} [url]'.format(sys.argv[0]))
        else:
            try:
                self.url = sys.argv[1]
                if self.url_validator():
                    self.file_name = os.path.basename(self.url)
                    content = open(self.file_name, 'wb')
                    content_size = self.calculate_size(self.url)
                    response = urllib2.urlopen(self.url).read(content_size)
                    content.write(response)
                    content.close()
                else:
                    print('Incorrect content location')
            except IOError:
                print('No such file or directory')

    def url_validator(self):
        from urlparse import urlparse

        splitted_url = urlparse(self.url)
        for i in range(0, 3):
            if splitted_url[i] == '':
                return False
        return True

    @staticmethod
    def calculate_size(url):
        import urllib

        data = urllib.urlopen(url).headers
        return int(data['Content-length'])

if __name__ == '__main__':
    download = Downloader()
    download.start()
