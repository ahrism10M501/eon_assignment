def calculator():
    print("계산기가 실행되었습니다")
    
    # 지원하는 계산 지정하기 
    OPERATORS = ['+', '-', '/', '*']
    
    while True:
        if (numbers := input("두 숫자를 입력하세요! ")):
            # 파이썬의 unpack 기능과 comprehension 기능
            # unpack: 어떤 함수의 출력이 2개 이상일 떄, 그 숫자만큼의 변수를 좌항에 넣어 바로바로 뺄 수 있다
            # comprehension: 리스트 안에서 for 문을 이용해 특정 배열을 빠르게 작성 할 수 있다.
            num1, num2 = [float(num) for num in numbers.lower().strip().split(' ')]

            operator = input("연산자를 입력하세요! ")
            
            if operator.strip() == "exit":
                print("계산기를 종료합니다")
                break
            
            elif operator.strip() not in OPERATORS:
                print("지원하지 않는 계산 형식입니다")
                continue
            
            if operator == "+":
                print(f"{num1} + {num2} = {num1+num2}")
                
            if operator == "-":
                print(f"{num1} - {num2} = {num1-num2}")
                
            if operator == "/":
                if num2 is None or num2 == 0:
                    print("0 으로는 나눗셈을 수행할 수 없습니다")
                    continue
                print(f"{num1} / {num2} = {num1/num2}")
                
            if operator == "*":
                print(f"{num1} * {num2} = {num1*num2}")
                
if __name__ == "__main__":
    calculator()