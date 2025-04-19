import { api } from './config';

interface VerifySlackConfigParams {
  token: string;
  email?: string;
}

interface VerifySlackConfigResponse {
  success: boolean;
  message?: string;
  data?: {
    userId: string;
    email: string;
    workspaceName: string;
  };
}

export const userApi = {
  verifySlackConfig: async (params: VerifySlackConfigParams): Promise<VerifySlackConfigResponse> => {
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('token', params.token);
      if (params.email) {
        queryParams.append('email', params.email);
      }

      const response = await api.get(`/user?${queryParams.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error verifying Slack config:', error);
      throw error;
    }
  },
};