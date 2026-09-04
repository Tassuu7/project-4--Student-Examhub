/**
 * ExamHub - Certificate & Credential Service
 */

import { api } from './apiClient';
import {
  CertificateRecord,
  CertificateVerificationResponse,
  StudentCertificatesListResponse,
} from '../types/certificate';

export const certificateService = {
  issueCertificate: (attemptId: string, customTitle?: string): Promise<CertificateRecord> => {
    return api.post<CertificateRecord>('/certificates/issue', {
      attempt_id: attemptId,
      custom_title: customTitle,
    });
  },

  verifyCertificate: (code: string): Promise<CertificateVerificationResponse> => {
    return api.get<CertificateVerificationResponse>(`/certificates/verify/${encodeURIComponent(code)}`);
  },

  getStudentCertificates: (studentId: string): Promise<StudentCertificatesListResponse> => {
    return api.get<StudentCertificatesListResponse>(`/certificates/student/${studentId}`);
  },

  getRenderUrl: (code: string): string => {
    return `/api/v1/certificates/render/${encodeURIComponent(code)}`;
  },
};
