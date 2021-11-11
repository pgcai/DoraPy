import argparse
import os
import time

import numpy as np
import dorapy as nn

def main():
    if args.seed >= 0:
        nn.seeder.random_seed(args.seed)

    mnist = nn.dataset.MNIST(args.data_dir, one_hot=True)
    train_x, train_y = mnist.train_set
    test_x, test_y = mnist.test_set

    if args.model_type == "mlp":
        # A multilayer perceptron model
        net = nn.net.Net([
            nn.layer.Dense(200),
            nn.layer.ReLU(),
            nn.layer.Dense(100),
            nn.layer.ReLU(),
            nn.layer.Dense(70),
            nn.layer.ReLU(),
            nn.layer.Dense(30),
            nn.layer.ReLU(),
            nn.layer.Dense(10)
        ])
    elif args.model_type == "cnn":
        # A LeNet-5 model with activation function changed to ReLU
        train_x = train_x.reshape((-1, 28, 28, 1))
        test_x = test_x.reshape((-1, 28, 28, 1))
        net = nn.net.Net([
            nn.layer.Conv2D(kernel=[5, 5, 1, 6], stride=[1, 1]),
            nn.layer.ReLU(),
            nn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]),
            nn.layer.Conv2D(kernel=[5, 5, 6, 16], stride=[1, 1]),
            nn.layer.ReLU(),
            nn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]),
            nn.layer.Flatten(),
            nn.layer.Dense(120),
            nn.layer.ReLU(),
            nn.layer.Dense(84),
            nn.layer.ReLU(),
            nn.layer.Dense(10)
        ])
    elif args.model_type == "rnn":
        # A simple recurrent neural net to classify images.
        train_x = train_x.reshape((-1, 28, 28))
        test_x = test_x.reshape((-1, 28, 28))
        net = nn.net.Net([
            nn.layer.RNN(num_hidden=50, activation=nn.layer.Tanh()),
            nn.layer.Dense(10)
        ])
    else:
        raise ValueError("Invalid argument: model_type")

    loss = nn.loss.SoftmaxCrossEntropy()
    optimizer = nn.optimizer.Adam(lr=args.lr)
    model = nn.model.Model(net=net, loss=loss, optimizer=optimizer)

    if args.model_path is not None:
        model.load(args.model_path)
        evaluate(model, test_x, test_y)
    else:
        iterator = nn.data_iterator.BatchIterator(batch_size=args.batch_size)
        loss_list = list()
        for epoch in range(args.num_ep):
            t_start = time.time()
            for batch in iterator(train_x, train_y):
                pred = model.forward(batch.inputs)
                loss, grads = model.backward(pred, batch.targets)
                model.apply_grads(grads)
                loss_list.append(loss)
            print(f"Epoch {epoch} time cost: {time.time() - t_start}")
            # evaluate
            evaluate(model, test_x, test_y)

        # save model
        if not os.path.isdir(args.model_dir):
            os.makedirs(args.model_dir)
        model_name = "mnist-%s-epoch%d.pkl" % (args.model_type, args.num_ep)
        model_path = os.path.join(args.model_dir, model_name)
        model.save(model_path)
        print(f"Model saved in {model_path}")


def evaluate(model, test_x, test_y):
    model.is_training = False
    test_pred = model.forward(test_x)
    test_pred_idx = np.argmax(test_pred, axis=1)
    test_y_idx = np.argmax(test_y, axis=1)
    accuracy, info = nn.metric.accuracy(test_pred_idx, test_y_idx)
    model.is_training = True
    print(f"accuracy: {accuracy:.4f} info: {info}")


if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str,
                        default=os.path.join(curr_dir, "data"))         # data path
    parser.add_argument("--model_dir", type=str,
                        default=os.path.join(curr_dir, "models"))       # model save path
    parser.add_argument("--model_path", type=str, default=None)         # model load path
    parser.add_argument("--model_type", default="cnn", type=str,        # model type(mlp or cnn)
                        help="[*mlp|cnn|rnn]")
    parser.add_argument("--num_ep", default=10, type=int)               # epoch num
    parser.add_argument("--lr", default=1e-3, type=float)               # learning rate
    parser.add_argument("--batch_size", default=128, type=int)          # batch size
    parser.add_argument("--seed", default=-1, type=int)                 # random seed
    args = parser.parse_args()
    main()


































