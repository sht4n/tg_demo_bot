import dataclasses
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

@dataclasses.dataclass
class Photo:
	first_photo_id: str
	second_photo_id: str | None
	third_photo_id: str | None
	first_photo: str
	second_photo: str | None
	third_photo: str | None

def dump_form(user_data: dict) -> None:
    lat, long = user_data.get("geo", (None, None))
    first_photo_dict = user_data.get("first_photo", {})
    second_photo_dict = user_data.get("second_photo", {})
    third_photo_dict = user_data.get("third_photo", {})

    form = Form(
        user_id=user_data.get("user_id"),
        lat=lat,
        long=long,
        goal=user_data.get("goal"),
        city=user_data.get("city"),
        gender=user_data.get("gender"),
        preference=user_data.get("preference"),
        name=user_data.get("name"),
        age=user_data.get("age"),
        description=user_data.get("description"),
        first_photo_id=first_photo_dict.get("first_photo_id"),
        second_photo_id=second_photo_dict.get("second_photo_id"),
        third_photo_id=third_photo_dict.get("third_photo_id"),
    )

    # to do: upload photo to s3
    photo = Photo(
        first_photo_id=first_photo_dict.get("first_photo_id"),
        second_photo_id=second_photo_dict.get("second_photo_id"),
        third_photo_id=third_photo_dict.get("third_photo_id"),
        first_photo=first_photo_dict.get("first_photo"),
        second_photo=second_photo_dict.get("second_photo"),
        third_photo=third_photo_dict.get("third_photo"),
    )
    
    jsn = dataclasses.asdict(form)
    requests.post(url="http://192.168.0.101:6432/form/upload", json=jsn)

def load_form(user_id_from: str) -> Form:
    params = {"user_id_from": user_id_from}
    response = requests.get("http://192.168.0.101:8000/predict", params=params)
    if response.status_code == 200:
        jsn = response.json()["form"]
        form = Form(
            user_id=jsn.get("user_id"),
            lat=jsn.get("lat"),
            long=jsn.get("long"),
            goal=jsn.get("goal"),
            city=jsn.get("city"),
            gender=jsn.get("gender"),
            preference=jsn.get("preference"),
            name=jsn.get("name"),
            age=jsn.get("age"),
            description=jsn.get("description"),
            first_photo_id=jsn.get("first_photo_id"),
            second_photo_id=jsn.get("second_photo_id"),
            third_photo_id=jsn.get("third_photo_id"),
        )
        return dataclasses.asdict(form)
    return None

def update_like(
    source_user_id: str,
    target_user_id: str,
    is_like: bool
) -> None:
    pass

def get_match(
    source_user_id: str,
) -> Form:
    import random
    dice = random.choice([0, 1, 0, 0, 0, 0])
    if dice:
         return load_form(source_user_id="42")
    return None
