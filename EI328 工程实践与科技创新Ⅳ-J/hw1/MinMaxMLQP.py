from MLQP import MLQP
class MinMaxMLQPPredictor:
    @classmethod
    def load(cls,model_1p2p_path,model_1p2n_path,model_1n2p_path,model_1n2n_path):
        return cls(MLQP.load(model_1p2p_path),MLQP.load(model_1p2n_path),MLQP.load(model_1n2p_path),MLQP.load(model_1n2n_path))

    def __init__(self, model_1p2p, model_1p2n, model_1n2p, model_1n2n):
        self.model_1p2n = model_1p2n
        self.model_1p2p = model_1p2p
        self.model_1n2n = model_1n2n
        self.model_1n2p = model_1n2p

    def predict_prob(self,x):
        # min-max prediction
        return max(min(self.model_1p2n.predict_prob(x),self.model_1p2p.predict_prob(x))
            ,min(self.model_1n2n.predict_prob(x),self.model_1n2p.predict_prob(x)))

    def predict(self,x):
        return self.predict_prob(x) > 0.5