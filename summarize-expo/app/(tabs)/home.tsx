import { LastRun } from '@/components/home/LastRun';
import { QuickActions } from '@/components/home/QuickActions';
import { SystemStatus } from '@/components/home/SystemStatus';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text variant="h1">Dashboard</Text>
      </View>

      <LastRun
        id="run_7SEBx_W"
        time="Invalid Date"
        channels={['#general', '#random']}
        onViewNotionPage={() => {
          // Handle opening Notion page in browser
          // You can use Linking.openURL(notionUrl) here
        }}
      />

      <QuickActions
        onSummarizeYesterday={() => {
          // Handle summarize yesterday
        }}
        onSummarizePastWeek={() => {
          // Handle summarize past week
        }}
      />

      <SystemStatus
        slackStatus="success"
        notionStatus="success"
        aiStatus="success"
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
});
