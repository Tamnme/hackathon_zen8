import axios from 'axios';

const BASE_URL = process.env.EXPO_PUBLIC_SLACK_API_URL || 'https://cqwwedkg6a.execute-api.ap-southeast-1.amazonaws.com';

export const slackApi = axios.create({
  baseURL: BASE_URL,
  headers: {
      'Content-Type': 'application/json',
    },
  });

export const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL || 'http://52.221.247.36:8080',
  headers: {
    'Content-Type': 'application/json',
  },
});