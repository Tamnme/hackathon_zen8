import { ChannelSelector } from '@/components/trigger/ChannelSelector';
import { DateRangeSelector } from '@/components/trigger/DateRangeSelector';
import { NotionTargetSelector } from '@/components/trigger/NotionTargetSelector';
import { Button } from '@/components/ui/Button';
import { Text } from '@/components/ui/Text';
import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

export default function TriggerScreen() {
  const [startDate, setStartDate] = useState<Date>();
  const [endDate, setEndDate] = useState<Date>();
  const [selectedChannels, setSelectedChannels] = useState<string[]>([]);

  const handleSelectChannels = () => {
    // Implement channel selection logic
  };

  const handleStartSummary = () => {
    // Implement summary creation logic
  };

  return (
    <View style={styles.container}>
      <Text variant="h1">Manual Summary</Text>
      <Text variant="subtitle" style={styles.description}>
        Create a new summary from Slack messages
      </Text>

      <DateRangeSelector
        startDate={startDate}
        endDate={endDate}
        onStartDateChange={setStartDate}
        onEndDateChange={setEndDate}
      />

      <ChannelSelector
        selectedChannels={selectedChannels}
        onSelectChannels={handleSelectChannels}
      />

      <NotionTargetSelector targetPage="Team Announcements" />

      <Button
        mode="contained"
        onPress={handleStartSummary}
        style={styles.submitButton}
      >
        Start Summary
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  description: {
    marginTop: 4,
    marginBottom: 24,
  },
  submitButton: {
    marginTop: 'auto',
  },
}); 