'''
# 과하게 설계된(Over-Engineered) 콘솔 계산기 구현

이 프로젝트는 파이썬의 기본 사칙연산과 몇 가지 추가 연산(몫, 나머지, 거듭제곱)을
수행하는 콘솔 기반 계산기입니다.

---

## 1. 함수 분리와 책임 할당 (함수형 패턴)
객체지향 프로그래밍(OOP)의 기초를 다지기 위한 함수형 프로그래밍 패턴을 적용했습니다.
모든 단일 연산(더하기, 빼기 등)은 독립된 함수로 분리됩니다.
이는 단일 책임 원칙(SRP)을 따르기 위한 기초 작업이며,
연산 로직을 캡슐화하고 재사용성을 높입니다.
(다만, 현재 규모에서는 명백한 오버엔지니어링입니다)

* `adder`, `subber`, `multiculator`, `divider`, `remainder`, `floor_divider`, `power`:
    각각 하나의 연산만 책임지는 함수들입니다.
* `calculator`: 연산 기호와 연산 함수를 연결하는 딕셔너리(`OPERATOR`)를 사용하여,
    사용자의 입력에 따라 해당 연산 함수를 동적으로 호출하는 '위임' 역할을 담당합니다.

---

## 2. 출력 및 변수 관리
변수의 효율적인 사용과 출력을 통해 사용자 경험을 개선합니다.

* `ans` 변수: 이전 계산 결과를 저장하여 다음 계산의 피연산자로 활용할 수 있도록 합니다.
    (`ans + 5`, `10 * ans`와 같은 형태로 사용 가능)
* 표준 입출력: `while` 루프와 `input()` 함수를 사용해 지속적인 사용자 입력을 받으며,
    `print()` 함수를 통해 계산 결과(`result`)와 상태 메시지(오류, ans 값)를 명확하게 출력합니다.

---

## 3. 강력한 예외 처리
안정성을 높이기 위해 다양한 입력 상황에 대한 예외 처리를 구현했습니다.

* `try-except` 블록을 사용하여 0으로 나누는 오류(`ZeroDivisionError` 대신 `ValueError`를 발생시켜 처리)나,
    잘못된 형식의 입력(`float` 변환 오류), 지원하지 않는 연산자 입력 등의 오류를 사용자에게 친절하게 알립니다.
* 연산자 우선순위는 고려하지 않으며, *장 먼저 발견된 연산자를 기준으로 좌우 두 개의 숫자만 계산합니다.
    (예: "1+2+3" 입력 시 "1+2"만 계산)

(제미나이가 대본 하난 기가 막힌다)
'''


# 사칙연산 및 기타 연산을 위한 함수들 정의
def adder(num1, num2):
    """더하기 함수"""
    return num1 + num2

def subber(num1, num2):
    """빼기 함수"""
    return num1 - num2

def multiculator(num1, num2):
    """곱하기 함수"""
    return num1 * num2

def divider(num1, num2):
    """나누기 함수"""
    if num2 == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return num1 / num2

def remainder(num1, num2):
    """나머지 연산 (%)"""
    if num2 == 0:
        raise ValueError("0으로 나눌 수 없습니다 (나머지 연산)")
    return num1 % num2

def floor_divider(num1, num2):
    """몫 연산 (//, 정수 나누기)"""
    if num2 == 0:
        raise ValueError("0으로 나눌 수 없습니다 (몫 연산)")
    return num1 // num2

def power(num1, num2):
    """거듭제곱 연산 (**)"""
    return num1 ** num2

# 함수를 동적으로 호출하는 계산기 함수
def calculator(operator, num1, num2):
    # 연산 기호(키)와 해당 연산을 수행하는 함수(값)를 연결한 딕셔너리
    # 파이썬에서 '함수 이름' 자체가 해당 함수를 참조하는 변수처럼 사용됨
    OPERATOR = {
        '+': adder,
        '-': subber,
        '*': multiculator,
        '/': divider,
        '%': remainder,
        '//': floor_divider,
        '**': power
    }
    
    # 딕셔너리에 해당 연산자가 있는지 확인
    if operator in OPERATOR:
        # 연산자 기호에 해당하는 함수를 찾아서 (num1, num2) 인수로 호출하고 결과 반환
        return OPERATOR[operator](num1, num2)
    else:
        # 지원하지 않는 연산 기호일 경우 예외 발생
        raise ValueError(f"지원하지 않는 연산자입니다: {operator}")

# print(f"10 + 5 = {calculator('+', 10, 5)}")
# print(f"10 - 5 = {calculator('-', 10, 5)}")
# print(f"10 * 5 = {calculator('*', 10, 5)}")

if __name__ == "__main__":
    OPERATOR_SYMBOLS = ['//', '**', '+', '-', '*', '/', '%']
    ans = 0
    
    print("계산기 시작!\n", end="")
    
    while True:
        # 입력
        order = input("입력: ").strip()
        
        # 종료하기, exit 말고도 Ctrl+C 도 가능
        if order.lower() == 'exit':
            break
        
        found_operator = None
        
        # 문자열 안에서 처음으로 나오는 연산자 찾기
        for op in OPERATOR_SYMBOLS:
            if op in order:
                found_operator = op
                break
        
        # 예외 처리를 위한 try-except 구문
        try:
            if not found_operator:
                if order.lower() == 'ans':
                    print(f'현재 ans 값: {ans}')
                    continue
                raise ValueError("연산자를 찾지 못했습니다.")
            
            # 문자열을 연산자 기준 좌, 우로 나누기
            numbers = order.split(found_operator)
            
            # 우리는 한 번에 두 숫자만 계산할 것이다
            if len(numbers) != 2:
                raise ValueError("너무 많은 값이 주어졌습니다")
            
            # 특별한 기능 ans를 위해 해당 값을 검사한다.
            # 숙제: 아래 ans인지 검사하고 값을 할당하는 로직을 함수로 만들어오기
            pos1 = numbers[0].strip().lower()
            if pos1 == 'ans':
                num1 = ans
            elif pos1 == '':
                raise ValueError("연산 가능한 형식이 아닙니다")
            else:
                num1 = float(pos1.strip())
            
            pos2 = numbers[1].strip().lower()
            if pos2 == 'ans':
                num2 = ans
            elif pos2 == '':
                raise ValueError("연산 가능한 형식이 아닙니다")
            else:
                num2 = float(pos2.strip())
            
            result = calculator(found_operator, num1, num2)
            ans = result
            print(f'계산 결과: {result}')
            
        except ValueError as e:
            # calculator 함수에서 발생한 0으로 나누는 오류나, float 변환 오류 등을 처리합니다.
            print(f"오류 발생: {e}")
            
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
            
'''
(venv) PS Coding/EON_> & C:Coding/EON_/venv/Scripts/python.exe cCoding/EON_/python_baic_project/calculator.py
계산기 시작!
입력: 10 ** 2
계산 결과: 100.0
입력: 100 ** 2
계산 결과: 10000.0
입력: 100-2
계산 결과: 98.0
입력: 10 % 2
계산 결과: 0.0
입력: 124**2
계산 결과: 15376.0
입력: ans//2
계산 결과: 7688.0
입력: 1/ans
계산 결과: 0.00013007284079084288
'''