import { api } from './config';

interface AppSettings {
  email: string;
  schedule_period: 'daily' | 'weekly';
  default_channels: string[];
  get_notion_page: string;
  slack_token: string;
  notion_secret: string;
  notion_page_id: string;
}

interface Response {
  success: boolean;
}

export const settingsApi = {
  // Get app settings for a user
  getAppSettings: async (email: string): Promise<AppSettings> => {
    try {
      const response = await api.get(`/api/app-settings?email=${email}`);
      return response.data;
    } catch (error) {
      console.error('Error getting app settings:', error);
      throw error;
    }
  },

  // Update app settings
  updateAppSettings: async (settings: Partial<AppSettings>): Promise<Response> => {
    try {
      const response = await api.post('/api/app-settings', settings);
      return {
        success: response.status === 200 || response.status === 201,
      };
    } catch (error) {
      console.error('Error updating app settings:', error);
      throw error;
    }
  },

  // Update Slack settings
  updateSlackSettings: async (email: string, slackToken: string): Promise<Response> => {
    try {
      const response = await api.put('/app-settings/slack', {
        email,
        slack_token: slackToken,
      });
      return {
        success: response.status === 200 || response.status === 201,
      };
    } catch (error) {
      console.error('Error updating Slack settings:', error);
      throw error;
    }
  },

  // Update Notion settings
  updateNotionSettings: async (email: string, notionSecret: string, notionPageId: string): Promise<Response> => {
    try {
      const response = await api.put('/app-settings/notion', {
        email,
        notion_secret: notionSecret,
        notion_page_id: notionPageId,
      });
      return {
        success: response.status === 200 || response.status === 201,
      };
    } catch (error) {
      console.error('Error updating Notion settings:', error);
      throw error;
    }
  },

  // Validate Notion connection
  validateNotionConnection: async (notionSecret: string, notionPageId: string): Promise<Response> => {
    try {
      const response = await api.post('/notion/validate-connection', {
        notion_secret: notionSecret,
        notion_page_id: notionPageId,
      });
      return {
        success: response.status === 200 || response.status === 201,
      };
    } catch (error) {
      console.error('Error validating Notion connection:', error);
      throw error;
    }
  },
};