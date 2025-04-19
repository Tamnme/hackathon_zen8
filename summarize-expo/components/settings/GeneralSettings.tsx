import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, Switch, View } from 'react-native';

interface GeneralSettingsProps {
  pushNotifications: boolean;
  onPushNotificationsChange: (value: boolean) => void;
  appearance: string;
}

export function GeneralSettings({
  pushNotifications,
  onPushNotificationsChange,
  appearance,
}: GeneralSettingsProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">General</Text>
      <Card style={{ marginTop: 16 }}>
        <View style={styles.settingRow}>
          <Text>Push Notifications</Text>
          <Switch
            value={pushNotifications}
            onValueChange={onPushNotificationsChange}
          />
        </View>
        <View style={styles.settingRow}>
          <Text>Appearance</Text>
          <Text style={styles.settingValue}>{appearance}</Text>
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
  settingValue: {
    color: '#666',
  },
}); 