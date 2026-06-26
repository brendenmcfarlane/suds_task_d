
class Query:
    def __init__(self, **kwargs):
        self._question = kwargs.get("question")
        self._ground_truth = kwargs.get("answer")

    def get_question(self):
        return self._question
    def get_ground_truth(self):
        return self._ground_truth

class MultiMediaQuery(Query):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._image_path = kwargs.get("image_url")

    def get_image_path(self):
        return self._image_path