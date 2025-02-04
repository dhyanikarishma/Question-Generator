# -*- coding: utf-8 -*-
"""Question_generator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pvpO4hif1tLNtED7aTlRYsqPXrB2JIKR
"""
#using pre-trained model

!pip install transformers

from transformers import pipeline

def generate_questions(paragraph, max_questions=5):
    try:
        question_generator = pipeline("text2text-generation", model="valhalla/t5-small-qg-prepend")

        questions = question_generator(
            f"generate questions: {paragraph}",
            max_length=256,
            num_return_sequences=max_questions,
            do_sample=True
        )

        return [q["generated_text"] for q in questions]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    paragraph = input("Enter a paragraph or a single line of text: ").strip()

    if paragraph:
        questions = generate_questions(paragraph)

        if questions:
            print("\nGenerated Questions:")
            for i, question in enumerate(questions, 1):
                print(f"{i}. {question}")
        else:
            print("No questions could be generated. Please try with different input.")
    else:
        print("Input cannot be empty. Please try again.")

if __name__ == "__main__":
    main()

!pip install datasets

#creating own model

import nltk
import random
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords

def extract_keywords(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    keywords = [word for word, tag in tagged_words if tag in ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"] and word.lower() not in stopwords.words("english")]
    return keywords

def generate_question(sentence):
    keywords = extract_keywords(sentence)

    if not keywords:
        return "No question."

    keyword = random.choice(keywords)

    for word in pos_tag(word_tokenize(sentence)):
        if word == keyword:
            if tag in ["NN", "NNS", "NNP", "NNPS"]:
                return f"What/Who is {keyword}?"
            elif tag in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
                return f"What is {keyword} doing?"

    return f"Can you explain about {keyword}?"

text = input("Enter your sentence: ")
print(generate_question(text))

