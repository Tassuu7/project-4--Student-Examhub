/**
 * ExamHub - Universal HTTP API Client
 * Manages bearer tokens, error normalization, and request lifecycle
 */

const API_BASE = '/api/v1';

export class ApiError extends Error {
  code: string;
  statusCode: number;
  details?: unknown;

  constructor(message: string, code: string = 'API_ERROR', statusCode: number = 500, details?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
  }
}

export async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('examhub_token');
  const headers = new Headers(options.headers || {});

  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 204) {
      return {} as T;
    }

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const errorMsg = data.error || data.detail?.error || data.detail || response.statusText || 'An unexpected error occurred';
      const errorCode = data.code || data.detail?.code || `HTTP_${response.status}`;
      throw new ApiError(
        typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg),
        errorCode,
        response.status,
        data.details || data.detail?.details
      );
    }

    return data as T;
  } catch (err) {
    if (err instanceof ApiError) {
      throw err;
    }
    throw new ApiError(
      err instanceof Error ? err.message : 'Network communication failure',
      'NETWORK_ERROR',
      0
    );
  }
}

export const api = {
  get: <T>(url: string, headers?: HeadersInit) => request<T>(url, { method: 'GET', headers }),
  post: <T>(url: string, body?: unknown, headers?: HeadersInit) =>
    request<T>(url, { method: 'POST', body: JSON.stringify(body), headers }),
  put: <T>(url: string, body?: unknown, headers?: HeadersInit) =>
    request<T>(url, { method: 'PUT', body: JSON.stringify(body), headers }),
  patch: <T>(url: string, body?: unknown, headers?: HeadersInit) =>
    request<T>(url, { method: 'PATCH', body: body ? JSON.stringify(body) : undefined, headers }),
  delete: <T>(url: string, headers?: HeadersInit) => request<T>(url, { method: 'DELETE', headers }),
};
