from acc_test import test_acc
def train(model, training_data, test_data, epochs = 2000, init_lr = 0.1, momentum = 0.9 ,tolerance = 200, lr_decrese_rate = 0.1, path = None, callbacks = []):
    if path is None:
        path = model.model_name + '.npz'
    best_correct = 0
    best_loss = 1e10
    epoach_since_best = 0
    lr = init_lr
    val_acc = None
    train_acc = None
    for epoch_id in range(epochs):
        loss = 0
        correct = 0
        for sample in training_data:
            model.input_sample(sample[:-1],sample[-1])
            model.forward()
            loss += model.loss()
            model.backward()
            model.update(lr,lr2=2*lr,momentum = momentum)
            if (model.output_prediction()[0] > 0.5 and sample[-1] > 0.5) or (model.output_prediction()[0] < 0.5 and sample[-1] < 0.5):
                correct += 1
        if test_data is not None:
            val_acc = test_acc(model,test_data)
        train_acc = correct/len(training_data)
        loss /= len(training_data)

        if correct > best_correct or loss < best_loss:
            model.create_checkpoint()
            best_correct = correct
            best_loss = loss
            epoach_since_best = 0
        else:
            epoach_since_best += 1
            if epoach_since_best > tolerance:
                if(correct==len(training_data)):
                    break
                model.restore_checkpoint()
                model.optimizer.reset()
                epoach_since_best = 0
                lr *= lr_decrese_rate
        
        if callbacks:
            for cb in callbacks:
                cb(**locals())
            
    model.restore_checkpoint()
    model.save(path)
    if test_data is not None:
        print("test_acc=",test_acc(model,test_data))