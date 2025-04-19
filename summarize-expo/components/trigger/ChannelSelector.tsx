import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface ChannelSelectorProps {
  selectedChannels: string[];
  onSelectChannels: () => void;
}

export function ChannelSelector({ selectedChannels, onSelectChannels }: ChannelSelectorProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">Channels</Text>
      <Card>
        <Text variant="label">Selected Channels</Text>
        <Text style={styles.placeholder}>
          {selectedChannels.length > 0 ? selectedChannels.join(', ') : 'No channels selected'}
        </Text>
        <Button
          mode="outlined"
          onPress={onSelectChannels}
          icon={({ color }) => <IconSymbol name="plus" size={20} color={color} />}
        >
          Select Channels
        </Button>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    marginBottom: 24,
  },
  placeholder: {
    color: '#666',
    marginVertical: 8,
  },
}); 