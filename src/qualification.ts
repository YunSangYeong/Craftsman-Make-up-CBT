/** Learning assumptions, NOT verified official rules: Q-Net access was denied. */
export const PROFILE = {
  name: "미용사(메이크업)", slug: "makeup-cbt",
  rulesVerificationStatus: "pending",
  officialSources: ["https://www.q-net.or.kr/crf005.do?id=crf00503&jmCd=7967"],
  subjects: ["메이크업 개론", "공중위생관리학", "화장품학"] as const,
  exam: { questionCount: 60, durationMinutes: 60, choiceCount: 4, passScore: 60,
    hasSubjectCutoff: false, selectionPolicy: "전 영역 전체 풀 무작위; 과목별 고정 배분 없음. 공식 분포 미확인.",
    scoring: "정답 수 / 전체 수 × 100; 미응답 오답; 합격은 반올림 전 비율로 판정" },
  targetReviewedCount: 1000,
} as const;
