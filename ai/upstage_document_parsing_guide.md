# Upstage Document Parsing API 가이드

## 개요

Document Parsing은 모든 문서를 HTML 또는 마크다운과 같은 구조화된 텍스트로 자동 변환하는 프로세스입니다. 이 API는 문단, 표, 이미지 등의 레이아웃 요소를 감지하여 문서 구조를 파악하고, 읽기 순서에 따라 요소들을 정렬한 후 구조화된 텍스트로 변환합니다.

## 제공 모델

현재 API로 제공되는 모델들은 다음과 같습니다:

| 별칭 | 현재 가리키는 모델 | RPS |
|------|------------------|-----|
| `document-parse` | document-parse-250618 | 10 (동기) / 30 (비동기) |
| `document-parse-nightly` | - | 10 (동기) / 30 (비동기) |

💡 **권장사항**: 모델명을 하드코딩하지 말고 안정적인 별칭(alias)을 사용하는 것을 권장합니다. 이를 통해 한 번 통합하면 향후 업데이트의 이점을 자동으로 받을 수 있습니다.

## 입력 요구사항

### 지원 파일 형식
- JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX, HWP, HWPX

### 제한사항
- **최대 파일 크기**: 50MB
- **페이지당 최대 픽셀수**: 200,000,000 픽셀 (이미지가 아닌 파일의 경우 150 DPI로 변환 후 결정)
- **파일당 최대 페이지 수**:
  - 동기 API: 100페이지 (초과 시 첫 100페이지만 처리)
  - 비동기 API: 1,000페이지

### 지원 문자 집합 (OCR 사용 시)
- **완전 지원**: 영숫자, 한글, 한자
- **베타 버전**: 중국어 간체/번체, 일본어 간지 (사용 가능하지만 완전 지원되지 않음)

### 최적 결과를 위한 가이드라인
- 텍스트 가독성을 위해 고해상도 문서 사용
- 최소 문서 너비 640픽셀 확보
- 이미지 높이의 최소 2.5% 크기로 텍스트 크기 확보 (예: 640픽셀 높이 이미지의 경우 최소 16픽셀 텍스트)

## 출력 이해하기

### 레이아웃 카테고리와 HTML 태그

Upstage Document Parse는 입력 문서에서 다양한 레이아웃 카테고리를 식별하고 이를 HTML 태그로 변환합니다.

| 레이아웃 카테고리 | HTML 태그 |
|-----------------|-----------|
| table | `<table> .. </table>` |
| figure | `<figure><img> .. </img></figure>` |
| chart | `<figure><img data-category="chart"> .. </img></figure>` |
| heading1 | `<h1>... </h1>` |
| header | `<header> .. </header>` |
| footer | `<footer> .. </footer>` |
| caption | `<caption> .. </caption>` |
| paragraph | `<p data-category="paragraph">..</p>` |
| equation | `<p data-category="equation">..</p>` |
| list | `<p data-category="list">..</p>` |

적절한 HTML 태그가 없는 레이아웃 카테고리의 경우, 모델이 감지한 레이아웃 카테고리를 설명하는 `data-category` 속성이 있는 `<p>` 태그를 사용합니다.

### 차트 인식

Document Parse는 다음 차트 유형을 인식하고 표 형식으로 변환할 수 있습니다:

- **막대 차트 (Bar charts)**
- **선 차트 (Line charts)**  
- **파이 차트 (Pie charts)**

#### 차트 인식 결과 구성요소

1. **`<figcaption>`**: 차트 메타데이터 포함
   - 차트 제목
   - X축/Y축 라벨
   - 차트 유형 (bar, line, pie)

2. **`<table>`**: 인식된 차트 데이터를 표 형식으로 제공

#### 차트 인식 예시

**차트 인식 성공 시**:
```json
{
  "category": "chart",
  "content": {
    "html": "<figure id='4' data-category='chart'><img data-coord=\"top-left:(175,1305); bottom-right:(785,1784)\" /><figcaption><p>Chart Type: bar</p></figcaption><table><tr><th></th><th>Nuclear</th><th>Renewables</th><th>Hydro</th><th>Natural gas</th><th>Coal</th><th>Oil</th></tr><tr><td>item_01</td><td>4%</td><td>4%</td><td>7%</td><td>24%</td><td>27%</td><td>34%</td></tr></table></figure>",
    "markdown": "- Chart Type: bar\n|  | Nuclear | Renewables | Hydro | Natural gas | Coal | Oil |\n| --- | --- | --- | --- | --- | --- | --- |\n| item_01 | 4% | 4% | 7% | 24% | 27% | 34% |\n",
    "text": "Chart Type: bar Nuclear Renewables Hydro Natural gas Coal Oil item_01 4% 4% 7% 24% 27% 34%"
  }
}
```

