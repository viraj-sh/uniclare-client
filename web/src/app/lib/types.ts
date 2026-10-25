export interface Captcha {
  value: number;
  session_token: string;
}

export interface OtpInfo {
  email: string;
  message: string | null;
}

export interface Profile {
  full_name: string;
  fat_name: string | null;
  mot_name: string | null;
  degree: string;
  degree_code: string | null;
  college: string | null;
  college_code: string | null;
  photo: string | null;
  category: string | null;
  fee_type: string | null;
  reg_no: string;
  mob_no: string | null;
  email: string | null;
  parent_mob_no: string | null;
}

export interface ResultSummary {
  year: string;
  exam_name: string;
  exam_date: string | null;
  result_date: string | null;
  rv_result_date: string | null;
  reg_no: string;
  mc_no: string | null;
  status: string | null;
}

export interface StudentDetail {
  sem: string | null;
  full_sem: string | null;
  exam_date: string | null;
  exam_no: string;
}

export interface ResultInfo {
  result: string | null;
  cgpa: string | null;
  sgpa: string | null;
  percentage: string | null;
}

export interface SubjectResult {
  id: number | null;
  sub: string | null;
  exam_type: string | null;
  ese_marks: string | null;
  viva_marks: string | null;
  ia_marks: string | null;
  total_marks: string | null;
  credits: string | null;
  grade_points: string | null;
  credit_points: string | null;
  remarks: string | null;
  grade: string | null;
}

export interface Result {
  student_details: StudentDetail;
  result: ResultInfo;
  subjects: SubjectResult[];
}

export interface Notification {
  title: string;
  body: string | null;
  date: string | null;
}