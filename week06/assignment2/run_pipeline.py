# week06/assignment2/run_pipeline.py
import pandas as pd
from classify import classify_review

def run_pipeline(csv_path: str = "reviews_sample.csv"):
    # CSV 데이터 읽기
    df = pd.read_csv(csv_path)
    
    total_count = len(df)
    success_count = 0
    failure_count = 0
    
    system_prompt = "고객 리뷰를 분석하여 category, sentiment, urgency를 JSON으로 답변하세요."
    
    # reviews_sample.csv의 리뷰 열 이름인 'review_text' 사용 (없을 시 'review' 등 호환)
    review_col = "review_text" if "review_text" in df.columns else "review"

    print(f"=== 파이프라인 실행 시작 (대상 파일: '{csv_path}', 총 {total_count}건) ===")
    
    for idx, row in df.iterrows():
        review_text = str(row[review_col])
        
        # 분류 및 방어 파싱 실행
        result = classify_review(review_text, system_prompt=system_prompt)
        
        # 실패 및 성공 집계
        if result is None:
            failure_count += 1
        else:
            success_count += 1
            
    print("\n==========================================")
    print("           파이프라인 처리 결과           ")
    print("==========================================")
    print(f"총 처리 건수 : {total_count}건")
    print(f"성공 건수     : {success_count}건")
    print(f"실패 건수     : {failure_count}건")
    print("------------------------------------------")
    # 과제 요구사항 핵심 구문
    print(f"처리 {total_count}건 / 실패 {failure_count}건")
    print("==========================================")

if __name__ == "__main__":
    run_pipeline("reviews_sample.csv")