import { summaryApi } from '@/api/summary';
import { StatusIndicator } from '@/components/StatusIndicator';
import { Card } from '@/components/ui/Card';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Text } from '@/components/ui/Text';
import { useAppSelector } from '@/store';
import React, { useEffect, useState } from 'react';
import { Linking, StyleSheet, View } from 'react-native';

interface LastRunProps {
  onViewNotionPage?: () => void;
}

export function LastRun({ onViewNotionPage }: LastRunProps) {
  const { slackConfig } = useAppSelector((state) => state.user);
  const [summary, setSummary] = useState<{
    id: number;
    email: string;
    channels: string[];
    start_time: string;
    end_time: string | null;
    notion_page_url: string;
    status: 'start' | 'completed' | 'failed';
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLatestSummary = async () => {
      if (!slackConfig.email) {
        setError('Slack email not configured');
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const latestSummary = await summaryApi.getLatestSummary(slackConfig.email);
        setSummary(latestSummary);
      } catch (err) {
        setError('Failed to fetch latest summary');
        console.error('Error fetching latest summary:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchLatestSummary();
  }, [slackConfig.email]);

  const handleViewNotionPage = () => {
    if (summary?.notion_page_url) {
      Linking.openURL(summary.notion_page_url);
    }
    onViewNotionPage?.();
  };

  if (loading) {
    return (
      <Card style={styles.lastRunCard}>
        <View style={styles.emptyContainer}>
          <IconSymbol name="arrow.clockwise" size={48} color="#E5E5E5" />
          <Text variant="h2" style={styles.emptyTitle}>Loading...</Text>
        </View>
      </Card>
    );
  }

  if (!summary || error) {
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
        <StatusIndicator 
          status={summary.status === 'completed' ? 'success' : summary.status === 'failed' ? 'error' : 'unverified'} 
          label={summary.status.charAt(0).toUpperCase() + summary.status.slice(1)} 
        />
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Run ID</Text>
        <Text>{summary.id}</Text>
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Time</Text>
        <Text>{new Date(summary.start_time).toLocaleString()}</Text>
      </View>

      <View style={styles.infoRow}>
        <Text variant="label">Channels</Text>
        <Text>{summary.channels.join(', ')}</Text>
      </View>

      {summary.notion_page_url && (
        <View style={styles.infoRow}>
          <Text variant="label">Notion Page</Text>
          <Text
            style={styles.link}
            onPress={handleViewNotionPage}
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