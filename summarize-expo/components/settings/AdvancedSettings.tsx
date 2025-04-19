import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface AdvancedSettingsProps {
  onOpenWebApp: () => void;
}

export function AdvancedSettings({ onOpenWebApp }: AdvancedSettingsProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">Advanced</Text>
      <Card>
        <Button
          mode="text"
          onPress={onOpenWebApp}
        >
          Open Web App for Full Configuration
        </Button>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    marginBottom: 24,
  },
}); 