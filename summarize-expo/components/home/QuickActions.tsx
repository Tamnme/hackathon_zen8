import { triggerApi } from '@/api/trigger';
import { Button } from '@/components/ui/Button';
import { useAppSelector } from '@/store';
import React, { useState } from 'react';
import { ActivityIndicator, StyleSheet, View } from 'react-native';
import { Text } from '../ui/Text';

interface QuickActionsProps {
  onSummarizeNow: () => void;
}

export function QuickActions({ onSummarizeNow }: QuickActionsProps) {
  const { slackConfig, channels } = useAppSelector((state) => state.user);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSummarize = async () => {
    if (!slackConfig.email || !slackConfig.isVerified) {
      setError('Please configure your Slack settings first');
      return;
    }

    if (!channels || channels.length === 0) {
      setError('Please configure your default channels first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Get today and yesterday in YYYY-MM-DD format
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);

      const startDate = yesterday.toISOString().split('T')[0];
      const endDate = today.toISOString().split('T')[0];

      const result = await triggerApi.createTriggerSettings({
        email: slackConfig.email,
        channels,
        start_date: startDate,
        end_date: endDate,
      });

      if (result.success) {
        onSummarizeNow();
      } else {
        setError('Failed to start summarization');
      }
    } catch (err) {
      setError('An error occurred while starting summarization');
      console.error('Error creating trigger:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.section}>
      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}
      <Button
        mode="contained"
        onPress={handleSummarize}
        style={styles.actionButton}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator size="small" color="#fff" />
        ) : (
          'Summarize Now'
        )}
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    marginBottom: 24,
  },
  actionButton: {
    marginTop: 8,
  },
  errorText: {
    color: '#FF3B30',
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 8,
  },
});