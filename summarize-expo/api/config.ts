import axios, { AxiosError, AxiosResponse } from 'axios';

const BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'https://cqwwedkg6a.execute-api.ap-southeast-1.amazonaws.com';

export const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    // Handle error responses here
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
); 