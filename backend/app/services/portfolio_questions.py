import uuid
from typing import List

def get_portfolio_based_questions(portfolio_text: str, keywords: List[str]) -> List:
    """포트폴리오 기반 맞춤형 질문 생성 - 항상 개인화된 질문만 생성"""
    print(f"Generating personalized questions with keywords: {keywords}")
    print(f"Portfolio text preview: {portfolio_text[:200]}...")
    
    # 포트폴리오 텍스트에서 추가 정보 추출
    portfolio_lower = portfolio_text.lower()
    has_team_project = any(word in portfolio_lower for word in ['팀', 'team', '협업', '함께', '그룹'])
    has_performance = any(word in portfolio_lower for word in ['성능', '최적화', '속도', '개선', 'performance'])
    has_database = any(word in portfolio_lower for word in ['데이터베이스', 'database', 'db', 'mysql', 'mongodb'])
    has_api = any(word in portfolio_lower for word in ['api', 'rest', '서버', 'server', 'backend'])
    has_frontend = any(word in portfolio_lower for word in ['프론트', 'frontend', 'react', 'vue', 'angular', 'ui'])
    
    # 키워드 기반 질문 템플릿 (더 구체적이고 개인화된 질문)
    keyword_questions = {
        'Java': {
            'title': 'Java 프로젝트 경험',
            'content': 'Java를 사용한 프로젝트에서 가장 인상 깊었던 경험은 무엇인가요? 어떤 기능을 구현했고, 어떤 어려움이 있었나요?',
            'category': 'Java Development',
            'difficulty': 'Medium',
            'time': 5
        },
        'Spring': {
            'title': 'Spring 프레임워크 활용',
            'content': 'Spring 프레임워크를 사용하면서 가장 유용했던 기능이나 어노테이션은 무엇인가요? 구체적인 사용 사례를 설명해주세요.',
            'category': 'Spring Framework',
            'difficulty': 'Medium',
            'time': 4
        },
        'React': {
            'title': 'React 컴포넌트 설계',
            'content': 'React로 개발한 프로젝트에서 컴포넌트 구조를 어떻게 설계했나요? 상태 관리나 라이프사이클 관리에서 고려한 점이 있다면 설명해주세요.',
            'category': 'React Development',
            'difficulty': 'Medium',
            'time': 4
        },
        'JavaScript': {
            'title': 'JavaScript 비동기 처리 경험',
            'content': 'JavaScript에서 비동기 처리를 다루면서 마주쳤던 문제와 해결 방법에 대해 설명해주세요. Promise, async/await 사용 경험도 포함해주세요.',
            'category': 'JavaScript Development',
            'difficulty': 'Medium',
            'time': 4
        },
        'Node.js': {
            'title': 'Node.js 서버 개발 경험',
            'content': 'Node.js로 서버를 개발하면서 가장 중요하게 생각한 부분은 무엇인가요? 성능, 보안, 에러 처리 등에서 고려한 점을 설명해주세요.',
            'category': 'Node.js Development',
            'difficulty': 'Medium',
            'time': 5
        },
        'Python': {
            'title': 'Python 프로젝트 경험',
            'content': 'Python으로 개발한 프로젝트에서 어떤 라이브러리나 프레임워크를 사용했나요? 선택 이유와 사용 경험을 설명해주세요.',
            'category': 'Python Development',
            'difficulty': 'Medium',
            'time': 4
        },
        'MySQL': {
            'title': 'MySQL 데이터베이스 설계',
            'content': 'MySQL을 사용한 프로젝트에서 데이터베이스 스키마를 어떻게 설계했나요? 정규화나 인덱스 최적화 경험이 있다면 설명해주세요.',
            'category': 'Database Design',
            'difficulty': 'Hard',
            'time': 5
        },
        'MongoDB': {
            'title': 'MongoDB NoSQL 경험',
            'content': 'MongoDB를 선택한 이유와 사용 경험에 대해 설명해주세요. 관계형 데이터베이스와 비교해서 어떤 장단점을 느꼈나요?',
            'category': 'NoSQL Database',
            'difficulty': 'Medium',
            'time': 4
        },
        'AWS': {
            'title': 'AWS 클라우드 서비스 활용',
            'content': 'AWS에서 어떤 서비스들을 사용해보셨나요? 배포나 인프라 관리에서 경험한 어려움이나 해결 방법을 설명해주세요.',
            'category': 'Cloud Services',
            'difficulty': 'Hard',
            'time': 5
        },
        'Docker': {
            'title': 'Docker 컨테이너화 경험',
            'content': 'Docker를 사용한 이유와 컨테이너화 과정에서 경험한 장점을 설명해주세요. Dockerfile 작성이나 이미지 최적화 경험이 있다면 포함해주세요.',
            'category': 'DevOps',
            'difficulty': 'Medium',
            'time': 4
        },
        'Git': {
            'title': 'Git 버전 관리 경험',
            'content': 'Git을 사용한 협업 경험에 대해 설명해주세요. 브랜치 전략이나 충돌 해결, 코드 리뷰 과정에서 경험한 점을 포함해주세요.',
            'category': 'Version Control',
            'difficulty': 'Easy',
            'time': 3
        }
    }
    
    portfolio_questions = []
    
    # 키워드 기반 질문 추가
    for keyword in keywords[:6]:  # 상위 6개 키워드
        if keyword in keyword_questions:
            template = keyword_questions[keyword]
            portfolio_questions.append({
                'id': str(uuid.uuid4()),
                'title': template['title'],
                'content': template['content'],
                'category': template['category'],
                'difficulty': template['difficulty'],
                'estimated_time': template['time']
            })
    
    # 포트폴리오 내용 기반 추가 질문
    portfolio_based = [
        {
            'title': '포트폴리오 프로젝트 소개',
            'content': f'포트폴리오에 언급된 프로젝트 중 가장 자랑스러운 프로젝트를 소개해주세요. 사용한 기술: {", ".join(keywords[:3]) if keywords else "기술 스택"}',
            'category': 'Portfolio Project',
            'difficulty': 'Easy',
            'time': 4
        },
        {
            'title': '기술 스택 선택 배경',
            'content': f'포트폴리오에서 {keywords[0] if keywords else "기술 스택"}을 선택한 이유는 무엇인가요? 다른 대안도 고려해보셨나요?',
            'category': 'Technical Decision',
            'difficulty': 'Medium',
            'time': 4
        },
        {
            'title': '프로젝트 성과 및 배운 점',
            'content': '포트폴리오 프로젝트를 통해 얻은 가장 큰 성과나 배운 점은 무엇인가요? 정량적인 결과가 있다면 포함해주세요.',
            'category': 'Project Outcome',
            'difficulty': 'Medium',
            'time': 5
        },
        {
            'title': '협업 및 코드 리뷰 경험',
            'content': '포트폴리오 프로젝트에서 팀원들과 어떻게 협업했나요? 코드 리뷰나 페어 프로그래밍 경험이 있다면 설명해주세요.',
            'category': 'Team Collaboration',
            'difficulty': 'Easy',
            'time': 3
        }
    ]
    
    # 기본 질문과 포트폴리오 기반 질문 결합
    for q in portfolio_based:
        if len(portfolio_questions) >= 10:
            break
        portfolio_questions.append({
            'id': str(uuid.uuid4()),
            'title': q['title'],
            'content': q['content'],
            'category': q['category'],
            'difficulty': q['difficulty'],
            'estimated_time': q['time']
        })
    
    # 포트폴리오 내용 기반 추가 개인화 질문들
    additional_personalized_questions = []
    
    if has_team_project:
        additional_personalized_questions.append({
            'title': '팀 프로젝트에서의 역할과 기여',
            'content': f'포트폴리오에 언급된 팀 프로젝트에서 본인의 구체적인 역할은 무엇이었나요? {keywords[0] if keywords else "기술적"} 측면에서 어떤 기여를 했나요?',
            'category': 'Team Leadership',
            'difficulty': 'Medium',
            'time': 4
        })
    
    if has_performance:
        additional_personalized_questions.append({
            'title': '성능 개선 경험과 측정 방법',
            'content': f'포트폴리오에서 언급한 성능 개선 경험에 대해 자세히 설명해주세요. {keywords[0] if keywords else "어떤 기술"}을 사용해서 어떤 지표가 얼마나 개선되었나요?',
            'category': 'Performance Optimization',
            'difficulty': 'Hard',
            'time': 5
        })
    
    if has_database:
        additional_personalized_questions.append({
            'title': '데이터베이스 설계 및 쿼리 최적화',
            'content': f'포트폴리오 프로젝트에서 데이터베이스를 어떻게 설계했나요? {"MySQL" if "mysql" in portfolio_lower else "MongoDB" if "mongodb" in portfolio_lower else "데이터베이스"}를 선택한 이유와 최적화 경험을 설명해주세요.',
            'category': 'Database Design',
            'difficulty': 'Hard',
            'time': 5
        })
    
    if has_api:
        additional_personalized_questions.append({
            'title': 'API 설계 및 백엔드 아키텍처',
            'content': f'포트폴리오에서 개발한 API나 백엔드 시스템의 아키텍처를 설명해주세요. {keywords[0] if keywords else "어떤 기술"}을 사용했고, 어떤 설계 원칙을 따랐나요?',
            'category': 'Backend Architecture',
            'difficulty': 'Hard',
            'time': 5
        })
    
    if has_frontend:
        additional_personalized_questions.append({
            'title': '프론트엔드 사용자 경험 개선',
            'content': f'포트폴리오의 프론트엔드 개발에서 사용자 경험을 어떻게 개선했나요? {"React" if "react" in portfolio_lower else "Vue" if "vue" in portfolio_lower else "프론트엔드 기술"}을 사용한 구체적인 사례를 설명해주세요.',
            'category': 'Frontend UX',
            'difficulty': 'Medium',
            'time': 4
        })
    
    # 키워드 기반 심화 질문들
    for i, keyword in enumerate(keywords[:3]):
        additional_personalized_questions.append({
            'title': f'{keyword} 기술 심화 경험',
            'content': f'포트폴리오에서 {keyword}를 사용하면서 가장 도전적이었던 부분은 무엇인가요? 이 기술을 선택한 이유와 사용하면서 얻은 인사이트를 공유해주세요.',
            'category': f'{keyword} Deep Dive',
            'difficulty': 'Hard',
            'time': 5
        })
    
    # 프로젝트 결과 및 임팩트 관련 질문들
    impact_questions = [
        {
            'title': '프로젝트 임팩트 및 사용자 피드백',
            'content': f'포트폴리오 프로젝트가 실제 사용자나 비즈니스에 어떤 임팩트를 주었나요? 구체적인 수치나 피드백이 있다면 공유해주세요.',
            'category': 'Business Impact',
            'difficulty': 'Medium',
            'time': 4
        },
        {
            'title': '기술적 의사결정과 트레이드오프',
            'content': f'포트폴리오 프로젝트에서 중요한 기술적 의사결정을 내려야 했던 순간이 있나요? {keywords[0] if keywords else "어떤 기술"} 선택에서 고려한 트레이드오프를 설명해주세요.',
            'category': 'Technical Decision',
            'difficulty': 'Hard',
            'time': 5
        },
        {
            'title': '코드 품질 및 유지보수성',
            'content': f'포트폴리오 프로젝트에서 코드 품질을 어떻게 관리했나요? {keywords[0] if keywords else "사용한 기술"}에서 클린 코드나 리팩토링 경험을 설명해주세요.',
            'category': 'Code Quality',
            'difficulty': 'Medium',
            'time': 4
        }
    ]
    
    # 추가 질문들을 포트폴리오 질문 리스트에 추가
    for q in additional_personalized_questions + impact_questions:
        if len(portfolio_questions) >= 10:
            break
        portfolio_questions.append({
            'id': str(uuid.uuid4()),
            'title': q['title'],
            'content': q['content'],
            'category': q['category'],
            'difficulty': q['difficulty'],
            'estimated_time': q['time']
        })
    
    # 정확히 10개가 되도록 보장 - 포트폴리오 기반 개인화 질문만 사용
    if len(portfolio_questions) < 10:
        # 부족한 만큼 키워드 기반 심화 질문 추가
        remaining = 10 - len(portfolio_questions)
        
        # 추가 심화 질문 풀
        deep_questions = []
        for keyword in keywords:
            deep_questions.extend([
                {
                    'title': f'{keyword} 심화 경험',
                    'content': f'포트폴리오에서 {keyword}를 사용하면서 가장 인상 깊었던 기능이나 문제는 무엇이었나요? 어떻게 해결하거나 구현하셨나요?',
                    'category': f'{keyword} Advanced',
                    'difficulty': 'Hard',
                    'time': 5
                },
                {
                    'title': f'{keyword} 프로젝트 성과',
                    'content': f'{keyword}를 활용한 프로젝트의 구체적인 성과나 임팩트는 무엇이었나요? 사용자나 비즈니스 관점에서 어떤 가치를 제공했나요?',
                    'category': f'{keyword} Impact',
                    'difficulty': 'Medium',
                    'time': 4
                }
            ])
        
        # 일반적인 심화 질문들
        general_deep_questions = [
            {
                'title': '포트폴리오 프로젝트의 아키텍처 설계',
                'content': f'포트폴리오의 가장 복잡한 프로젝트에서 시스템 아키텍처를 어떻게 설계하셨나요? {keywords[0] if keywords else "주요 기술"}을 선택한 이유와 대안 기술들을 비교 설명해주세요.',
                'category': 'System Architecture',
                'difficulty': 'Hard',
                'time': 6
            },
            {
                'title': '포트폴리오 프로젝트의 협업과 리더십',
                'content': '포트폴리오 프로젝트에서 팀원들과 어떻게 협업하고 소통하셨나요? 기술적 의사결정에서 리더십을 발휘한 경험이 있다면 설명해주세요.',
                'category': 'Leadership & Collaboration',
                'difficulty': 'Medium',
                'time': 4
            },
            {
                'title': '포트폴리오 프로젝트의 학습과 성장',
                'content': '포트폴리오 프로젝트를 통해 가장 많이 성장한 부분은 무엇인가요? 이 경험이 현재 개발자로서의 역량에 어떤 영향을 주었나요?',
                'category': 'Personal Growth',
                'difficulty': 'Medium',
                'time': 4
            }
        ]
        
        # 사용할 수 있는 모든 질문들
        available_questions = deep_questions + general_deep_questions
        
        # 부족한 만큼 추가
        for i in range(min(remaining, len(available_questions))):
            q = available_questions[i]
            portfolio_questions.append({
                'id': str(uuid.uuid4()),
                'title': q['title'],
                'content': q['content'],
                'category': q['category'],
                'difficulty': q['difficulty'],
                'estimated_time': q['time']
            })
    
    final_questions = portfolio_questions[:10]
    
    # 10개가 안 되면 에러 발생
    if len(final_questions) < 10:
        raise Exception(f"포트폴리오 기반 질문을 충분히 생성할 수 없습니다. (생성된 질문: {len(final_questions)}/10) 더 자세한 포트폴리오를 업로드해주세요.")
    
    print(f"Generated {len(final_questions)} personalized questions based on portfolio")
    for i, q in enumerate(final_questions):
        print(f"  {i+1}. [{q['category']}] {q['title']}")
    
    return final_questions