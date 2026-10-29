import type {
  Captcha,
  Notification,
  OtpInfo,
  Profile,
  Result,
  ResultSummary,
} from "./types";

const API_BASE =
  (import.meta.env.VITE_API_BASE_URL ?? window.location.origin)
    .replace(/\/+$/, "") + "/api";

const TOKEN_KEY = "session_token";

export class BackendError extends Error {
  code: string;

  constructor(code: string, message: string) {
    super(message);
    this.name = "BackendError";
    this.code = code;
  }
}

type Envelope<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: string; message: string } };

const isDesktop = (): boolean =>
  typeof window !== "undefined" && "pywebview" in window;

const bridgeReady = new Promise<void>((resolve) => {
  if (typeof window === "undefined") return resolve();
  const w = window as any;
  if (w.pywebview?.api) return resolve();
  window.addEventListener("pywebviewready", () => resolve(), { once: true });
});

async function viaBridge<T>(method: string, args: object): Promise<T> {
  await bridgeReady;
  const env: Envelope<T> = await (window as any).pywebview.api[method](args);
  if (!env.ok) throw new BackendError(env.error.code, env.error.message);
  return env.data;
}

async function viaHttp<T>(method: string, args: object): Promise<T> {
  const token = localStorage.getItem(TOKEN_KEY) || "";
  const res = await fetch(`${API_BASE}/${method}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(args),
  });
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    throw new BackendError(
      body?.error?.code ?? "http_error",
      body?.error?.message ?? `Error ${res.status}`
    );
  }
  return body as T;
}

const call = async <T>(
  method: string,
  args: object = {},
): Promise<T> => {
  if (isDesktop()) {
    return viaBridge<T>(method, args);
  }

  await bridgeReady;

  if (isDesktop()) {
    return viaBridge<T>(method, args);
  }

  return viaHttp<T>(method, args);
};

const token = (): string => localStorage.getItem(TOKEN_KEY) || "";

export const api = {
  // ---- auth ----
  getCaptcha: () => call<Captcha>("get_captcha"),

  login: (
    mobile: string,
    password: string,
    captcha_code: number,
    captcha_token: string,
  ) =>
    call<{ session_token: string }>("login", {
      mobile,
      password,
      captcha_code,
      captcha_token,
    }),

  logout: () => call<null>("logout", { token: token() }),

  status: () => call<boolean>("status", { token: token() }),

  sendOtp: (mobile: string) =>
    call<OtpInfo>("request_otp", { mobile_no: mobile }),

  resetPassword: (
    mobile: string,
    otp: string,
    new_password: string,
    session_token: string,
  ) =>
    call<null>("reset_password", {
      mobile_no: mobile,
      otp_code: otp,
      new_password,
      session_token,
    }),

  // ---- data ----
  getProfile: () => call<Profile>("get_profile", { token: token() }),

  getResults: () => call<ResultSummary[]>("get_results", { token: token() }),

  getResult: (exam_no: string, reg_no: string) =>
    call<Result>("get_result", { token: token(), exam_no, reg_no }),

  getNotifications: (limit = 20) =>
    call<Notification[]>("get_notifications", { token: token(), limit }),

  // ---- system ----
  healthCheck: () => call<Record<string, boolean>>("health"),
};