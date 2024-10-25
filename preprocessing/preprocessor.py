#!/usr/bin/python

import html2text
import nltk
import os
from tqdm import tqdm
from nltk.tag.stanford import StanfordNERTagger
import re
import csv
import random
import string


java_path = "C:\Program Files (x86)\Common Files\Oracle\Java\javapath"
os.environ['JAVAHOME'] = java_path


class TextPreprocessor:
    """Handles initial text cleaning and parsing tasks."""

    @staticmethod
    def parse_html(file):
        with open(file, encoding="utf-8") as f:
            content = html2text.html2text(f.read())
            new_file = file.split('.')[0] + '.txt'

            with open(new_file, 'w', encoding="utf-8") as out:
                out.write(content)
            print('success: ' + file)

    @staticmethod
    def parse_html_batch(in_dir):
        for f in os.listdir(in_dir):
            try:
                TextPreprocessor.parse_html(os.path.join(in_dir, f))
            except:
                print('fail: ' + f)

    @staticmethod
    def anonymize(text):
        st = StanfordNERTagger(r"english.all.3class.distsim.crf.ser.gz",
                               r"stanford-ner.jar",
                               encoding='utf-8')
        tagged_sentence = st.tag(text.split())
        edited_sentence = []
        for word, tag in tagged_sentence:
            if tag != 'PERSON':
                w = word
            else:
                w = 'ANONYMIZED'
            edited_sentence.append(w)
        return ' '.join(edited_sentence)

    @staticmethod
    def remove_multiple_spaces(text):
        if '  ' in text:
            t = text.replace('  ', ' ')
            return TextPreprocessor.remove_multiple_spaces(t)
        else:
            return text
    @staticmethod
    def clean_sentence(text):
        out_text = ''
        text = re.sub(r"http\S+", "", text)  # removes urls
        text = re.sub(r'\S*@\S*\s?', 'EMAIL', text)  # removes e-mail addresses
        text = text.replace('_', ' ').replace('  ', ' ')
        for x in text:  # add space before and after punctuation
            if re.match('[\?\!,\.:\';]', x):
                xx = ' ' + x + ' '
                xx.replace('  ', ' ')
            elif re.match('[a-zA-Z1-9 ]', x):
                xx = x
            else:
                continue

            out_text += xx
        out = out_text.lower()
        return re.sub('  ', ' ', out)

class SentenceExtractor:
    """Focuses on extracting and formatting sentences from text."""

    @staticmethod
    def extract_sentences(src_name, dst_name):
        content = []
        with open(src_name, encoding="utf8") as f:
            lines = f.readlines()
            for l in lines:
                if '#' in l: continue  # Ignores titles
                temp1 = re.sub("\*\*.*?\*\*", "", l) \
                    .replace(' : ', '').replace('_', '')
                temp2 = re.sub("[\(\{\[].*?[\)\}\]]", "", temp1).replace('- END OF TRANSCRIPT -', '')
                content.append(temp2)
        text = ' '.join(content)
        txt = TextPreprocessor.remove_multiple_spaces(text.replace('\n', ' '))

        with open(dst_name, 'w', encoding="utf8") as dst_file:
            data = nltk.tokenize.sent_tokenize(txt)
            temp = [re.sub("[\(\{\[].*?[\)\}\]]", "", s) for s in data]
            data2 = [s for s in temp if len(s.split(' ')) > 2]
            for sent in data2:
                cnt = TextPreprocessor.remove_multiple_spaces(sent) + '\n'
                dst_file.write(cnt.replace('\n ', '\n'))

    @staticmethod
    def extract_sentences_batch(input_dir, output_dir):
        for f in tqdm(os.listdir(input_dir)):
            if '.txt' in f:
                src = os.path.join(output_dir, f)
                dst = os.path.join(output_dir, f.replace('.txt', '-sent.txt'))
                SentenceExtractor.extract_sentences(src, dst)

    @staticmethod
    def format_input(src_dir):
        for f in tqdm(os.listdir(src_dir)):
            out_file = src_dir + f.replace('.txt', '-formatted.txt')
            with open(src_dir + f, encoding='utf8') as file:
                lines = file.readlines()
                out_lines = []
                i = 1
                for l in lines:
                    text = ''.join([x for x in l if x in string.printable])
                    text = TextPreprocessor.clean_sentence(text)
                    text = text.replace('\n', ' ').replace('\t', ' ')
                    new_line = (src_dir + f + str(i)) + '\t' + ((text + '\t') * 4) + '\n'
                    new_line = new_line.replace('\t\n', '\n')  # Removes last tab
                    out_lines.append(new_line)
                    i += 1
                with open(out_file, 'w') as out:
                    out.writelines(out_lines)


class DataOrganizer:
    """Deals with data categorization, merging, and sampling."""

    @staticmethod
    def get_modules_by_category(file):
        categories = {}
        with open(file) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader, None)
            subjects = []
            for row in reader:
                subjects.append(row[4])

            subjects = set(subjects)

            for s in subjects:
                categories[s] = []

        with open(file) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader, None)
            for r in reader:
                key = r[4]
                value = r[1]
                categories[key].append(value)
            return categories

    @staticmethod
    def merge_modules_by_subject(dictionary, data_dir, out_dir):
        for k in tqdm(dictionary):
            content = ''
            if len(dictionary[k]) > 2:
                for module in dictionary[k]:
                    sentences_file = data_dir + module + '-sent.txt'
                    if os.path.isfile(sentences_file):
                        with open(sentences_file, encoding='utf8') as f:
                            content+= f.read()
                out_file = k + '.txt'

                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)

                with open(out_dir+out_file, 'w', encoding='utf8') as ff:
                    ff.write(content)

    @staticmethod
    def get_samples(src_dir):
        for area in os.listdir(src_dir):
            with open(src_dir+area, encoding='utf8') as f:
                lines = f.readlines()
                random.shuffle(lines)
                sample = random.sample(lines, 1000)
                with open(src_dir + area.replace('.txt', '-sample.txt'), 'w', encoding='utf8') as out:
                    out.writelines(sample)

