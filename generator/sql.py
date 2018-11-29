import nltk

cp = nltk.load_parser('../static/grammar.fcfg')
query = 'What cities are located in China'
trees = list(cp.parse(query.split()))
answer = trees[0].label()['SEM']
answer = [s for s in answer if s]
print(' '.join(answer))