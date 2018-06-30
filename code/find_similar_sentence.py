import argparse
import tensorflow as tf
import tensorflow_hub as hub
import time
import sys

from annoy import AnnoyIndex

D=512


def print_with_time(msg):
    print('{}: {}'.format(time.ctime(), msg))
    sys.stdout.flush()


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sentences')
    parser.add_argument('-ann')
    parser.add_argument('-k', default=10, type=int, help='# of neighbors')
    return parser.parse_args()


def load_sentences(file):
    with open(file) as fr:
        return [line.strip() for line in fr]


def main():
    args = setup_args()
    print_with_time(args)

    ann = AnnoyIndex(D)
    ann.load(args.ann)
    print_with_time('Annoy Index: {}'.format(ann.get_n_items()))

    sentences = load_sentences(args.sentences)
    print_with_time('Sentences: {}'.format(len(sentences)))


    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/1")
    sentences_ph = tf.placeholder(dtype=tf.string, shape=[None])
    embedding_fun = embed(sentences_ph)

    sess = tf.Session()
    sess.run([tf.global_variables_initializer(), tf.tables_initializer()])

    print_with_time('Ready!')
    while True:
        input_sentence = input('Enter sentence: ').strip()

        if input_sentence == 'q':
            return
        print_with_time('Input Sentence: {}'.format(input_sentence))
        sentence_vector = sess.run(embedding_fun, feed_dict={sentences_ph:[input_sentence]})
        print_with_time('vec done')
        nns = ann.get_nns_by_vector(sentence_vector[0], args.k)
        print_with_time('nns done')
        similar_sentences = [sentences[nn] for nn in nns]
        for sentence in similar_sentences:
            print(sentence)




if __name__ == '__main__':
    main()