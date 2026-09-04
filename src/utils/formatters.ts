/**
 * ExamHub - Common Formatters
 */

export function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}m ${s}s`;
}

export function formatPercentage(val: number): string {
  return `${val.toFixed(1)}%`;
}

export function formatScore(obtained: number, total: number): string {
  return `${obtained.toFixed(1)} / ${total.toFixed(1)}`;
}

export function formatDate(isoStr: string): string {
  if (!isoStr) return 'N/A';
  try {
    return new Date(isoStr).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return isoStr;
  }
}

export function formatDateTime(isoStr: string): string {
  if (!isoStr) return 'N/A';
  try {
    return new Date(isoStr).toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  } catch {
    return isoStr;
  }
}
