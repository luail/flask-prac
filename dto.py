from pydantic import BaseModel


class RepoDTO(BaseModel):
    name: str          # owner/repo 형태
    description: str   # 저장소 설명 (없으면 빈 문자열)
    language: str      # 주 언어 (없으면 "Unknown")
    stars: int         # 전체 스타 수
    stars_today: int   # 오늘 획득 스타
    url: str           # 저장소 URL
