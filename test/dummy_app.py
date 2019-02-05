#!/usr/bin/python
# -*- coding: utf-8 -*-


from rekcurd import Rekcurd
from rekcurd.utils import PredictLabel, PredictResult, EvaluateResult, EvaluateResultDetail, EvaluateDetail
from typing import List, Generator


class DummyApp(Rekcurd):
    def __init__(self, config_file: str = None):
        super().__init__(config_file)

    def load_model(self) -> None:
        pass

    def predict(self, input: PredictLabel, option: dict = None) -> PredictResult:
        pass

    def evaluate(self, file: bytes) -> EvaluateResult:
        pass

    def get_evaluate_detail(self, file_path: str, results: List[EvaluateResultDetail]) -> Generator[EvaluateDetail, None, None]:
        pass
