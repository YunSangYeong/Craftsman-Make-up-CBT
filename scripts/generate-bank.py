"""Deterministic transcription of authored material, without scraped exam items.

The original 90 entries keep their IDs, order, answers, and metadata. Each new
manuscript row contributes ONE question; no permutations or numeric variants
are counted as additional questions. Distractors come from the same unit.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://github.com/YunSangYeong/Craftsman-Make-up-CBT/blob/codex/makeup-cbt-standard/scripts/'
REVIEW_NOTE = 'AI 일반 지식으로 자체 작성. 문항·보기·정답·해설의 내부 일관성과 개념 검토. 외부 자료 대조·전문가 검수·공식 출제기준 대조 미완료. 저장소 링크는 작성 위치이며 외부 정답 증빙이 아님.'
RIGHTS = '자체 제작 학습 문항 · CC BY 4.0 · Craftsman-Make-up-CBT contributors. 외부 기출 원문 복제 없음.'


def original_bank():
    rows = []
    subject = ''
    for line in (ROOT / 'scripts/makeup-items.txt').read_text().splitlines():
        if line.startswith('['):
            subject = line[1:-1]
            continue
        if not line:
            continue
        question, correct, *rest = line.split('|')
        wrong, explanation = rest[:3], rest[3]
        number = len(rows) + 1
        position = (number - 1) % 4
        choices = wrong[:]
        choices.insert(position, correct)
        rows.append(dict(
            id=f'MU-{number:03}', subject=subject, topic=question.split(' ')[0],
            question=question, choices=choices, answer=position + 1,
            explanation=explanation, difficulty='하', year=None, session=None,
            type='original', sourceUrl=BASE_URL + 'makeup-items.txt',
            verificationStatus='reviewed', reviewNote=REVIEW_NOTE,
            version='makeup-main', rights=RIGHTS,
        ))
    assert len(rows) == 90, '기존 90문항 원고를 변경하지 마세요.'
    return rows


def authored_units():
    units = []
    for line in (ROOT / 'scripts/makeup-expanded.txt').read_text().splitlines():
        if not line.strip():
            continue
        if line.startswith('['):
            subject, topic = line[1:-1].split('|')
            units.append(dict(subject=subject, topic=topic, items=[]))
        else:
            term, clue = line.split('|')
            units[-1]['items'].append((term, clue))
    assert len(units) == 91
    assert all(len(u['items']) == 10 for u in units)
    return units


def expanded_bank():
    rows = []
    for unit_index, unit in enumerate(authored_units(), 1):
        items = unit['items']
        assert len(set(term for term, _ in items)) == len(items)
        for item_index, (term, clue) in enumerate(items, 1):
            number = 91 + len(rows)
            question_id = f'MU-{number:03}'
            # A stable order ensures adding unrelated material never changes these answers.
            alternatives = sorted(
                (pair for pair in items if pair[0] != term),
                key=lambda pair: hashlib.sha256((question_id + ':' + pair[0]).encode()).digest(),
            )[:3]
            choices = [pair[0] for pair in alternatives]
            position = (number - 1) % 4
            choices.insert(position, term)
            distinction = ' / '.join(f'{other}: {meaning}.' for other, meaning in alternatives)
            rows.append(dict(
                id=question_id, subject=unit['subject'], topic=unit['topic'],
                question=f"{unit['topic']}에 관한 다음 설명에 가장 가까운 것은?\n{clue}.",
                choices=choices, answer=position + 1,
                explanation=f'정답은 {term}입니다. 판단 근거: {clue}. 다른 보기와의 구별: {distinction}',
                difficulty='하', year=None, session=None, type='original',
                sourceUrl=BASE_URL + 'makeup-expanded.txt', verificationStatus='reviewed',
                reviewNote=REVIEW_NOTE + ' 설명 판별형 자체 문항. 같은 단원의 개념·작업을 보기로 비교하며 공식 용어·기출 표현의 재현을 주장하지 않음.',
                version='makeup-main', rights=RIGHTS,
                objectiveId=f'EXP-{unit_index:02}-{item_index:02}',
                learningObjective=f"{unit['topic']}: {term}", authoringTemplate='description-selection-v1',
            ))
    return rows


def normalized(text):
    import unicodedata
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).lower()


def main():
    rows = original_bank() + expanded_bank()
    assert len(rows) == 1000
    assert len({q['id'] for q in rows}) == len(rows)
    assert len({normalized(q['question']) for q in rows}) == len(rows)
    fingerprints = [normalized('|'.join([q['question'], *sorted(q['choices'])])) for q in rows]
    assert len(set(fingerprints)) == len(rows)
    for q in rows:
        assert len(q['choices']) == len(set(map(normalized, q['choices']))) == 4
        assert q['answer'] in (1, 2, 3, 4)
        assert q['year'] is None and q['session'] is None
    (ROOT / 'src/data/questions.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    print('Authored questions:', len(rows), dict(Counter(q['subject'] for q in rows)))


if __name__ == '__main__':
    main()
