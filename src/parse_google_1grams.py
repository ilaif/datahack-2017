import glob
import pickle
Z_PATH = r"C:\Users\user\Desktop\datahack2017\google_books\googlebooks-eng-all-1gram-20120701-z"
all_paths = glob.glob(r"C:\Users\user\Desktop\datahack2017\google_books\googlebooks-eng-all-1gram-20120701-*")
print all_paths

"""
def parse_google_file(path):
    lines = file(path,'rb').read().splitlines()
    lines = [x.split('\t') for x in lines]
    lines = [x for x in lines if len(x) == 4]
    words_and_counts = [(x[0].split('_')[0], int(x[2])) for x in lines]
    res = {}
    for w, curr_count in words_and_counts:
        w = w.lower()
        count = res.get(w, 0)
        count += curr_count
        res[w] = count
    return res
"""

LEGIT_LETTERS = set("abcdefghijklmnopqrstuvwxyz'.")
def is_legit_word(w):
    return all([x in LEGIT_LETTERS for  x in w])

def parse_google_file(path):
    f = file(path, 'rb')
    line = "not empty"
    res = {}
    count_line = 0
    while True:
        line = f.readline().strip()
        if not line:
            break
        line = line.split('\t')
        if len(line) != 4:
            continue
        w, curr_count = (line[0].split('_')[0].lower(), int(line[2]))
        res[w] = res.get(w, 0) + curr_count
        if count_line % 1000000 == 0:
            print count_line
        count_line += 1
    real_res = {x : y for x,y in res.iteritems() if is_legit_word(x)}
    print "done parsing", path
    return res


def get_all_word_counts():
    all_words = {}
    for path in all_paths:
        print path
        parsed_letter = parse_google_file(path)
        all_words.update(parsed_letter)

    pickle.dump(all_words, file(r"C:\Users\user\Desktop\datahack2017\google_books\res.pickle", 'wb'))
    return all_words

all_words = get_all_word_counts()