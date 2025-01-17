# import spacy;
# from watchmen.lake.model_schema import ModelSchema
#
# from watchmen.common.knowledge.knowledge_loader import load_lexicon
#
# nlp = spacy.load('en_core_web_sm')
#
# def lexicon_match(model_schema: ModelSchema):
#     keys = model_schema.businessFields.keys()
#     # values = model_schema.businessFields.values()
#     field_names = " ".join(keys)
#     lexicon_lib = load_lexicon(model_schema.domain, "en")
#
#     lexicon_str = " ".join(lexicon_lib.keys())
#
#     tokens = nlp(field_names)
#
#     lexicon_tokens = nlp(lexicon_str)
#
#     lexicon_match_results = []
#
#     for import_token in tokens:
#         for lexicon_token in lexicon_tokens:
#             if import_token.has_vector:
#                 similarity = import_token.similarity(lexicon_token)
#                 if similarity > 0.7:
#                     lexicon_match_results.append(
#                         {"source": import_token.text, "target": lexicon_token.text, "similarity": str(similarity)})
#
#     return lexicon_match_results
