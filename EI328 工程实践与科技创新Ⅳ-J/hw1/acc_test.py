def test_acc(model,data):
    correct = 0
    for sample in data:
            model.input_sample(sample[:-1],sample[-1])
            model.forward()
            if (model.output_prediction()[0] > 0.5 and sample[-1] > 0.5) or (model.output_prediction()[0] < 0.5 and sample[-1] < 0.5):
                correct += 1
    return correct/len(data)

def test_acc_(pred,data):
    correct = 0
    for sample in data:
            p = pred(sample[0:2])
            if (p > 0.5 and sample[-1] > 0.5) or (p < 0.5 and sample[-1] < 0.5):
                correct += 1
    return correct/len(data)