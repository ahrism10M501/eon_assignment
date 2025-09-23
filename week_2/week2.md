# 공부 내용

저번에 K-means를 공부하고 이를 직접 구현해보았다.

복습하자면, 데이터 포인트들 중 랜덤한 k개를 중심으로 각 점들의 거리를 비교해 군집화하고,

각 군집들의 평균 위치로 k를 옮겨서 다시 비교하는 식으로 반복해 수렴(혹은 임계값 이하로 진동)할 때 까지 반복하는 간단한 알고리즘이었다.

이번 시간은 이런걸 해본다!

- Silhouette Score, Elbow Method를 직접 구현하고 이를 이용해 군집화 성능 측정하기
- 각 k 값들을 비교하고 이를 통해 적합한 k값 구하기
- C언어로 2차원 행렬 연산을 위한 연습하기

이 중 C언어로 행렬 연산을 만드는건 목표일뿐 실현되지 않을 가능성이 높다.   
못한다면 백준 초급 알고리즘 문제 몇 개를 풀어보려한다.

## 실루엣 스코어란?

데이터 군집화 되었는지 평가 및 검증하기 위해 제안된 지표로, 각 객체가 얼마나 잘 분류되었는지를 간결한 그래픽으로 표현한다.

논문(doi) : https://doi.org/10.1016/0377-0427(87)90125-7

## 논문 분석

A new graphical display is proposed foe partitioning techniques.

Each cluster is represented by a so-called shillouette, which is based on the comparison of its tightness and separation.

논문의 Abstract에서의 문장을 통해 이 silhouette의 개념을 알 수 있다.

1. 그래픽 디스플레이 방식
2. 각 군집을 나타냄
3. 실루엣은 응집도(밀도, 견고함, 단단함)과 분리도간의 비교를 통해 구성됨

Construction of silhouette 파트에서 이를 어떻게 비교하는지 방법이 적혀있다.

1. 필요한 것: partition(군집), 모든 점과의 근접성(거리)(the proximities are on a ratio scale(as in the case of Euclidean distances), 유클리드 거리로 구함)

임의의 군집 A에 대해, 실루엣 s(i)는 다음과 같은 변수를 이용해 정의한다.

a(i) = avg dissimilarity of i to all other objects of A   
어떤 점 i와 군집 A 간의 평균 비유사성(부록 1.)

d(i, C) = avg dissimilarity of i to all objects of C
어떤 군집(속한 군집 제외 다른 군집)과 오브젝트(점, 포인트)i 간의 평균 비유사성

b(i) = minimum d(i, C) (C!=A)
속한 군집 외 다른 군집간의 평균 비유사성 중 가장 작은 값

s(i) = 1-a(i)/b(i) if a(i) < b(i), 0 if a(i) = b(i), b(i)/a(i)-1 if a(i)>b(i)
    = $(b(i) - a(i)) over (max{a(i), b(i)})$

또한 -1 <= s(i) <= 1 로 표현된다.   
위 식이 실루엣을 코딩으로 표현할 때 사용하는 식이다. 이때 논문에서는 proximity로 유클리드 거리를 사용한다고 하였다.

이 식에 대해 생각해보자.

s(i)가 클수록 b(i)가 a(i)보다 크다는 말이다. 여기서 b는 다른 군집과의 거리, a는 자기 군집과의 평균 거리임을 고려하면 이를 군집화가 잘 수행되었다고 할 수 있다(논문 4p.)   
s(i)가 0에 가깝다면 이는 점 i가 두 군집 A와 B 중 어느 곳에 속하기 어려운 애매한 위치에 있다는 것을 시사한다. 마찬가지로 s(i)가 -1에 가까워 진다면, 이는 자기 군집 보다 다른 군집에 어울리는 점이라는 의미이므로 군집화가 잘 안 되었다고 말할 수 있다.


## 부록
### 1. 비유사성과 유사성

데이터 간의 차이를 발함. 유사성이 1에 가까울수록 같거나 비슷하고, 0에 가까울수록 다르다.   
영어로 similarity(유사성)와 dissimilarity(비유사성)으로 나타내며, 논문에서는 proximity라는 용어로 두 단어를 가리킨다(논문의 정의에 따라 다름).(벡터로 생각할 때 (유사성)=-(비유사성) 이므로)

이를 구하는 방법은 3가지이다.

1. Nominal Attribute

object가 같은지 다른지만 설명한다. 즉 0과 1로만 표현된다
```
Nominal = {dissimilarity:[0 if x=y, 1 if x!= y], similarity:[1 if x=y, 0 if x!=y]}
```

2. Ordinal Attribute

두 object 간의 거리(difference)를 계산해서 n-1로 나누어 dissimilarity를 구한다.   
silarity = 1-dissimilarity
n-1로 나누므로 0~1사이의 값을 가지게 된다

```
ordinal = {d:[|x-y|/(n-1)], s:(1-d)}
```

3. (Interval || Ratio) Attribute

두 오브젝트 간의 거리만 계산한다.   
이때 dissimilarity를 어떻게 구하는지에 따라 similarity는 다양하게 표현될 수 있다.

```
Ratio = {d:|x-y|, s1:-d, s2: 1/(1+d), s3: exp(-d), s4:frac{1-(d-min(d))}{max(d)-min(d)}, ...}
```

### 2. 거리
데이터 마이닝에서 거리란, 각 데이터가 얼마나 비슷한지, 얼마나 떨어져 있는지를 의미하며 이는 각 종속변수들 간의 상간관계를 파악하거나 소속을 정하는데 굉장히 중요하게 쓰이는 지표다.   
그러므로 이 거리는 상황에 따라 알맞게 사용되어야하며 거리를 구하는 방법은 각 상황마다 여러 개가 있다. 또, 항상 어떤 상황에 어떤 거리 함수를 써야한다기 보다는 직접 실험해보며 비교하는 것이 바람직하겠다.

**1. Euclidean Distance**   
중학생 때부터 지겹도록 하는 삼각형 빗변의 길이 구하기, 피타고라스 정리와 99% 동일한 거리법이다

%%d = \frac{}{}%%