## Overview

This repository contains the code related to the article "[From hype to evidence: exploring large language models for inter-group bias classification in higher education](https://www.tandfonline.com/doi/full/10.1080/10494820.2024.2408554)". 

## Citing
- APA
  
  ```
  Albuquerque, J., Rienties, B., Holmes, W., & Hlosta, M. (2024). From hype to evidence: exploring large language models for inter-group bias classification in higher education. Interactive Learning Environments, 1–23. https://doi.org/10.1080/10494820.2024.2408554
  ```

- Bibtex

```bibtex
@article{albuquerque2024from,
        author = {Josmario Albuquerque, Bart Rienties, Wayne Holmes and Martin Hlosta},
        title = {From hype to evidence: exploring large language models for inter-group bias classification in higher education},
        journal = {Interactive Learning Environments},
        volume = {0},
        number = {0},
        pages = {1--23},
        year = {2024},
        publisher = {Routledge},
        doi = {10.1080/10494820.2024.2408554},
        URL = {https://doi.org/10.1080/10494820.2024.2408554)}
}

```



## Project Structure

```
├── preprocessing          # Text preprocessing modules
├── classification         # Contains bias classification modules (Bard, BERT, Gender, GPT)
├── main.py                # Main script for running the tool
└── requirements.txt       # List of Python dependencies
```

## Requirements

```bash
$ pip install -r requirements.txt
$ python -m nltk.downloader punkt averaged_perceptron_tagger
```

## Pre-processing

- **Parsing HTML files to plain text (*.txt)**
  ```bash
  $ python main.py parse "input_dir/"
  ```

  Where `input_dir/` is the directory containing the HTML files.

- **Extracting sentences from text files**
  ```bash
  $ python main.py extract "input_dir/"
  ```

  Where `input_dir/` is the directory containing the text files (plain text). Output files will be saved in the same directory, with one sentence per line.

- **Anonymizing text**
  ```bash
  $ python main.py anonymize "Bob is working from home."
  ```

  Output:

  ```
  ANONYMIZED is working from home.
  ```

## Bias Classification

- **ChatGPT**
  ```bash
  $ python main.py gpt -t "text to be checked" -k OPENAI_API_KEY
  ```
  (or)
  ```bash
  $ python main.py gpt -b "input_dir/" -k OPENAI_API_KEY
  ```

  Where `input_dir/` is the directory containing text files (plain text) to be checked for bias using GPT 3.5-Turbo.

---

- **Bard**  
  ```bash
  $ python main.py bard -t "text to be checked" -k BARD_TOKEN 
  ```
  (or)
  ```bash
  $ python main.py bard -b "input_dir/" -k BARD_TOKEN
  ```

  Where `input_dir/` is the directory containing text files (plain text) to be checked for bias using Bard.

---

- **BERT**
  - Please, refer to [this repository](https://github.com/rpryzant/neutralizing-bias) for more details.

---

- **Gender Bias**
  ```bash
  $ python main.py gender -t "text to be checked"
  ```

  (or)

  ```bash
  $ python main.py gender -b "input_dir/"
  ```

  Where `input_dir/` is the directory containing the text files being checked for potential gender bias.\  
\
  **Output Format** (for Gender Classification): A CSV file containing the following columns:
  
  ```
  text, female, male, num_words, bias
  ```
  
  Where:
  * `text` is the input text.
    * `female` and `male` correspond to the number of words considered biased towards each gender.
    * `num_words` is the total number of words analyzed.
    * `bias` is one of the following strings: `male`, `female`, `neutral`.
