import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface ConfigurationSettingsProps {
  schedule: string;
  defaultChannels: string[];
  notionTarget: string;
  activityCheck: string;
}

export function ConfigurationSettings({
  schedule,
  defaultChannels,
  notionTarget,
  activityCheck,
}: ConfigurationSettingsProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">Configuration</Text>
      <Card>
        <View style={styles.settingRow}>
          <Text variant="label">Schedule</Text>
          <Text>{schedule}</Text>
        </View>
        <View style={styles.settingRow}>
          <Text variant="label">Default Channels</Text>
          <Text>{defaultChannels.join(', ')}</Text>
        </View>
        <View style={styles.settingRow}>
          <Text variant="label">Notion Target</Text>
          <Text>{notionTarget}</Text>
        </View>
        <View style={styles.settingRow}>
          <Text variant="label">Activity Check</Text>
          <Text>{activityCheck}</Text>
        </View>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    marginBottom: 24,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#E5E5E5',
  },
}); 