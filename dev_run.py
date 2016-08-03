from hjlog import app
import os
import random

from hjlog import db
from hjlog.models import User, Post, Tag

db.drop_all()
db.create_all()

u = User()
u.username = 'admin'
u.password = 'supersecret'

db.session.add(u)
db.session.commit()

dummy_body = """
# 이천십오년 오월 팔일

이상의 인간이 유소년에게서 피다. 풀이 타오르고 찾아다녀도, 위하여, 위하여 기관과 봄바람이다. 많이 충분히 것은 가치를 황금시대의 사막이다. 따뜻한 이는 인생에 황금시대다. 속잎나고, 아니더면, 같이, 스며들어 천지는 것은 우리의 사막이다. 동력은 창공에 황금시대를 생명을 인간의 가치를 길을 트고, 부패뿐이다. 청춘의 봄날의 그러므로 미인을 황금시대다. 이상 위하여 어디 것이다. 곳으로 위하여, 꾸며 없는 인생을 이것이야말로 이상, 봄바람이다. 피어나는 얼마나 우리의 두손을 힘있다. 가진 풀이 인간에 아니다.

#### 심장은 있는 인간이 싶이 밝은 것이다. 것은 천자만홍이 품에 듣기만 돋고, 부패뿐이다. 아니더면, 청춘의 품으며, 실현에 끓는 가치를 하여도 같은 이것이다. 위하여서, 인간의 돋고, 때에, 커다란 청춘이 속잎나고, 사막이다. 우는 봄날의 되는 없는 그들의 원질이 그것을 약동하다. 오아이스도 우리 물방아 보는 꽃이 이것은 어디 피다. 쓸쓸한 모래뿐일 사랑의 뿐이다. 열락의 바이며, 있음으로써 불러 열락의 말이다. 이것은 평화스러운 청춘이 불어 말이다. 별과 그들은 피어나기 얼마나 그들의 있다. 가치를 놀이 방황하여도, 그들은 생생하며, 있는가? 피가 눈이 품었기 커다란 ?

**위하여서**, *실로 그들의 사막이다.* 풍부하게 가슴이 방황하여도, 피부가 능히 같은 이것이다. 그림자는 보이는 피어나기 곧 뿐이다. 산야에 현저하게 살았으며, 이것을 커다란 심장은 위하여서. 설레는 곳이 봄날의 그들의 어디 운다. 우는 동력은 설산에서 이는 아름다우냐? 아니한 것은 인생에 때문이다. 없는 같지 같은 같이, 피다. 있으며, 석가는 없으면 사람은 곧 가장 교향악이다. 피에 청춘에서만 우는 풍부하게 풀이 이것을 이상의 이는 피다.

- 리스트
- 카이스트
- 베스트

1. 목록
2. 방명록
3. 호로로록

[세상에서 가장 아름다운 여성](facebook.com/hajin.shim.1)

![바로 이 분](https://scontent-lhr3-1.xx.fbcdn.net/l/t31.0-8/12605558_856619597791033_3084313196590193040_o.jpg)
"""

dummy_tagnames = ["개발", "일상", "태그", "콜드브류", "샤브향", "알레스클라"]
dummy_tags = [Tag(tagname) for tagname in dummy_tagnames]

for dummy_tag in dummy_tags:
    db.session.add(dummy_tag)
    db.session.commit()

for i in range(15):
    p = Post(
            "{} 번째 테스트 글".format(i + 1),
            dummy_body,
            "everyday",
            u,
            [dummy_tag for dummy_tag in dummy_tags if random.random() > 0.5]
            )
    db.session.add(p)
    db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
