export interface MovieResponse {
  id: number;
  title: string;
  description: string | null;
  duration_minutes: number;
  language: string;
  release_date: string; // ISO date string: "2024-06-15"
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface MovieCreate {
  title: string;
  description?: string; // optional - backend defaults to null
  duration_minutes: number;
  language: string;
  release_date: string; // ISO date string: "2024-06-15"
}

export interface MovieUpdate {
  title?: string;
  description?: string | null;
  duration_minutes?: number;
  language?: string;
  release_date?: string;
  is_active?: boolean;
}

export interface ShowResponse {
  id: number;
  movie_id: number;
  show_time: string; // ISO datetime string: "2024-06-15T19:30:00"
  total_seats: number;
  available_seats: number;
  hall_name: string;
  created_at: string;
  updated_at: string;
}
