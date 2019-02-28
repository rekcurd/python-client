from rekcurd import Rekcurd


class DummyApp(Rekcurd):
    def load_model(self, **kwargs):
        pass

    def predict(self, **kwargs):
        pass

    def evaluate(self, **kwargs):
        pass

    def get_evaluate_detail(self, **kwargs):
        pass
