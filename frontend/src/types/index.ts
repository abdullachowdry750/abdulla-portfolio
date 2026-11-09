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
export interface CustomerSummary {
  total_customers: number;
  unique_cities: number;
  first_signup: string | null;
  latest_signup: string | null;
}

export interface CityDistribution {
  city: string;
  customer_count: number;
}

export interface MonthlySignup {
  signup_month: string;
  new_customers: number;
}

export interface CustomerAnalytics {
  summary: CustomerSummary;
  city_distribution: CityDistribution[];
  monthly_signups: MonthlySignup[];
}