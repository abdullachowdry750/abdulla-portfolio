import type { Profile, ProjectsResponse } from "@/types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getProfile(): Promise<Profile> {
  const response = await fetch(`${API_URL}/api/profile`, {
    next: { revalidate: 3600 },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch profile");
  }

  return response.json();
}

export async function getProjects(): Promise<ProjectsResponse> {
  const response = await fetch(`${API_URL}/api/projects`, {
    next: { revalidate: 3600 },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch projects");
  }

  return response.json();
}