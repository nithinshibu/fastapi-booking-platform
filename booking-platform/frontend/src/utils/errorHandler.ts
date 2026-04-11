import type { AxiosError } from "axios";

interface ApiErrorBody {
  detail: string;
}

export const handleApiError = (error: unknown): string => {
  const axiosError = error as AxiosError<ApiErrorBody>;
  return axiosError.response?.data?.detail ?? "Something went wrong";
};
