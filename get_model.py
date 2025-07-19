from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from preprocess import preprocessing

import os
os.environ["CURL_CA_BUNDLE"] = ""


MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
# MODEL_NAME = "facebook/bart-large-cnn"
TOKENIZER = AutoTokenizer.from_pretrained(MODEL_NAME)
MODEL = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def get_prediction(article_obj):

    def abs_sum(text, model, tokenizer):

        tokens_input = tokenizer.encode(text,
                                        max_length=512,
                                        padding="max_length",
                                        truncation=True, return_tensors="pt")

        summary_ids = model.generate(tokens_input,
                                     max_length=200,
                                     min_length=50,
                                     length_penalty=15, num_beams=4,
                                     no_repeat_ngram_size=3)

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

        return summary

    results = []
    for obj in article_obj:
        summarized_text = abs_sum(preprocessing(obj.articleContent), MODEL, TOKENIZER)
        results.append({"articleUuid": obj.articleUuid,
                        "summarizedContent": summarized_text
                        })

    return results
