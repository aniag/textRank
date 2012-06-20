import evaluation as e
e.load_texts('../logs/texts.json')
e.load_xtracts('../logs/2012-06-20_0746-extracts.json')
e.prepare_single_xtracts()
e.prepare_complement_rankings()
e.prepare_avg_rankings()
e.create_extractors('/home/aglazek/private/praca/lang_data/synonimy-slowosiec.txt', '/home/aglazek/private/praca/lang_data/related_words.txt', '/home/aglazek/private/praca/lang_data/combined_stopwords.txt', ['noun'])
e.prepare_grades()
e.prepare_automatic_rankings()

