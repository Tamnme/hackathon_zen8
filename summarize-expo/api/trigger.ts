import { api } from './config';

interface TriggerSettings {
  email: string;
  channels: string[];
  start_date: string;
  end_date: string;
}

interface Response {
  success: boolean;
}

export const triggerApi = {
  // Create trigger settings
  createTriggerSettings: async (settings: TriggerSettings): Promise<Response> => {
    try {
      const response = await api.post('/api/trigger-settings', settings);
      return {
        success: response.status === 200 || response.status === 201,
      };
    } catch (error) {
      console.error('Error creating trigger settings:', error);
      throw error;
    }
  },
};