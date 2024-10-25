from bardapi import Bard
import pandas as pd


class BardBiasClassifier:
    def __init__(self, token, max_tokens=1000, temperature=0.7):

        self.bard = Bard(token=token)
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.prompt_base = """
        Identify potential bias in the sentences provided below. A sentence is considered ‘biased' if it shows inclination against a particular group or individual based on social characteristics like gender, ethnic origin, economic background, etc. Provide your answers in a 3-column table with (i) the sentence index; (ii) a ‘YES' label for biased sentences or ‘NO' for unbiased sentences; and (iii) a brief explanation to support your answer.

        Sentences:
        """

    def classify_sentences(self, sentences):
        prompt = self.prompt_base + "\n".join([f"{i + 1}. {sentence}" for i, sentence in enumerate(sentences)])

        response = self.bard.get_answer(prompt)['content']

        result_table = [line.split("|") for line in response.strip().split("\n") if "|" in line]
        results = []
        for row in result_table:
            try:
                results.append(
                    {"sentence_index": int(row[0].strip()), "bias": row[1].strip(), "explanation": row[2].strip()})
            except (IndexError, ValueError):
                print(f"Warning: Unexpected response format for sentence: {row}")

        return results

    def classify_from_csv(self, file_path, batch_size=50):

        df = pd.read_csv(file_path)
        all_results = []
        for i in range(0, len(df), batch_size):
            batch = df['sentences'][i:i + batch_size].tolist()
            results = self.classify_sentences(batch)
            all_results.extend(results)
        return all_results
