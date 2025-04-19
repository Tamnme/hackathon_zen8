import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface AboutSectionProps {
  version: string;
  onSignOut: () => void;
}

export function AboutSection({ version, onSignOut }: AboutSectionProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">About</Text>
      <Card>
        <View style={styles.settingRow}>
          <Text>Version</Text>
          <Text>{version}</Text>
        </View>
        <Button
          mode="text"
          onPress={onSignOut}
          style={styles.signOutButton}
          textColor="#FF3B30"
        >
          Sign Out
        </Button>
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
  signOutButton: {
    marginTop: 8,
  },
}); 