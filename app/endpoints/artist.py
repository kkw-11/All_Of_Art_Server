from fastapi import APIRouter, HTTPException

from ..database import SessionLocal
from ..models import artist, painting

router = APIRouter()


@router.get("/", summary="Get artists information")
def get_all_artist():
    # 화가 사진이랑 이름
    with SessionLocal() as db:
        all_artists = db.query(artist.Artist).all()
    result = []
    for each_artist in all_artists:
        result.append(
            {
                "id": each_artist.id,
                "profile": f"/static/images/artist/{each_artist.name}.jpg",
                "name": each_artist.name.replace("_", " "),
            }
        )

    return result


@router.get("/detail/{artist_id}")
def get_artist_detail(artist_id: int = 1):
    with SessionLocal() as db:
        some_artist = (
            db.query(artist.Artist).filter(artist.Artist.id == artist_id).one_or_none()
        )
        if (some_artist is None) or (artist_id > 50):
            raise HTTPException(status_code=404, detail="요청하신 화가가 없습니다!")
        number_of_paintings = (
            db.query(painting.Painting)
            .filter(painting.Painting.painting_type == artist_id)
            .count()
        )

    some_artist.bio1 = "화가 소개 한줄짜리"  # 임의로 null 값 수정
    some_artist.bio2 = "상세정보에서 보이는 디테일한 화가 소개"  # 임의로 null 값 수정

    images = [
        f"/static/images/artist/{some_artist.name.replace(' ','_')}_{i}.jpg"
        for i in range(1, number_of_paintings + 1)
    ]
    images.insert(0, f"/static/images/profile/{some_artist.name.replace(' ','_')}.jpeg")
    some_artist.images = images

    return some_artist