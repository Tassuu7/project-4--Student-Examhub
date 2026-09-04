/**
 * ExamHub - Math & Statistics Utilities
 */

export function calculateAverage(arr: number[]): number {
  if (arr.length === 0) return 0;
  return arr.reduce((acc, v) => acc + v, 0) / arr.length;
}

export function calculateStandardDeviation(arr: number[]): number {
  if (arr.length < 2) return 0;
  const avg = calculateAverage(arr);
  const variance = arr.reduce((acc, v) => acc + Math.pow(v - avg, 2), 0) / (arr.length - 1);
  return Math.sqrt(variance);
}

export function clamp(val: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, val));
}
