"""Deterministic transcription of original manuscript; no scraped material."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rows=[]; subject=''; number=0
for line in (root/'scripts/makeup-items.txt').read_text().splitlines():
 if line.startswith('['):subject=line[1:-1];continue
 if not line:continue
 question,correct,*rest=line.split('|'); wrong=rest[:3]; explanation=rest[3]
 number+=1; position=(number-1)%4
 choices=wrong[:];choices.insert(position,correct)
 rows.append(dict(id=f'MU-{number:03}',subject=subject,topic=question.split(' ')[0],question=question,choices=choices,answer=position+1,explanation=explanation,difficulty='하',year=None,session=None,type='original',sourceUrl='https://github.com/YunSangYeong/Craftsman-Make-up-CBT/blob/codex/makeup-cbt-standard/scripts/makeup-items.txt',verificationStatus='reviewed',reviewNote='AI 일반 지식으로 자체 작성. 문항·보기·정답·해설의 내부 일관성과 개념 검토. 외부 자료 대조·전문가 검수·공식 출제기준 대조 미완료. 저장소 링크는 작성 위치이며 외부 정답 증빙이 아님.',version='makeup-main',rights='자체 제작 학습 문항 · CC BY 4.0 · Craftsman-Make-up-CBT contributors. 외부 기출 원문 복제 없음.'))
(root/'src/data/questions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Authored questions:',len(rows))
