import { Button } from '@/components/ui/Button';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface QuickActionsProps {
  onSummarizeYesterday: () => void;
  onSummarizePastWeek: () => void;
}

export function QuickActions({ onSummarizeYesterday, onSummarizePastWeek }: QuickActionsProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">Quick Actions</Text>
      <Button
        mode="contained"
        onPress={onSummarizeYesterday}
        style={styles.actionButton}
      >
        Summarize Yesterday
      </Button>
      <Button
        mode="outlined"
        onPress={onSummarizePastWeek}
        style={styles.actionButton}
      >
        Summarize Past Week
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
}); 