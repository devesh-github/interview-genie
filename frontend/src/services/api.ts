
const API_URL = "http://localhost:8000/api";

export interface Profile {
  id: number;
  name: string;
  role: string;
  experience_years: number;
  target_company: string;
  created_at: string;
}

export type ProfileInput = Pick<
  Profile,
  "name" | "role" | "experience_years" | "target_company"
>;

export interface Skill {
  id: number;
  profile_id: number;
  name: string;
  level: "Beginner" | "Intermediate" | "Advanced";
  priority: "Low" | "Medium" | "High";
}

export type SkillInput = Pick<
  Skill,
  "name" | "level" | "priority"
>;

async function request<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      error.detail || `Request failed: ${response.status}`
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export const api = {
  getProfile: () => request<Profile>("/profile"),

  saveProfile: (data: ProfileInput) =>
    request<Profile>("/profile", {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  getSkills: () => request<Skill[]>("/skills"),

  addSkill: (data: SkillInput) =>
    request<Skill>("/skills", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  deleteSkill: (id: number) =>
    request<void>(`/skills/${id}`, {
      method: "DELETE",
    }),
};
