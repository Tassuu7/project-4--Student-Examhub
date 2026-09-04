/**
 * ExamHub - Live Proctoring Service
 */

import { api } from './apiClient';
import {
  CandidateIntegrityProfile,
  ProctoringLiveFeedResponse,
} from '../types/proctoring';

export const proctoringService = {
  ingestEvent: (attemptId: string, eventType: string, details?: string, severity: string = 'low'): Promise<{ status: string; event_id: string }> => {
    return api.post<{ status: string; event_id: string }>('/proctoring/events', {
      attempt_id: attemptId,
      event_type: eventType,
      details,
      severity,
    });
  },

  getCandidateIntegrity: (attemptId: string): Promise<CandidateIntegrityProfile> => {
    return api.get<CandidateIntegrityProfile>(`/proctoring/candidate/${attemptId}`);
  },

  getLiveFeed: (): Promise<ProctoringLiveFeedResponse> => {
    return api.get<ProctoringLiveFeedResponse>('/proctoring/feed');
  },
};
