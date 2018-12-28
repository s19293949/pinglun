import os
current_path=os.getcwd()
os.chdir(current_path)
import readdata
from word2vec import *
import lstm_model
import numpy as np
import tensorflow as tf



#文件路径
train_data_path="./data/lstm/training_params.pickle"


#模型超参
class config():
    test_sample_percentage=0.1 #训练样本和测试样本的比例
    num_labels=2               #标签数量
    embedding_size=64          #词向量维度
    dropout_keep_prob=1      #dropout数量
    batch_size=64
    num_epochs=80
    max_sentences_length=100
    num_layers=2
    max_grad_norm=5
    l2_rate=0.000005
params = readdata.loadDict(train_data_path)

testconfig=config()
lstm=lstm_model.TextLSTM(config=testconfig)
sess = tf.InteractiveSession()        
saver = tf.train.Saver()
saver.restore(sess, "./data/lstm/text_model")

def get_lstm_result(test_sample):   
    train_length = int(params['max_sentences_length'])
    test_sample_lists = readdata.get_cleaned_list1(test_sample)
    test_sample_lists,max_sentences_length = readdata.padding_sentences(test_sample_lists,padding_token='<PADDING>',padding_sentence_length=train_length)
    test_sample_arrays=np.array(get_embedding_vector(test_sample_lists))

    def test_step(x_batch):
        feed_dict={
            lstm.input_x:x_batch,
            lstm.dropout_keep_prob:testconfig.dropout_keep_prob
        }
        predictions,scores=sess.run(
            [lstm.predictions,lstm.softmax_result],
            feed_dict=feed_dict
        )
        return (predictions,scores)


    #定义测试函数


    predictions, scores=test_step(test_sample_arrays)
    return np.array(predictions),np.array(scores)
    #print("(0->neg & 1->pos)the result is:")
    #print(predictions)
    #print("********************************")
    #print("the scores is:")
    #print(scores)

