# -*- coding:utf-8 -*-
import os
import re
import codecs
import itertools


from data_utils import create_dico, create_mapping, zero_digits
from data_utils import iob2, iob_iobes, get_seg_features
from loader import load_sentences, update_tag_scheme, tag_mapping


if __name__ == '__main__':
    print(len("中"))
    path = "data/example.train"
    zeros = False

    sentences = []
    sentence = []
    num = 0
    for line in codecs.open(path, 'r', 'utf8'):
        num += 1
        line = zero_digits(line.rstrip()) if zeros else line.rstrip()
        # print(list(line))
        if not line:
            if len(sentence) > 0:
                if 'DOCSTART' not in sentence[0][0]:
                    sentences.append(sentence)
                sentence = []
        else:
            if line[0] == " ":
                line = "$" + line[1:]
                word = line.split()
                # word[0] = " "
                # print(word)
                # break
            else:
                word = line.split()
            # print(word)
            assert len(word) >= 2, print([word[0]])
            sentence.append(word)
        # break
    tag_scheme = "iob"
    for i, s in enumerate(sentences):
        tags = [w[-1] for w in s]
        # Check that tags are given in the IOB format
        if not iob2(tags):
            s_str = '\n'.join(' '.join(w) for w in s)
            raise Exception('Sentences should be given in IOB format! ' +
                            'Please check sentence %i:\n%s' % (i, s_str))
        if tag_scheme == 'iob':
            # If format was IOB1, we convert to IOB2
            for word, new_tag in zip(s, tags):
                word[-1] = new_tag
            break
        elif tag_scheme == 'iobes':
            new_tags = iob_iobes(tags)
            for word, new_tag in zip(s, new_tags):
                word[-1] = new_tag
            break
        else:
            raise Exception('Unknown tagging scheme!')
    lower = True

    tag_dico, _,_ = tag_mapping(sentences)
    print(list(tag_dico.items())[0])