# Building The Best ChatBot with Deep NLP



# Importing the libraries
import seq2seq_wrapper
import importlib
importlib.reload(seq2seq_wrapper)
import data_preprocessing
import data_utils_1
import data_utils_2



########## PART 1 - DATA PREPROCESSING ##########


def load_data():
    # Importing the dataset
    metadata, idx_q, idx_a = data_preprocessing.load_data(PATH = './')

    # Splitting the dataset into the Training set and the Test set
    (trainX, trainY), (testX, testY), (validX, validY) = data_utils_1.split_dataset(idx_q, idx_a)

    # Embedding
    xseq_len = trainX.shape[-1]
    yseq_len = trainY.shape[-1]
    batch_size = 16
    vocab_twit = metadata['idx2w']
    xvocab_size = len(metadata['idx2w'])  
    yvocab_size = xvocab_size
    emb_dim = 1024
    idx2w, w2idx, limit = data_utils_2.get_metadata()

    return (xseq_len, yseq_len, xvocab_size, yvocab_size, emb_dim)



########## PART 2 - BUILDING THE SEQ2SEQ MODEL ##########


def build_model():
    # Building the seq2seq model
    xseq_len, yseq_len, xvocab_size, yvocab_size, emb_dim = load_data()
    model = seq2seq_wrapper.Seq2Seq(xseq_len = xseq_len,
                                    yseq_len = yseq_len,
                                    xvocab_size = xvocab_size,
                                    yvocab_size = yvocab_size,
                                    ckpt_path = './weights',
                                    emb_dim = emb_dim,
                                    num_layers = 3)
    return model

########## PART 3 - TRAINING THE SEQ2SEQ MODEL ##########


# See the Training in seq2seq_wrapper.py



########## PART 4 - TESTING THE SEQ2SEQ MODEL ##########


def chat(model, message):
    # Loading the weights and Running the session
    session = model.restore_last_session()

    # Getting the ChatBot predicted answer
    def respond(question):
        idx2w, w2idx, limit = data_utils_2.get_metadata()
        encoded_question = data_utils_2.encode(question, w2idx, limit['maxq'])
        answer = model.predict(session, encoded_question)[0]
        return data_utils_2.decode(answer, idx2w) 
    # Setting up the chat
    question = message.lower()
    if ((question == 'bye') | (question == 'good bye')):
        return ("Bye.. take care. :)")
    if((question == "who are you?") | (question == "what's your name?") | (question == 'tell me about yourself') | (question == "introduce yourself")):
        return ("I'm your personal assisstant, Cruxbreaker. I am here to help you.")
    if((question == "do you know ankit dutta") | (question == "what do think of ankit dutta")):
        return ("Ankit is developer, designer and ML & AI enthusiat. He helped me getting smarter. Checkout his other awesome works: https://github.com/cruxbreaker")
    if((question == "do you know ashok dey") | (question == "what do think of ashok dey")):
        return ("A geek who loves developing web apps! Ashok has helped me look classy and presentable. Checkout more of his great projects: https://github.com/ashokdey")
    if((question == "whom do you work for?") | (question == 'for whom do you work?')):
        return ("I work for you! I am here to help you :)")
    answer = respond(question)
    return (answer)


# def main():
#     chat('bye')

# if __name__ == "__main__":
#         main()