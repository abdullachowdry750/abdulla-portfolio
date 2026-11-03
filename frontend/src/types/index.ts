export interface Profile {
  name: string;
  role: string;
  experience: string;
  specialization: string[];
}

export interface Project {
  id: number;
  name: string;
  category: string;
  status: string;
  description: string;
  stack: string[];
}

export interface ProjectsResponse {
  projects: Project[];
}