/**
 * ExamHub - Certificate & Credential Service
 */

import { api } from './apiClient';
import {
  CertificateRecord,
  CertificateVerificationResponse,
  StudentCertificatesListResponse,
  CertificateIssueRequest,
} from '../types/certificate';

export const certificateService = {
  listAllCertificates: (): Promise<StudentCertificatesListResponse> => {
    return api.get<StudentCertificatesListResponse>('/certificates');
  },

  issueCertificate: (req: string | CertificateIssueRequest, customTitle?: string): Promise<CertificateRecord> => {
    if (typeof req === 'string') {
      return api.post<CertificateRecord>('/certificates/issue', {
        attempt_id: req,
        custom_title: customTitle,
      });
    }
    return api.post<CertificateRecord>('/certificates/issue', req);
  },

  revokeCertificate: (certificateCode: string, reason: string): Promise<{ status: string }> => {
    return api.post<{ status: string }>(`/certificates/revoke/${encodeURIComponent(certificateCode)}`, {
      reason,
      revoked_by: 'Instructor Review',
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
