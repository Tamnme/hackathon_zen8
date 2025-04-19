import { api } from './config';

interface Summary {
  id: number;
  email: string;
  channels: string[];
  start_time: string;
  end_time: string | null;
  notion_page_url: string;
  status: 'start' | 'completed' | 'failed';
}

interface PaginatedSummaryResponse {
  histories: Summary[];
  total: number;
  page: number;
  limit: number;
}

export const summaryApi = {
  // Get the latest summary for a user
  getLatestSummary: async (email: string): Promise<Summary> => {
    try {
      const response = await api.get(`/api/summary/latest?email=${email}`);
      return response.data;
    } catch (error) {
      console.error('Error getting latest summary:', error);
      throw error;
    }
  },

  // Get summary histories with pagination
  getSummaryHistories: async (
    email: string,
    limit: number = 10,
    page: number = 1
  ): Promise<PaginatedSummaryResponse> => {
    try {
      const response = await api.get('/api/summary-histories', {
        params: {
          email,
          limit,
          page,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error getting summary histories:', error);
      throw error;
    }
  },
};