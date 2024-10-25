#!/usr/bin/python

import re
import csv
import os


"""
CSV format: category_id, category_name, original_sentence, suggested_sentence, has_bias
"""

sujects = {
    '000': 'Social Sciences',
    '001': 'Natural Sciences',
    '002': 'Math',
    '003': 'Health',
    '004': 'Business',
    '005': 'Education',
    '006': 'Arts',
    '007': 'Law'
}


def get_stats(out_dir, data_output, categories):
    with open(data_output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['category_id', 'category_name', 'original_sentence', 'suggested_sentence', 'has_bias'])
        for filename in os.listdir(out_dir):
            try:
                category_id = filename.replace('output-', '').replace('.txt', '')
                file_path = os.path.join(out_dir, filename)

                with open(file_path, 'r') as f:
                    content = f.read()

                pairs = re.findall(r'(GOLD SEQ:      b)(.*\n*.*)(\nGOLD DIST)', content)
                for item in pairs:
                    pair = list(item)[1]
                    original_sentence = pair.split('\nPRED SEQ:     b')[0].strip()
                    suggested_sentence = pair.split('\nPRED SEQ:     b')[1].strip()
                    has_bias = 'YES' if original_sentence != suggested_sentence else 'NO'
                    category_name = categories.get(category_id, "Unknown")
                    writer.writerow([category_id, category_name, original_sentence, suggested_sentence, has_bias])

            except FileNotFoundError:
                print(f"Error: File not found - {filename}")
            except KeyError as e:
                print(f"Error: Key not found in categories dictionary - {e}")


# get_stats('data/biases-raw/', 'data-final.csv', subjects)