**차트 인식 실패 시**: 차트는 `figure`로 분류되고 응답에는 HTML, 마크다운, 텍스트가 포함됩니다.

### 수식 인식

수식의 경우 응답의 `content.html`과 `content.markdown` 필드에 LaTeX 형식으로 인식된 수식이 포함되며, `content.text` 필드에는 OCR 결과 텍스트가 포함됩니다.

⚠️ **주의**: OCR 모델은 현재 수식 인식을 지원하지 않으므로 `content.text` 필드에는 정확한 수식 텍스트가 포함되지 않을 수 있습니다.

#### HTML에서 수식 렌더링

API 응답이 JSON 형식에서 `\` 문자를 이스케이프하므로, HTML 파일에서 수식을 제대로 렌더링하려면 JavaScript를 사용하여 이스케이프를 해제해야 합니다:

```html
<!DOCTYPE html>
<html>
<head>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script type="text/javascript">
        <!-- API 응답을 innerHTML 필드에 입력 -->
        document.getElementById('equation').innerHTML = "<p id='5' data-category='equation'>$$f(x)=a_{0}+\\sum_{n=1}^{\\infty}\\left[a_{n}\\cos\\left(\\frac{n\\pi x}{L}\\right)+b_{n}\\sin\\left(\\frac{n\\pi x}{L}\\right)\\right]$$</p>";
    </script>
</head>
<body>
    <div id="equation"></div>
