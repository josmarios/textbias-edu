#!/usr/bin/python

import re
import csv
import os


class GenderBiasChecker:

    def __init__(self):
        self.masculine_words = ["active", "adventurous", "aggress", "ambitio", "analy", "assert", "athlet", "autonom",
                                "battle", "boast", "challeng", "champion", "compet", "confident", "courag", "decid",
                                "decision", "decisive", "defend", "determin", "domina", "dominant", "driven",
                                "fearless", "fight", "force", "greedy", "head-strong", "headstrong", "hierarch",
                                "hostil", "impulsive", "independen", "individual", "intellect", "lead", "logic",
                                "objective", "opinion", "outspoken", "persist", "principle", "reckless",
                                "self-confiden", "self-relian", "self-sufficien", "selfconfiden", "selfrelian",
                                "selfsufficien", "stubborn", "superior", "unreasonab"]

        self.feminine_words = ["agree", "affectionate", "child", "cheer", "collab", "commit", "communal", "compassion",
                               "connect", "considerate", "cooperat", "co-operat", "depend", "emotiona", "empath",
                               "feel", "flatterable", "gentle", "honest", "interpersonal", "interdependen",
                               "interpersona", "inter-personal", "inter-dependen", "inter-persona", "kind", "kinship",
                               "loyal", "modesty", "nag", "nurtur", "pleasant", "polite", "quiet", "respon", "sensitiv",
                               "submissive", "support", "sympath", "tender", "together", "trust", "understand", "warm",
                               "whin", "enthusias", "inclusive", "yield", "share", "sharin"]

    def check_bias(self, text):

        female_count = 0
        male_count = 0
        words = re.findall(r'\b\w+\b', text.lower())

        for word in words:
            for masc in self.masculine_words:
                if masc in word:
                    male_count += 1
                    # break

            for fem in self.feminine_words:
                if fem in word:
                    female_count += 1
                    # break
        bias_score = male_count - female_count

        if bias_score == 0:
            bias_classification = 'neutral'
        elif bias_score < -3:
            bias_classification = "strongly feminine-coded"
        elif bias_score < 0:
            bias_classification = "feminine-coded"
        elif bias_score > 3:
            bias_classification = "strongly masculine-coded"
        else:
            bias_classification = "masculine-coded"

        return male_count, female_count, bias_classification

    def check_bias_file(self, filename):

        output_file = filename.replace('.txt', '-gender.csv')
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['text', 'female', 'male', 'num_words', 'bias'])

            with open(filename, 'r') as data:
                for line in data:
                    female_count, male_count, bias = self.check_bias(line)
                    words = line.split()
                    writer.writerow([line.strip(), female_count, male_count, len(words), bias])

    def check_bias_batch(self, in_dir):

        for filename in os.listdir(in_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(in_dir, filename)
                self.check_bias_file(file_path)

    @staticmethod
    def summarize_area(self, dir):

        print('area,female,male,neutral')
        for filename in os.listdir(dir):
            if filename.endswith('-gender.csv'):
                with open(os.path.join(dir, filename), 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)

                    total_bias_m = 0
                    total_bias_f = 0
                    total_neutral = 0
                    for row in reader:
                        if row[4] == 'neutral':
                            total_neutral += 1
                        elif row[4] == 'female':
                            total_bias_f += 1
                        else:
                            total_bias_m += 1

                    area_id = filename.replace('-sample-gender.csv', '')
                    print(f"{area_id},{total_bias_f},{total_bias_m},{total_neutral}")
