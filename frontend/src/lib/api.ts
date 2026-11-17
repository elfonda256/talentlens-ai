/** Single place where the frontend talks to the backend. */

/**
 * Requests go to this app's own server-side relay (app/api/backend), which adds the API key
 * and forwards them to the backend. The browser never sees the key or the backend address.
 */
const API_V1 = "/api/backend";

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
  shortlist: number;
  review: number;
  reject: number;
};

export type ConfidenceLevel = "high" | "medium" | "low";

/** Decision aid read from the screening result; it never changes a score or a decision. */
export type Assessment = {
  hiring: {
    decision: Recommendation;
    title: string;
    summary: string;
    next_steps: string[];
  };
  confidence: { level: ConfidenceLevel; reasons: string[] };
  risks: string[];
  highly_recommended: boolean;
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
  /** Components left out of the score because the CV section behind them was not read. */
  unassessed: ScoreComponent[];
  evidence: { requirement: string; best_match: string; similarity: number }[];
  recommendation: Recommendation;
  reasons: string[];
  narrative: string;
};

export type ComponentKey =
  "must_skills" | "bonus_skills" | "experience" | "education" | "semantic";

export type ComponentScore = {
  key: ComponentKey;
  weight_percent: number;
  score_percent: number;
  points: number;
  max_points: number;
  explanation: string;
  assessed: boolean;
};

export type MatchStatus = "matched" | "implied" | "missing";

export type SkillMatch = {
  label: string;
  status: MatchStatus;
  terms: string[];
};

export type ExperienceRelevance = {
  title: string;
  company: string;
  start: string;
  end: string;
  months: number;
  description: string;
  relevance: "relevant" | "partial" | "not_relevant";
  terms: string[];
};

export type MatchBreakdown = {
  components: ComponentScore[];
  must_have_skills: SkillMatch[];
  bonus_skills: SkillMatch[];
  experience: {
    relevant_years: number;
    total_years: number;
    required_years: number;
    met: boolean;
    assessed: boolean;
  };
  experiences: ExperienceRelevance[];
  education: {
    status: "match" | "related" | "mismatch" | "not_required" | "unknown";
    found_fields: string[];
    required_fields: string[];
    level_below_requirement: boolean;
  };
  unmet_requirements: string[];
};

export type MatchHighlights = {
  must_matched: number;
  must_total: number;
  bonus_matched: number;
  bonus_total: number;
  relevant_years: number;
  required_years: number;
  components: ComponentScore[];
};

export type RankingRow = ScreeningResult & {
  file_name: string;
  extraction_method: string;
  name: string;
  highlights: MatchHighlights;
  assessment: Assessment;
  warnings: string[];
};

export type Ranking = {
  job_id: string;
  embedding_backend: string;
  results: RankingRow[];
};

export type CandidateDetail = {
  result: ScreeningResult;
  breakdown: MatchBreakdown;
  assessment: Assessment;
  summary: string;
  education: { degree: string; level: number; field: string }[];
  education_in_progress: { degree: string; level: number; field: string }[];
  skills: string[];
  total_experience_months: number;
  extraction_method: string;
  extraction_confidence: number;
  /** Per section, 0 (not found) to 1 (fully read). */
  section_confidence: Record<string, number>;
  warnings: string[];
  identity: Record<string, string>;
};

export type HRSummary = {
  headline: string;
  fit: string;
  strengths: string[];
  concerns: string[];
  risks: string[];
  interview_focus: string[];
  recommendation_reason: string;
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
  const response = await fetch(`${API_V1}${path}`, {
    cache: "no-store",
    ...init,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail =
      typeof body?.detail === "string"
        ? body.detail
        : `Galat ${response.status}`;
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
export const createJob = (file: File) =>
  upload<JobProfile>("/jobs", "file", [file]);

export const listCandidates = (jobId: string) =>
  request<CandidateListItem[]>(`/jobs/${jobId}/candidates`);
export const uploadCandidates = (jobId: string, files: File[]) =>
  upload<UploadOutcome[]>(`/jobs/${jobId}/candidates`, "files", files);

export const runScreening = (jobId: string) =>
  request<ScreeningRun>(`/jobs/${jobId}/screen`, { method: "POST" });
export const getRanking = (jobId: string, reveal: boolean) =>
  request<Ranking>(`/jobs/${jobId}/ranking${withReveal(reveal)}`);

export const getCandidateDetail = (
  jobId: string,
  candidateId: string,
  reveal: boolean,
) =>
  request<CandidateDetail>(
    `/jobs/${jobId}/candidates/${candidateId}${withReveal(reveal)}`,
  );
export const createHRSummary = (
  jobId: string,
  candidateId: string,
  refresh: boolean,
) =>
  request<HRSummary>(
    `/jobs/${jobId}/candidates/${candidateId}/summary${refresh ? "?refresh=true" : ""}`,
    { method: "POST" },
  );