</body>
</html>
```

## 주요 특징

### ✅ 무료 체험
- HTML 또는 마크다운으로 문서 변환
- 샘플 파일 또는 사용자 파일 사용 가능
- API 키 없이 무료 체험 가능

### 🔧 차트 정보 활용
차트를 이미지로만 파싱하는 대신, 수치 데이터를 표 형식으로 추출하여 기존 텍스트 기반 파이프라인에 원활하게 통합할 수 있습니다. 이를 통해 검색, QA, RAG 등의 작업에서 차트 정보를 효과적으로 활용할 수 있습니다.

### 📊 구조화된 출력
- **HTML**: 완전한 구조화된 마크업
- **마크다운**: 가독성 높은 텍스트 형식
- **텍스트**: 순수 텍스트 추출

## 사용 시나리오

1. **문서 디지털화**: 물리적 문서를 구조화된 디지털 형식으로 변환
2. **콘텐츠 관리**: 다양한 형식의 문서를 통일된 구조로 관리
3. **데이터 추출**: 차트와 표에서 구조화된 데이터 추출
4. **검색 최적화**: 문서 내용을 검색 가능한 형태로 변환
5. **AI 파이프라인**: RAG, QA 시스템 등에서 문서 전처리

---

*이 가이드는 Upstage Console API 문서를 기반으로 작성되었습니다.*
# Upstage Document Parsing API 가이드

## 개요

Document Parsing은 모든 문서를 HTML 또는 마크다운과 같은 구조화된 텍스트로 자동 변환하는 프로세스입니다. 이 API는 문단, 표, 이미지 등의 레이아웃 요소를 감지하여 문서 구조를 파악하고, 읽기 순서에 따라 요소들을 정렬한 후 구조화된 텍스트로 변환합니다.

## 제공 모델

현재 API로 제공되는 모델들은 다음과 같습니다:

| 별칭 | 현재 가리키는 모델 | RPS |
|------|------------------|-----|
| `document-parse` | document-parse-250618 | 10 (동기) / 30 (비동기) |
| `document-parse-nightly` | - | 10 (동기) / 30 (비동기) |

💡 **권장사항**: 모델명을 하드코딩하지 말고 안정적인 별칭(alias)을 사용하는 것을 권장합니다. 이를 통해 한 번 통합하면 향후 업데이트의 이점을 자동으로 받을 수 있습니다.

## 입력 요구사항

### 지원 파일 형식
- JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX, HWP, HWPX

### 제한사항
- **최대 파일 크기**: 50MB
- **페이지당 최대 픽셀수**: 200,000,000 픽셀 (이미지가 아닌 파일의 경우 150 DPI로 변환 후 결정)
- **파일당 최대 페이지 수**:
  - 동기 API: 100페이지 (초과 시 첫 100페이지만 처리)
  - 비동기 API: 1,000페이지

### 지원 문자 집합 (OCR 사용 시)
- **완전 지원**: 영숫자, 한글, 한자
- **베타 버전**: 중국어 간체/번체, 일본어 간지 (사용 가능하지만 완전 지원되지 않음)

### 최적 결과를 위한 가이드라인
- 텍스트 가독성을 위해 고해상도 문서 사용
- 최소 문서 너비 640픽셀 확보
- 이미지 높이의 최소 2.5% 크기로 텍스트 크기 확보 (예: 640픽셀 높이 이미지의 경우 최소 16픽셀 텍스트)

## 출력 이해하기

### 레이아웃 카테고리와 HTML 태그

Upstage Document Parse는 입력 문서에서 다양한 레이아웃 카테고리를 식별하고 이를 HTML 태그로 변환합니다.

| 레이아웃 카테고리 | HTML 태그 |
|-----------------|-----------|
| table | `<table> .. </table>` |
| figure | `<figure><img> .. </img></figure>` |
| chart | `<figure><img data-category="chart"> .. </img></figure>` |
| heading1 | `<h1>... </h1>` |
| header | `<header> .. </header>` |
| footer | `<footer> .. </footer>` |
| caption | `<caption> .. </caption>` |
| paragraph | `<p data-category="paragraph">..</p>` |
| equation | `<p data-category="equation">..</p>` |
| list | `<p data-category="list">..</p>` |

적절한 HTML 태그가 없는 레이아웃 카테고리의 경우, 모델이 감지한 레이아웃 카테고리를 설명하는 `data-category` 속성이 있는 `<p>` 태그를 사용합니다.

### 차트 인식

Document Parse는 다음 차트 유형을 인식하고 표 형식으로 변환할 수 있습니다:

- **막대 차트 (Bar charts)**
- **선 차트 (Line charts)**  
- **파이 차트 (Pie charts)**

#### 차트 인식 결과 구성요소

1. **`<figcaption>`**: 차트 메타데이터 포함
   - 차트 제목
   - X축/Y축 라벨
   - 차트 유형 (bar, line, pie)

2. **`<table>`**: 인식된 차트 데이터를 표 형식으로 제공

#### 차트 인식 예시

**차트 인식 성공 시**:
```json
{
  "category": "chart",
  "content": {
    "html": "<figure id='4' data-category='chart'><img data-coord=\"top-left:(175,1305); bottom-right:(785,1784)\" /><figcaption><p>Chart Type: bar</p></figcaption><table><tr><th></th><th>Nuclear</th><th>Renewables</th><th>Hydro</th><th>Natural gas</th><th>Coal</th><th>Oil</th></tr><tr><td>item_01</td><td>4%</td><td>4%</td><td>7%</td><td>24%</td><td>27%</td><td>34%</td></tr></table></figure>",
    "markdown": "- Chart Type: bar\n|  | Nuclear | Renewables | Hydro | Natural gas | Coal | Oil |\n| --- | --- | --- | --- | --- | --- | --- |\n| item_01 | 4% | 4% | 7% | 24% | 27% | 34% |\n",
    "text": "Chart Type: bar Nuclear Renewables Hydro Natural gas Coal Oil item_01 4% 4% 7% 24% 27% 34%"
  }
}
```

**차트 인식 실패 시**: 차트는 `figure`로 분류되고 응답에는 HTML, 마크다운, 텍스트가 포함됩니다.

### 수식 인식

수식의 경우 응답의 `content.html`과 `content.markdown` 필드에 LaTeX 형식으로 인식된 수식이 포함되며, `content.text` 필드에는 OCR 결과 텍스트가 포함됩니다.

⚠️ **주의**: OCR 모델은 현재 수식 인식을 지원하지 않으므로 `content.text` 필드에는 정확한 수식 텍스트가 포함되지 않을 수 있습니다.

#### HTML에서 수식 렌더링

API 응답이 JSON 형식에서 `\` 문자를 이스케이프하므로, HTML 파일에서 수식을 제대로 렌더링하려면 JavaScript를 사용하여 이스케이프를 해제해야 합니다:

```html
<!DOCTYPE html>
<html>
<head>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script type="text/javascript">
        <!-- API 응답을 innerHTML 필드에 입력 -->
        document.getElementById('equation').innerHTML = "<p id='5' data-category='equation'>$$f(x)=a_{0}+\\sum_{n=1}^{\\infty}\\left[a_{n}\\cos\\left(\\frac{n\\pi x}{L}\\right)+b_{n}\\sin\\left(\\frac{n\\pi x}{L}\\right)\\right]$$</p>";
    </script>
