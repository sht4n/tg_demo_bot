import dataclasses
import random
import requests


@dataclasses.dataclass
class Form:
	user_id: str
	lat: float
	long: float
	goal: str
	city: str
	gender: str
	preference: str
	name: str
	age: int
	description: str
	first_photo_id: str
	second_photo_id: str | None
	third_photo_id: str | None


class Base():
    def __init__(self) -> None:
        pass

    def predict(self, user_id: str) -> Form:
        params = {
            "user_id": user_id
        }
        response = requests.get(url="http://0.0.0.0:6432/form/get_candidates", params=params)
        forms = response.json()
        jsn = random.choice(forms["feed"])
        return {
            "user_id_from": user_id,
            "form": jsn,
        }
    
base = Base()

     
@dataclasses.dataclass
class RecomendationPrediction:
    form: Form


def load_model():
    def model(user_id: str) -> RecomendationPrediction:
        prediction = base.predict(user_id=user_id)
        return RecomendationPrediction(
            form=prediction["form"],
        )
    return model
