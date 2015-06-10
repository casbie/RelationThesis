#author: Yu-Ju Chen
#date: 2015-06-09

#relation list:
#   MotivatedByGoal, HasProperty, CapableOf, HasFirstSubevent, Desires,
#   HasSubevent, CausesDesire, MadeOf, SymbolOf, NotDesires,
#   UsedFor, AtLocation, IsA, Causes, PartOf

from os.path import join
import json

def read_pair(rel):
    pair_list = []
    fp = open(join('Relation', rel+'.txt'))
    for line in fp:
        p = line.strip().split(',')
        pair_list.append((p[0], p[1]))
    return pair_list


def read_corpus():
    corpus = []
    pattern = []
    corpus_path = join('../../LearnRelation/Data/sa_json','small_output.jsons')
    fp = open(corpus_path)
    for line in fp:
        article = []
        article_pattern = []
        data = json.loads(line.strip())
        for s in data['sentence']:
            sentence = []
            sentence_pattern = []
            for w in s:
                sentence.append(w[0].encode('utf-8'))
                sentence_pattern.append(w[1].encode('utf-8'))
            article.append(sentence)
            article_pattern.append(sentence_pattern)
        corpus.append(article)
        pattern.append(article_pattern)
    return corpus, pattern


def map_corpus(pairs, corpus, pattern):
    corpus_pair = []
    seed_index = {}
    seed_pattern = {}
    index = 0
    for p in pairs:
        index += 1
        if index % 1000 == 0:
            print index

        for i in range(0,len(corpus)):
            for j in range(0,len(corpus[i])):
                if p[0] in corpus[i][j] and p[1] in corpus[i][j] and (p[0],p[1]):
                    corpus_pair.append((p[0], p[1]))

                    if (p[0],p[1]) in seed_index:
                        seed_index[(p[0],p[1])].append(str(i)+'-'+str(j))
                    else:
                        seed_index[(p[0],p[1])] = [str(i)+'-'+str(j)]

                    idx_0 = corpus[i][j].index(p[0])
                    idx_1 = corpus[i][j].index(p[1])
                    if (p[0],p[1]) in seed_pattern:
                        seed_pattern[(p[0],p[1])].append(pattern[i][j][idx_0]+'+'+pattern[i][j][idx_1])
                    else:
                        seed_pattern[(p[0],p[1])] = [pattern[i][j][idx_0]+'+'+pattern[i][j][idx_1]]
    return corpus_pair, seed_index, seed_pattern


def remove_same(old_list):
    new_list = []
    for data in old_list:
        if data not in new_list:
            new_list.append(data)
    return new_list


def write_pair(rel, pairs):
    fp = open(join('Relation_corpus', rel+'.txt'), 'w')
    for p in remove_same(pairs):
        fp.write(p[0]+','+p[1]+'\n')
    fp.close()


def write_index(rel, seed_index):
    fp = open(join('Seed_index',rel+'.txt'), 'w')
    for seed in seed_index:
        fp.write(seed[0]+','+seed[1]+':')
        for i in range(0,len(seed_index[seed])):
            fp.write(seed_index[seed][i])
            if i != len(seed_index[seed])-1:
                fp.write(',')
            else:
                fp.write('\n')


def write_pattern(rel, seed_pattern):
    fp = open(join('Seed_pattern',rel+'.txt'), 'w')
    for seed in seed_pattern:
        fp.write(seed[0]+','+seed[1]+':')
        for i in range(0,len(seed_pattern[seed])):
            fp.write(seed_pattern[seed][i])
            if i != len(seed_pattern[seed])-1:
                fp.write(',')
            else:
                fp.write('\n')


def main():
    rel_list = ['MotivatedByGoal', 'HasProperty', 'CapableOf', 'HasFirstSubevent', 'Desires',
            'HasSubevent', 'CausesDesire', 'MadeOf', 'SymbolOf', 'NotDesires',
            'UsedFor', 'AtLocation', 'IsA', 'Causes', 'PartOf']
    #rel_list = ['SymbolOf']
    corpus, pattern = read_corpus()
    for rel in rel_list:
        pairs = read_pair(rel)
        corpus_pairs, seed_index, seed_pattern = map_corpus(pairs, corpus, pattern)
        print len(corpus_pairs)
        #write_pair(rel, corpus_pairs)
        write_index(rel, seed_index)
        write_pattern(rel, seed_pattern)

if __name__ == '__main__':
    main()
