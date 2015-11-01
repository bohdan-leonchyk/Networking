def parse(file_name):
    with open(file_name) as content:
        new_dict = dict()

        while True:
            file_line = content.readline()
            if not file_line:
                return new_dict
                break
            file_line.split()
            file_line_words = file_line.split()
            try:
                new_dict.update({file_line_words[0]: file_line_words[1]})
            except IndexError:
                pass
