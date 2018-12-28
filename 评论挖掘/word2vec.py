import gensim
import numpy as np



print("loading word2vec model now...........")
embedding_model_path="./data/embedding_64.bin"

model=gensim.models.KeyedVectors.load_word2vec_format(embedding_model_path,binary=True)

print("loading word2vec finished")
def get_embedding_vector(sentences):

    global model
    all_sample_vector_lists=[]
    padding_embedding=np.array([0] * model.vector_size,dtype=np.float32)
    for sentence in sentences:
        sentence_vector = []
        for word in sentence:
            if word in model.vocab:
                sentence_vector.append(model[word])
            else:
                sentence_vector.append(padding_embedding)
        all_sample_vector_lists.append(sentence_vector)
        del sentence_vector
    del sentences
    return all_sample_vector_lists