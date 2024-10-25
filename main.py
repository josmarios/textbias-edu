#!/usr/bin/python

import argparse
from classification.gender import GenderBiasChecker
from preprocessing.preprocessor import TextPreprocessor, SentenceExtractor
from classification.gpt import GPTBiasClassifier
from classification.bard import BardBiasClassifier


def main():
    parser = argparse.ArgumentParser(description="Text preprocessing and bias classification tool.")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for gender bias checking
    gender_parser = subparsers.add_parser("gender", help="Check gender bias in text.")
    gender_parser.add_argument("-t", "--text", type=str, help="Text to analyze for gender bias.")
    gender_parser.add_argument("-b", "--batch", type=str, help="Directory containing files to analyze.")

    # Subparser for anonymizing text
    anonymize_parser = subparsers.add_parser("anonymize", help="Anonymize text.")
    anonymize_parser.add_argument("text", type=str, help="Text to anonymize.")

    # Subparser for parsing HTML
    parse_parser = subparsers.add_parser("parse", help="Parse HTML to text.")
    parse_parser.add_argument("directory", type=str, help="Directory containing HTML files to parse.")

    # Subparser for extracting sentences
    extract_parser = subparsers.add_parser("extract", help="Extract sentences from text files.")
    extract_parser.add_argument("directory", type=str, help="Directory containing text files.")

    # Subparsers for GPT and Bard bias classification (similar to gender bias)
    gpt_parser = subparsers.add_parser("gpt", help="Check bias using GPT.")
    gpt_parser.add_argument("-t", "--text", type=str, help="Text to analyze for bias using GPT.")
    gpt_parser.add_argument("-b", "--batch", type=str, help="Directory containing files to analyze using GPT.")
    gpt_parser.add_argument("-k", "--api_key", type=str, help="Your OpenAI API key.", required=True)

    bard_parser = subparsers.add_parser("bard", help="Check bias using Bard.")
    bard_parser.add_argument("-t", "--text", type=str, help="Text to analyze for bias using Bard.")
    bard_parser.add_argument("-b", "--batch", type=str, help="Directory containing files to analyze using Bard.")
    bard_parser.add_argument("-k", "--api_key", type=str, help="Your Google Bard token.", required=True)

    args = parser.parse_args()

    if args.command == "gender":
        gbc = GenderBiasChecker()
        if args.text:
            a, b, c = gbc.check_bias(args.text)
            print("Result: {}\nMasculine: {}\nFeminine: {}".format(c, a, b))
        elif args.batch:
            gbc.check_bias_batch(args.batch)
        else:
            gender_parser.print_help()
    elif args.command == "anonymize":
        print(TextPreprocessor.anonymize(args.text))
    elif args.command == "parse":
        TextPreprocessor.parse_html_batch(args.directory)
    elif args.command == "extract":
        SentenceExtractor.extract_sentences_batch(args.directory)
    elif args.command == "gpt":
        gpt_classifier = GPTBiasClassifier(api_key=args.api_key)
        if args.text:
            results = gpt_classifier.classify_sentences([args.text])
            for result in results:
                print(result)
        elif args.batch:
            results = gpt_classifier.classify_from_csv(args.batch)
            for result in results:
                print(result)
        else:
            gpt_parser.print_help()
    elif args.command == "bard":
        bard_classifier = BardBiasClassifier(token=args.api_key)
        if args.text:
            results = bard_classifier.classify_sentences([args.text])
            for result in results:
                print(result)
        elif args.batch:
            results = bard_classifier.classify_from_csv(args.batch)
            for result in results:
                print(result)
        else:
            bard_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

