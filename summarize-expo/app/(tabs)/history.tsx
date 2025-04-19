import { HistoryList } from '@/components/history/HistoryList';
import { SummaryRun } from '@/components/history/types';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

// Mock data - replace with real data in production
const HISTORY_DATA: SummaryRun[] = [
  {
    id: 'run_7SEBx_W',
    date: '2024-03-20',
    status: 'success',
    channels: ['#general', '#random'],
    notionUrl: '/',
  },
  {
    id: 'run_6FGHx_Y',
    date: '2024-03-19',
    status: 'success',
    channels: ['#general'],
    notionUrl: '/',
  },
  {
    id: 'run_5JKLx_Z',
    date: '2024-03-18',
    status: 'error',
    channels: ['#general', '#dev-team'],
    notionUrl: '/',
  },
];

export default function HistoryScreen() {
  const handleViewNotionPage = (notionUrl: string) => {
    // Handle opening Notion page in browser
    // You can use Linking.openURL(notionUrl) here
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text variant="h1">History</Text>
        <Text variant="subtitle">Past summary runs</Text>
      </View>

      <HistoryList
        data={HISTORY_DATA}
        onViewNotionPage={handleViewNotionPage}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  header: {
    marginBottom: 24,
  },
});