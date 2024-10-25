from openai import OpenAI
import pandas as pd


class GPTBiasClassifier:
    def __init__(self, api_key, max_tokens=2048, temperature=0.7, model="gpt-3.5-turbo"):
        """
        Initializes the ChatGPTBiasClassifier.

        Args:
            api_key (str): OpenAI API key.
            max_tokens (int, optional): Maximum tokens in the generated response. Defaults to 2048.
            temperature (float, optional): Controls randomness of output. Defaults to 0.7.
            model (str, optional): The ChatGPT model to use. Defaults to "gpt-3.5-turbo".
        """
        self.client = OpenAI(api_key=api_key)
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = model
        self.prompt_base = """
        Identify potential bias in the sentences provided below. A sentence is considered ‘biased' if it shows inclination against a particular group or individual based on social characteristics like gender, ethnic origin, economic background, etc. Provide your answers in a 3-column table with (i) the sentence index; (ii) a ‘YES' label for biased sentences or ‘NO' for unbiased sentences; and (iii) a brief explanation to support your answer.

        Sentences:
        """

    def classify_sentences(self, sentences):
        """
        Classifies sentences for bias using ChatGPT.

        Args:
            sentences (list): A list of sentences to classify.

        Returns:
            list: A list of dictionaries, each containing the sentence index, bias label, and explanation.
        """
        prompt = self.prompt_base + "\n".join([f"{i + 1}. {sentence}" for i, sentence in enumerate(sentences)])

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        # Extract and process the response
        result_text = response["choices"][0]["message"]["content"]
        result_table = [line.split("|") for line in result_text.strip().split("\n")[2:-1]]
        results = []
        for row in result_table:
            try:
                results.append(
                    {"sentence_index": int(row[0].strip()), "bias": row[1].strip(), "explanation": row[2].strip()})
            except IndexError:  # Handle potential errors in response format
                print(f"Warning: Unexpected response format for sentence: {row}")

        return results

    def classify_from_csv(self, file_path, batch_size=50):
        """
        Classifies sentences from a CSV file in batches.

        Args:
            file_path (str): Path to the CSV file containing sentences.
            batch_size (int, optional): The size of each batch. Defaults to 50.
        """
        df = pd.read_csv(file_path)
        all_results = []
        for i in range(0, len(df), batch_size):
            batch = df['sentences'][i:i + batch_size].tolist()
            results = self.classify_sentences(batch)
            all_results.extend(results)
        return all_results


# classifier = GPTBiasClassifier(api_key="api_key")
#
#
# sentences = ['When a candidate arrives, he must be ready for the interview.',
#              'Two plus two is four, and everyone should know that!',
#              'I do not understand this subject.',
#              'Mankind will suffer if serious actions are not taken to solve the climate problems.']
#
# print(classifier.classify_sentences(sentences))
# results = classifier.classify_from_csv("your_sentences.csv")
# print(results)
