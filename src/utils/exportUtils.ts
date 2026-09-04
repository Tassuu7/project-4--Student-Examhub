/**
 * ExamHub - File Export & Download Utilities
 */

export function downloadBlob(content: string, filename: string, mimeType: string = 'text/csv;charset=utf-8;') {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function exportJsonFile(data: unknown, filename: string) {
  const jsonStr = JSON.stringify(data, null, 2);
  downloadBlob(jsonStr, filename, 'application/json;charset=utf-8;');
}
