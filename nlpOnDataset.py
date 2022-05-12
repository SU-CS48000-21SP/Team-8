from pytorch_pretrained_bert import BertTokenizer, BertForSequenceClassification, BertAdam
import torch
from torch.utils.data import TensorDataset, RandomSampler, SequentialSampler, DataLoader
from torch.nn import BCEWithLogitsLoss, Sigmoid
from tqdm.notebook import tqdm, trange
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

df_train = pd.read_csv("filteredTitles.csv")

df_train = df_train.head()
token_titles = ["[CLS] "+ i + " [SEP]"for i in df_train]


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case = True)

train_tokenizer_texts = list(map(lambda t: tokenizer.tokenize(t)[:510], tqdm(token_titles)))

MAX_LEN = 128

input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tqdm(train_tokenizer_texts)]
input_ids = pad_sequences(sequences = input_ids, maxlen = MAX_LEN, dtype = 'long', padding='post', truncating='post')

print(input_ids[0])

def create_attention_masks(input_ids):
    attention_masks = []
    for seq in tqdm(input_ids):
        seq_mask = [float(i>0) for i in seq]
        attention_masks.append(seq_mask)
    return np.array(attention_masks)

attention_masks = create_attention_masks(input_ids)

print(attention_masks[0])

X_train, X_val, y_train, y_val = train_test_split(input_ids, labels, random_state = 123, test_size = 0.20)
attention_masks_train, attention_masks_val = train_test_split(attention_masks, random_state = 123, test_size = 0.20)

# Convert all inputs and labels into torch tensors, the required datatype 
X_train = torch.tensor(X_train)
X_val = torch.tensor(X_val)
y_train = torch.tensor(y_train) 
y_val = torch.tensor(y_val)
attention_masks_train = torch.tensor(attention_masks_train)
attention_masks_val = torch.tensor(attention_masks_val)


BATCH_SIZE = 32
#Dataset wrapping tensors.
train_data = TensorDataset(X_train, attention_masks_train, y_train)
val_data = TensorDataset(X_val, attention_masks_val, y_val)

#Samples elements randomly. If without replacement(default), then sample from a shuffled dataset.
train_sampler = RandomSampler(train_data)
val_sampler = SequentialSampler(val_data)

#represents a Python iterable over a dataset
train_dataloader = DataLoader(train_data, sampler = train_sampler, batch_size = BATCH_SIZE)
val_dataloader = DataLoader(val_data, sampler = val_sampler, batch_size = BATCH_SIZE)

#Inititaing a BERT model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels = 6)

#Dividing the params into those which needs to be updated and rest
param_optimizer = list(model.named_parameters())
no_decay = ['bias', 'gamma', 'beta']
optimizer_grouped_parameters = [
    {
        'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
        'weight_decay_rate': 0.01
    },
    {
        'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
        'weight_decay_rate': 0.0
    }
]

optimizer = BertAdam(optimizer_grouped_parameters, lr = 2e-5, warmup = .1)

#freeing up memory
torch.cuda.empty_cache()
import gc
gc.collect()

#Empty the GPU memory as it might be memory and CPU intensive while training
torch.cuda.empty_cache()
#Number of times the whole dataset will run through the network and model is fine-tuned
epochs = 2
#Iterate over number of epochs
for _ in trange(epochs, desc = "Epoch"):
    #Switch model to train phase where it will update gradients
    model.train()
    #Initaite train and validation loss, number of rows passed and number of batches passed
    tr_loss = 0
    nb_tr_examples, nb_tr_steps = 0, 0
    val_loss = 0
    nb_val_examples, nb_val_steps = 0, 0
    #Iterate over batches within the same epoch
    for batch in tqdm(train_dataloader):
        #Shift the batch to GPU for computation
        batch = tuple(t.to(device) for t in batch)
        #Load the input ids and masks from the batch
        b_input_ids, b_input_mask, b_labels = batch
        #Initiate gradients to 0 as they tend to add up
        optimizer.zero_grad()
        #Forward pass the input data
        logits = model(b_input_ids, token_type_ids = None, attention_mask = b_input_mask)
        #We will be using the Binary Cross entropy loss with added sigmoid function after that in BCEWithLogitsLoss
        loss_func = BCEWithLogitsLoss()
        #Calculate the loss between multilabel predicted outputs and actuals
        loss = loss_func(logits, b_labels.type_as(logits))
        #Backpropogate the loss and calculate the gradients
        loss.backward()
        #Update the weights with the calculated gradients
        optimizer.step()
        #Add the loss of the batch to the final loss, number of rows and batches
        tr_loss += loss.item()
        nb_tr_examples += b_input_ids.size(0)
        nb_tr_steps += 1
    #Print the current training loss 
    print("Train Loss: {}".format(tr_loss/nb_tr_examples))
    #Switch the model to evaluate stage at which the gradients wont be updated
    model.eval()
    #Iterate over the validation data
    for step, batch in enumerate(val_dataloader):
         #Shift the validation data to GPUs for computation
        batch = tuple(t.to(device) for t in batch)
        #We dont want to update the gradients
        with torch.no_grad():
            #Load the input ids and masks from the batch
            b_input_ids, b_input_mask, b_labels = batch
            #Forward pass the input data
            logits = model(b_input_ids, token_type_ids = None, attention_mask = b_input_mask)
            #We will be using the Binary Cross entropy loss with added sigmoid function after that in BCEWithLogitsLoss
            loss_func = BCEWithLogitsLoss()
            #Calculate the loss between multilabel predicted outputs and actuals
            loss = loss_func(logits, b_labels.type_as(logits))
            #Add the loss of the batch to the final loss, number of rows and batches
            val_loss += loss.item()
            nb_val_examples += b_input_ids.size(0)
            nb_val_steps += 1
    #Print the current validation loss     
    print("Valid Loss: {}".format(val_loss/nb_val_examples))
    outputs = []

#Iterate over the test_loader 
for step, batch in enumerate(train_dataloader):
        #Transfer batch to GPUs
        batch = tuple(t.to(device) for t in batch)
        #We dont need to update gradients as we are just predicting
        with torch.no_grad():
            #Bring up the next batch of input_texts and attention_masks 
            b_input_ids, b_input_mask = batch
            #Forward propogate the inputs and get output as logits
            logits = model(b_input_ids, token_type_ids = None, attention_mask = b_input_mask)
            #Pass the outputs through a sigmoid function to get the multi-label preditions
            s = Sigmoid()
            out = s(logits).to('cpu').numpy()    
            #Add the predictions for this batch to the final list
            outputs.extend(out)