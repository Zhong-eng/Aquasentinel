import torch
import random
import torchvision
import matplotlib.pyplot as plt

torch.nn.MaxPool2d()

transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
  torchvision.transforms.Normalize((0.5,), (0.5,)),
])

trainset = torchvision.datasets.MNIST('train_set', download=True, train=True, transform=transform) # downloads to train_set
valset = torchvision.datasets.MNIST('test_set', download=True, train=False, transform=transform) # downloads to test_set
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True) # batch is the number of images to consider at a time
valloader = torch.utils.data.DataLoader(valset, batch_size=64, shuffle=True)


torch.nn.ReLU()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

input_size = 28

hidden_sizes = [128, 64, 32, 16, 8, 4]

num_class = 10


model = torch.nn.Sequential(
    # [(64) batch_size, (784) width x height] -> [(64) batch_size, (128) hidden_size #1]
    torch.nn.Linear(input_size, hidden_sizes[0]),
    torch.nn.ReLU(), # activation function
    # [(64) batch_size, (128) hidden_size #1] -> [(64) batch_size, (32) hidden_size #2]
    torch.nn.Linear(hidden_sizes[0], hidden_sizes[1]),
    torch.nn.ReLU(), # activation function
    # [(64) batch_size, (32) hidden_size #2] -> [(64) batch_size, (10) num_class]

    #EXERCISE: Define the third layer as taking in the output size of the second layer and outputting the number of classes.
    torch.nn.Linear(hidden_sizes[1], hidden_sizes[2]),
    # torch.nn.Linear(hidden_sizes[2], hidden_sizes[3]),
    # torch.nn.Linear(hidden_sizes[3], hidden_sizes[4]),
    # torch.nn.Linear(hidden_sizes[4], hidden_sizes[5]),
    torch.nn.Linear(hidden_sizes[2], num_class),
    # output activation function - the hidden layer functions don't work for optimization
    # LogSoftmax because it is better at gradient optimization
    torch.nn.LogSoftmax(dim=-1) # apply LogSoftmax to the last layer (num_class)
)

print(model.to(device))



criterion = torch.nn.NLLLoss() # Loss object to find back propagation
optimizer = torch.optim.SGD(model.parameters(), lr=0.003, momentum=0.9) # Optimizer
epochs = 8
for e in range(epochs):
    running_loss = 0
    for images, labels in trainloader:
        #EXERCISE: transfer images and labels to GPU.
        images = images.to(device)
        labels = labels.to(device)
        # Formats the image to be a usable 1d array.
        #   [(64) batch size, 1, 28, 28] -> [(64) batch size, 784]
        images = images.view(images.shape[0], -1)

        # Resets the optimizer for each training step
        optimizer.zero_grad()

        # Finds error then runs back propagation
        # step 1
        output = model(images)
        #EXERCISE: calculate the loss by passing the outputs and the labels into the lsos function.
        # step 2
        loss = criterion(output, labels)
        # step 3
        loss.backward()

        # Updates model weights
        optimizer.step()

        # Keeps track of error to allow visualization of progress
        running_loss += loss.item()
    else:
        print("Epoch {} - Training loss: {}".format(e, running_loss/len(trainloader)))