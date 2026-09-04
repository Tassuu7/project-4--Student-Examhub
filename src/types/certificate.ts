/**
 * ExamHub - Digital Certificate TypeScript Interfaces
 */

export interface CertificateRecord {
  id: string;
  certificate_code: string;
  attempt_id: string;
  exam_id: string;
  student_id: string;
  student_name: string;
  roll_number: string;
  exam_name: string;
  subject_code: string;
  subject_name: string;
  percentage: number;
  grade: string;
  issue_date: string;
  expiry_date?: string;
  verification_hash: string;
  status: 'active' | 'expired' | 'revoked';
  download_url: string;
}

export interface CertificateVerificationResponse {
  is_valid: boolean;
  certificate_code: string;
  student_name: string;
  roll_number: string;
  exam_name: string;
  subject_code: string;
  subject_name: string;
  percentage: number;
  grade: string;
  issue_date: string;
  expiry_date?: string;
  issuer: string;
  verification_hash: string;
  status: string;
  tamper_status: 'intact' | 'invalid_signature';
}

export interface StudentCertificatesListResponse {
  student_id: string;
  total_certificates: number;
  items: CertificateRecord[];
}

export interface CertificateIssueRequest {
  attempt_id?: string;
  student_id?: string;
  exam_id?: string;
  custom_title?: string;
  expiry_months?: number;
}
