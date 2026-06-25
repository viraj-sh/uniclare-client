const BASE_URL =
  (import.meta.env.VITE_API_BASE_URL ?? window.location.origin)
    .replace(/\/+$/, "") + "/api";

function getToken(): string {
  return localStorage.getItem("session_token") || "";
}

function authHeaders(): HeadersInit {
  return { Authorization: `Bearer ${getToken()}` };
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    let msg = `Error ${res.status}`;
    try {
      const body = await res.json();
      msg = body?.detail?.[0]?.msg || body?.detail || body?.msg || msg;
    } catch {}
    throw new Error(msg);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  login(mobile_no: string, password: string) {
    const params = new URLSearchParams({ mobile_no, password });
    return request<{ session_id: string; msg: string }>(`/auth/login?${params}`, { method: "POST" });
  },

  logout() {
    return request<void>(`/auth/logout`, { method: "POST", headers: authHeaders() });
  },

  sendOtp(mobile_no: string) {
    const params = new URLSearchParams({ mobile_no });
    return request<unknown>(`/auth/send-otp?${params}`, { method: "POST" });
  },

  resetPassword(mobile_no: string, otp: string, new_password: string) {
    const params = new URLSearchParams({ mobile_no, otp, new_password });
    return request<unknown>(`/auth/reset-password?${params}`, { method: "POST" });
  },

  getProfile() {
    return request<{
      full_name: string;
      fat_name: string;
      mot_name: string;
      degree: string;
      degree_code: string;
      college: string;
      college_code: string;
      photo: string;
      category: string;
      fee_type: string;
      reg_no: string;
      mob_no: string;
      email: string;
      parent_mob_no: string;
    }>(`/user`, { headers: authHeaders() });
  },

  changePassword(current_password: string, new_password: string) {
    const params = new URLSearchParams({ current_password, new_password });
    return request<{ status: string; msg: string }>(`/user/change-password?${params}`, {
      method: "PATCH",
      headers: authHeaders(),
    });
  },

  getResults() {
    return request<Array<{
      year: string;
      exam_date: string;
      exam_name: string;
      result_date: string;
      rv_result_date: string;
      reg_no: string;
      mc_no: string;
      status: string;
    }>>(`/result`, { headers: authHeaders() });
  },

  getResult(exam_no: string, reg_no: string) {
    const params = new URLSearchParams({ reg_no });
    return request<{
      student_details: {
        sem: string;
        full_sem: string;
        exam_date: string;
        exam_no: string;
      };
      result: {
        result: string;
        cgpa: string;
        sgpa: string;
        percentage: string;
      } | null;
      subjects: Array<{
        id: number;
        sub: string;
        exam_type: string;
        ese_marks: string;
        viva_marks: string;
        ia_marks: string;
        total_marks: string;
        credits: string;
        grade_points: string;
        credit_points: string;
        remarks: string;
        grade: string;
      }>;
    }>(`/result/${exam_no}?${params}`, { headers: authHeaders() });
  },

  healthCheck() {
    return request<{ status: string }>(`/health`);
  },

  getNotifications() {
    return request<Array<{
      title: string;
      body: string;
      date: string;
    }>>(`/notifications`, { headers: authHeaders() });
  },
};