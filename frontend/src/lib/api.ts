/** Single place where the frontend talks to the backend. */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const API_V1 = `${API_BASE_URL}/api/v1`;

export const API_DOCS_URL = `${API_BASE_URL}/docs`;

export type Recommendation = "SHORTLIST" | "REVIEW" | "REJECT";

export type HealthResponse = {
  status: "ok";
  app_name: string;
  version: string;
  environment: string;
  timestamp: string;
  embedding_backend: string;
  llm_summary: boolean;
};

export type JobSummary = {
  job_id: string;
  title: string;
  candidate_count: number;
  screened: boolean;
};

export type SkillRequirement = {
  skill_id: string;
  label: string;
  priority: "must" | "nice";
  group: string;
};

export type JobProfile = {
  job_id: string;
  title: string;
  min_years_experience: number;
  degree_fields: string[];
  skills: SkillRequirement[];
  requirement_sentences: string[];
  responsibility_sentences: string[];
  weights: Record<string, number>;
};

export type UploadOutcome = {
  file_name: string;
  status: "parsed" | "duplicate" | "failed";
  candidate_id: string;
  detail: string;
};

export type CandidateListItem = {
  candidate_id: string;
  file_name: string;
  extraction_method: string;
  extraction_confidence: number;
  total_experience_months: number;
  skill_count: number;
  name: string;
};

export type ScreeningRun = {
  job_id: string;
  screened: number;
  embedding_backend: string;
  shortlist: number;
  review: number;
  reject: number;
};

export type ScoreComponent = "skills" | "experience" | "semantic" | "education";

export type ScreeningResult = {
  candidate_id: string;
  rank: number;
  score: number;
  breakdown: Record<ScoreComponent, number>;
  contributions: Record<ScoreComponent, number>;
  matched_skills: string[];
  missing_must_skills: string[];
  missing_nice_skills: string[];
  knockout_flags: string[];
  evidence: { requirement: string; best_match: string; similarity: number }[];
  recommendation: Recommendation;
  reasons: string[];
  narrative: string;
};

export type RankingRow = ScreeningResult & {
  file_name: string;
  extraction_method: string;
  name: string;
};

export type Ranking = {
  job_id: string;
  embedding_backend: string;
  results: RankingRow[];
};

export type CandidateDetail = {
  result: ScreeningResult;
  summary: string;
  experiences: { title: string; company: string; start: string; end: string; months: number }[];
  education: { degree: string; level: number; field: string }[];
  skills: string[];
  total_experience_months: number;
  extraction_method: string;
  extraction_confidence: number;
  warnings: string[];
  identity: Record<string, string>;
};

export type HRSummary = {
  text: string;
  source: "gemini" | "template";
  model: string;
  note: string;
};

/** An error answer from the API. `status` lets callers tell "not screened yet" from a failure. */
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_V1}${path}`, { cache: "no-store", ...init });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = typeof body?.detail === "string" ? body.detail : `Galat ${response.status}`;
    throw new ApiError(response.status, detail);
  }
  return (await response.json()) as T;
}

function upload<T>(path: string, field: string, files: File[]): Promise<T> {
  const form = new FormData();
  files.forEach((file) => form.append(field, file));
  return request<T>(path, { method: "POST", body: form });
}

const withReveal = (reveal: boolean) => (reveal ? "?reveal=true" : "");

export const getHealth = () => request<HealthResponse>("/health");
export const listJobs = () => request<JobSummary[]>("/jobs");
export const getJob = (jobId: string) => request<JobProfile>(`/jobs/${jobId}`);
export const createJob = (file: File) => upload<JobProfile>("/jobs", "file", [file]);

export const listCandidates = (jobId: string) =>
  request<CandidateListItem[]>(`/jobs/${jobId}/candidates`);
export const uploadCandidates = (jobId: string, files: File[]) =>
  upload<UploadOutcome[]>(`/jobs/${jobId}/candidates`, "files", files);

export const runScreening = (jobId: string) =>
  request<ScreeningRun>(`/jobs/${jobId}/screen`, { method: "POST" });
export const getRanking = (jobId: string, reveal: boolean) =>
  request<Ranking>(`/jobs/${jobId}/ranking${withReveal(reveal)}`);

export const getCandidateDetail = (jobId: string, candidateId: string, reveal: boolean) =>
  request<CandidateDetail>(`/jobs/${jobId}/candidates/${candidateId}${withReveal(reveal)}`);
export const createHRSummary = (jobId: string, candidateId: string, refresh: boolean) =>
  request<HRSummary>(
    `/jobs/${jobId}/candidates/${candidateId}/summary${refresh ? "?refresh=true" : ""}`,
    { method: "POST" },
  );
