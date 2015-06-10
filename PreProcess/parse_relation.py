# author: Yu-Ju Chen
# date: 2015-06-09
# generate relation pairs from ConceptNet
# check the directory Relation/


import json
from os.path import join

def read_input(fp):
    output = {}
    for line in fp:
        data = json.loads(line.strip())
        start = data['start'][len('/c/zh_TW/'):]
        end = data['end'][len('/c/zh_TW/'):]
        rel = data['rel'][len('/r/'):]

        if rel in output:
            output[rel].append((start,end))
        else:
            output[rel] = [(start,end)]
    return output


def write_output(rel, data):
    fp_out = open(join('Relation', rel.encode('utf-8')+'.txt'), 'w')
    for d in data:
        fp_out.write(d[0].encode('utf-8')+','+d[1].encode('utf-8')+'\n')
    fp_out.close()


def main():
    fp_in = open('conceptnet4_zh.json')
    data = read_input(fp_in)
    for rel in data:
        print rel, len(data[rel])
    for rel in data:
        write_output(rel, data[rel])

if __name__ == '__main__':
    main()
