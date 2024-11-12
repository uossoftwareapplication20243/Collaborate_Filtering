import numpy as np
import pandas as pd
import json
import sys
import re
import io
import os

# stdin의 인코딩을 UTF-8로 재설정
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))

def main():
    try:
        # JSON 데이터 직접 로드
        json_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        sys.exit(1)


    """
    input으로 json_data가 들어갑니다. 
    json_data는 username, tag, line 세 가지 정보를 가지고 있습니다.

    이 사이에 파이썬 추가 하시거나 아니면 직접 만드셔도 되고,

    아웃풋으로 champions를 주시면 바로 작동 가능할 것 같습니다.
    """

    
    # 챔피언 정보를 JSON으로 출력
    response_data = {
        "message": "Data received successfully",
        "champions": ['가렌', '갈리오', '갱플랭크']
        # "champions": champions
    }
    if json_data.tag == "KR3":
        response_data.champions = ['알리스타', '브라움', '마오카이']
    
    # ensure_ascii=False를 사용하여 한글이 제대로 출력되도록 함
    print(json.dumps(response_data, ensure_ascii=False))

if __name__ == "__main__":
    main()
