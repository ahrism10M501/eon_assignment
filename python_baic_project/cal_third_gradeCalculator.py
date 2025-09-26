import math
import logging
import random

# 로그 설정
logging.basicConfig(level=logging.INFO)
GRADE_TO_SCORE = {
        'a+': 4.5, 'a': 4.0, 'b+': 3.5, 'b': 3.0,
        'c+': 2.5, 'c': 2.0, 'd+': 1.5, 'd': 1.0,
        'f': 0.0
    }
def grade_to_score_converter(grade: str) -> float:
    
    grade = grade.strip().lower()
    if grade not in GRADE_TO_SCORE:
        raise ValueError(f"잘못된 성적 입력: {grade}")
    return GRADE_TO_SCORE[grade]

def calc_gpa(grades: list) -> float:
    try:
        # 전체 점수
        total_points = sum(grade_to_score_converter(grade.strip()) * credit for grade, credit in grades)
        
        # 전체 학점
        total_credits = sum(credit for _, credit in grades)
        
        # 평균 반환
        return total_points / total_credits if total_credits > 0 else 0.0
    
    except Exception as e:
        logging.error(f"평균 계산 중 오류: {e}")
        return 0.0

def calc_class_avg(scores):
    return sum(scores) / len(scores)

def calc_class_std(scores):
    class_avg = calc_class_avg(scores)
    return math.sqrt(sum((x - class_avg) ** 2 for x in scores) / len(scores))

def input_grades() -> list:
    grades = []
    print("성적과 학점을 입력해주세요 (예: A 3). 종료하려면 'end'를 입력하세요.")
    while True:
        try:
            raw = input().strip()
            if raw.lower() == 'end':
                break

            grade, credit = raw.split()
            credit = int(credit)
            
            # 함수에 입력을 넣어 입력 값이 올바른지 검사, 예외처리 기능 재사용
            score = grade_to_score_converter(grade) 
            grades.append((grade, credit))

        except ValueError as e:
            print(f"입력 오류: {e}")
        except Exception as e:
            print(f"알 수 없는 오류: {e}")
    return grades

def userInputScore() -> list:
    """ 다수 학생 입력 받아 전체 평균과 표준편차 계산 """
    all_scores = []
    while True:
        print("\n--- 학생 성적 입력 ---")
        grades = input_grades()
        if not grades:
            print("입력된 성적이 없습니다.")
            continue

        avg = calc_gpa(grades)
        all_scores.append(avg)
        print(f"학생의 평균 평점(GPA): {avg:.2f}")

        cont = input("다음 학생을 입력하시겠습니까? (Y/n): ").strip().lower()
        if cont == 'n':
            break

    if all_scores:
        return all_scores
    else:
        print("입력된 학생이 없습니다.")
        return []


def make_dummies(n=20, num_lecture:range=range(5, 7)):
    score_to_grade = {v:k for k, v in GRADE_TO_SCORE.items()}
    
    dummies = []
    for _ in range(n):
        dummy = []
        for _ in num_lecture:
            score = score_to_grade[random.choice(list(score_to_grade.keys()))]
            credit = random.randint(2, 3)
            dummy.append([score, credit])
        dummies.append(dummy)
        
    return dummies

def dummyScore(dummies):
    all_scores = []
    for dummy in dummies:
        avg = calc_gpa(dummy)
        all_scores.append(avg)
    return all_scores

def main():
    tech_stat = {'조회':len ,'평균':calc_class_avg, '표준편차':calc_class_std, '최소':min, '최대':max}
    
    dummy = make_dummies(n=100)
    dummy_score = dummyScore(dummy)
    user_input_scores = userInputScore()
    all_scores = dummy_score+user_input_scores
    if not all_scores:
        print("통계를 낼 데이터가 없습니다. 프로그램을 종료합니다.")
        return
    
    print("\n입력이 완료되었습니다.\n통계를 확인할 수 있습니다.\n종료하시려면 종료 를 입력해주세요.")
    print("조회 가능한 통계: ", ', '.join(tech_stat.keys()))
    
    while True:
        selector = input("어떤 통계를 보고 싶으신가요: ").strip()
        if selector.strip() in list(tech_stat.keys()):
            stat = tech_stat[selector](all_scores)
            print(f"{selector}: {stat:.4f}")
            
        elif selector.strip() == "종료":
            print("프로그램을 종료합니다.")
            break
        else:
            print("유효하지 않은 입력입니다")
            print("조회 가능한 통계: ", ', '.join(tech_stat.keys()))
    return
if __name__ == "__main__":
    main()
    
    
