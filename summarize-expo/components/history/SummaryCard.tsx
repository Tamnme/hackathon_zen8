import { StatusIndicator } from '@/components/StatusIndicator';
import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface SummaryCardProps {
  id: string;
  date: string;
  status: 'success' | 'error';
  channels: string[];
  onViewNotionPage: () => void;
}

export function SummaryCard({ id, date, status, channels, onViewNotionPage }: SummaryCardProps) {
  return (
    <Card style={styles.historyCard}>
      <View style={styles.historyHeader}>
        <Text variant="h2">Summary Run</Text>
        <StatusIndicator
          status={status}
          label={status.charAt(0).toUpperCase() + status.slice(1)} 
        />
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Run ID</Text>
        <Text>{id}</Text>
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Date</Text>
        <Text>{new Date(date).toLocaleDateString()}</Text>
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Channels</Text>
        <Text>{channels.join(', ')}</Text>
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Notion Page</Text>
        <Text
          style={styles.link}
          onPress={onViewNotionPage}
        >
          View
        </Text>
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  historyCard: {
    marginBottom: 8,
  },
  historyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  link: {
    color: '#0066FF',
  },
}); 