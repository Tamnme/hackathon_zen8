import { slackApi } from './config';

interface VerifySlackConfigParams {
  token: string;
  email?: string;
}

interface Response {
  success: boolean;
}

interface Channel {
  id: string;
  name: string;
}

export const slackConfigApi = {
  verifySlackConfig: async (params: VerifySlackConfigParams): Promise<Response> => {
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('token', params.token);
      if (params.email) {
        queryParams.append('email', params.email);
      }

      const response = await slackApi.get(`/user?${queryParams.toString()}`);
      return {
        success: response.status === 200 || response.status === 201,
      };
    } catch (error) {
      console.error('Error verifying Slack config:', error);
      throw error;
    }
  },

  getChannels: async (token: string): Promise<Channel[]> => {
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('token', token);

      const response = await slackApi.get(`/channels?${queryParams.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Slack channels:', error);
      throw error;
    }
  },
};