</head>
<body>
    <div id="equation"></div>
</body>
</html>
```

## 주요 특징

### ✅ 무료 체험
- HTML 또는 마크다운으로 문서 변환
- 샘플 파일 또는 사용자 파일 사용 가능
- API 키 없이 무료 체험 가능

### 🔧 차트 정보 활용
차트를 이미지로만 파싱하는 대신, 수치 데이터를 표 형식으로 추출하여 기존 텍스트 기반 파이프라인에 원활하게 통합할 수 있습니다. 이를 통해 검색, QA, RAG 등의 작업에서 차트 정보를 효과적으로 활용할 수 있습니다.

### 📊 구조화된 출력
- **HTML**: 완전한 구조화된 마크업
- **마크다운**: 가독성 높은 텍스트 형식
- **텍스트**: 순수 텍스트 추출

## 사용 시나리오

1. **문서 디지털화**: 물리적 문서를 구조화된 디지털 형식으로 변환
2. **콘텐츠 관리**: 다양한 형식의 문서를 통일된 구조로 관리
3. **데이터 추출**: 차트와 표에서 구조화된 데이터 추출
4. **검색 최적화**: 문서 내용을 검색 가능한 형태로 변환
5. **AI 파이프라인**: RAG, QA 시스템 등에서 문서 전처리

---

Structured outputs
What is structured outputs?
Structured outputs enable users to extract and organize information in a standardized format by generating a JSON string based on a provided JSON schema. This feature ensures that extracted data is both machine-readable and easily integrable into various applications.

What models does Upstage provide?
The table below lists models currently available as an API. Upstage provides stable aliases that point to specific model versions, allowing you to integrate once and automatically benefit from future updates. We recommend using aliases instead of hardcoding model names, as models can be frequently updated.

Alias	Currently points to	RPM / TPM (Learn more)
solar-pro2	solar-pro2-250710	100 / 100,000
solar-mini	solar-mini-250422	100 / 100,000

Examples
Example: Extract key information from an HTML string
Request

```
# pip install openai
 
from openai import OpenAI  # openai==1.52.2
 
client = OpenAI(
    api_key="UPSTAGE_API_KEY",
    base_url="https://api.upstage.ai/v1"
)
 
messages=[
    {
        "role": "system",
        "content": "You are an expert in information extraction. Extract information from the given HTML representation of image and organize them into a clear and accurate JSON format."
    },
    {
        "role": "user",
        "content": "HTML string: <table id='0' style='font-size:14px'><tr><td>1</td><td>FUTAMI 17 GREEN TEA (CLAS</td><td>12,500</td></tr><tr><td>1</td><td>EGG TART</td><td>13,000</td></tr><tr><td>1</td><td>GRAIN CROQUE MONSIEUR</td><td>17,000</td></tr></table><br><table id='1' style='font-size:18px'><tr><td>TOTAL</td><td>42, 500</td></tr><tr><td>CASH</td><td>50,000</td></tr><tr><td></td><td></td></tr><tr><td>CHANGE</td><td>7 ,500</td></tr></table>\n. Extract the structured data from the HTML string in JSON format."
    }
]
 
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": "restaurant_receipt",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "menu_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "menu_cnt": {
                                "type": "number",
                                "description": "The count of the menu item."
                            },
                            "menu_name": {
                                "type": "string",
                                "description": "The name of the menu item."
                            },
                            "menu_price": {
                                "type": "number",
                                "description": "The price of the menu item."
                            }
                        },
                        "required": ["menu_cnt", "menu_name", "menu_price"],
                    }
                },
                "total_price": {
                    "type": "number",
                    "description": "The total price of the receipt."
                }
            },
            "required": ["menu_items", "total_price"],
        }
    }
}
 
response = client.chat.completions.create(
    model="solar-pro2",
    messages=messages,
    response_format=response_format
)
 
print(response.choices[0].message.content)
```