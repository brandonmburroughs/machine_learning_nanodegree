"""A small module to predict missing words in text."""
import operator
from collections import defaultdict


def next_word_probability(sampletext, word):
    """Get the probability of words follow the given word from the given sample text.

    Parameters
    ----------
    sampletext : str
        A sample corpus
    word : str
        A word in the corpus

    Returns
    -------
    dict
        A dictionary of word counts that follow the given word
    """
    # Split the text
    split_text = sampletext.split()

    # Count all of the words following the word
    prob_dict = defaultdict(int)
    for i, new_word in enumerate(split_text):
        if new_word == word and i != len(split_text):
            prob_dict[split_text[i + 1]] += 1

    return prob_dict


def normalize_dictionary(dictionary):
    """Normalize the counts in a dictionary.

    Parameters
    ----------
    dictionary : dict
        A dictionary with count values

    Returns
    -------
    dict
        A dictionary with normalized counts
    """
    total_count = sum(dictionary.values())

    for key, value in dictionary.iteritems():
        dictionary[key] = float(value) / total_count

    return dictionary


def predict_following_word(sample, word, distance):
    """Given a sample text, predict the most likely word to be `distance` words away from the given
    `word`.

    Parameters
    ----------
    sample : str
        A sample corpus
    word : str
        A word in the corpus
    distance : int
        How many words after the given word to predict

    Returns
    -------
    str
        The most likely word to be `distance` words from the given `word`
    """
    # This will be like a tree search, initialize with the root note
    word_distance_prob = {word: 1.0}

    # Traverse the "tree" by distance
    for _ in xrange(distance):
        next_word_distance_prob = {}

        # Iterate through all of the current words
        for new_word, prob in word_distance_prob.iteritems():
            relative_word_probabilities = normalize_dictionary(
                next_word_probability(sample, new_word)
            )

            # Get the conditional probability
            for key, value in relative_word_probabilities.iteritems():
                relative_word_probabilities[key] = value * prob

            # Update the current word probabilities at this point in the traversal
            next_word_distance_prob.update(relative_word_probabilities)

        # Set the root node to the current node
        word_distance_prob = next_word_distance_prob

    return max(word_distance_prob.iteritems(), key=operator.itemgetter(1))[0]


def demo():
    """A little demo."""
    sample_memo = """
    Milt, we're gonna need to go ahead and move you downstairs into storage B. We have some new people coming in, and we need all the space we can get. So if you could just go ahead and pack up your stuff and move it down there, that would be terrific, OK?
    Oh, and remember: next Friday... is Hawaiian shirt day. So, you know, if you want to, go ahead and wear a Hawaiian shirt and jeans.
    Oh, oh, and I almost forgot. Ahh, I'm also gonna need you to go ahead and come in on Sunday, too...
    Hello Peter, whats happening? Ummm, I'm gonna need you to go ahead and come in tomorrow. So if you could be here around 9 that would be great, mmmk... oh oh! and I almost forgot ahh, I'm also gonna need you to go ahead and come in on Sunday too, kay. We ahh lost some people this week and ah, we sorta need to play catch up.
    """

    corrupted_memo = """
    Yeah, I'm gonna --- you to go ahead --- --- complain about this. Oh, and if you could --- --- and sit at the kids' table, that'd be --- 
    """

    print "CORRUPTED MEMO:"
    print corrupted_memo
    print "CORRUPTED MEMO FIXED:"
    print """
    Yeah, I'm gonna {} you to go ahead {} {} complain about this. Oh, and if you could {} {} and sit at the kids' table, that'd be {} 
    """.format(
        predict_following_word(sample_memo, "gonna", 1),
        predict_following_word(sample_memo, "ahead", 1),
        predict_following_word(sample_memo, "ahead", 2),
        predict_following_word(sample_memo, "could", 1),
        predict_following_word(sample_memo, "could", 2),
        predict_following_word(sample_memo, "be", 1)
    )


if __name__ == "__main__":
    demo()