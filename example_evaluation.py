import evaluation as e
e.load_texts('../logs/texts.json')
e.load_xtracts('../logs/2012-06-27_0712-extracts.json')
e.prepare_single_xtracts()
e.prepare_complement_rankings()
e.prepare_avg_rankings()
e.create_extractors('/home/aglazek/private/praca/lang_data/synonimy-slowosiec.txt', '/home/aglazek/private/praca/lang_data/related_words.txt', '/home/aglazek/private/praca/lang_data/combined_stopwords.txt', ['noun'])
e.prepare_grades()
e.prepare_automatic_rankings()
e.prepare_rms_errors()
e.prepare_conv_rms_errors()
e.prepare_coocc_rates()
e.prepare_familiada_scores()
e.compare_xtracts_methods()
p = e.cooccurence_rate.items()
p.sort(key=lambda v : v[1])
p

'''
p = e.method_cumulated_error.items()
p.sort(key=lambda v : v[1])
p
f = open('/tmp/results.json', 'w')
f.write(e.json.dumps(p))
f.close()
'''
'''
for a, b in e.rms_error:
    x.write(str(a)) 
    x.write('\t')
    x.write(b)
    x.write('\t')
    x.write(str(e.rms_error[(a, b)]))
    x.write('\n')
'''

