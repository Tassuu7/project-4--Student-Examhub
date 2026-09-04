/**
 * ExamHub - Grading & Normalization Interfaces
 */

export interface GradeCurveResult {
  exam_id: string;
  method: string;
  original_mean: number;
  curved_mean: number;
  adjusted_scores_count: number;
  score_deltas: Array<{
    attempt_id: string;
    old_score: number;
    curved_score: number;
    delta: number;
  }>;
}
