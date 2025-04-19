export interface SummaryRun {
  id: string;
  date: string;
  status: 'success' | 'error';
  channels: string[];
  notionUrl: string;
} 