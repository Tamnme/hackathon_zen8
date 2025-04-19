import { StatusIndicator } from '@/components/StatusIndicator';
import { Card } from '@/components/ui/Card';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface LastRunProps {
  id?: string;
  time?: string;
  channels?: string[];
  onViewNotionPage?: () => void;
}

export function LastRun({ id, time, channels, onViewNotionPage }: LastRunProps) {
  const isEmpty = true

  if (isEmpty) {
    return (
      <Card style={styles.lastRunCard}>
        <View style={styles.emptyContainer}>
          <IconSymbol name="doc.text" size={48} color="#E5E5E5" />
          <Text variant="h2" style={styles.emptyTitle}>No Runs Yet</Text>
          <Text style={styles.emptyDescription}>
            Your first summary will appear here after it's created
          </Text>
        </View>
      </Card>
    );
  }

  return (
    <Card style={styles.lastRunCard}>
      <View style={styles.lastRunHeader}>
        <Text variant="h2">Last Run</Text>
        <StatusIndicator status="success" label="Success" />
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Run ID</Text>
        <Text>{id}</Text>
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Time</Text>
        <Text>{time}</Text>
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Channels</Text>
        <Text>{channels?.join(', ')}</Text>
      </View>

      {onViewNotionPage && (
        <View style={styles.infoRow}>
          <Text variant="label">Notion Page</Text>
          <Text
            style={styles.link}
            onPress={onViewNotionPage}
          >
            View
          </Text>
        </View>
      )}
    </Card>
  );
}

const styles = StyleSheet.create({
  lastRunCard: {
    marginBottom: 24,
  },
  lastRunHeader: {
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
  emptyContainer: {
    padding: 32,
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyTitle: {
    marginTop: 16,
    marginBottom: 8,
    textAlign: 'center',
  },
  emptyDescription: {
    color: '#666',
    textAlign: 'center',
  },
});