import DateTimePicker from '@/components/DateTimePicker';
import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface DateRangeSelectorProps {
  startDate?: Date;
  endDate?: Date;
  onStartDateChange: (date: Date | undefined) => void;
  onEndDateChange: (date: Date | undefined) => void;
}

export function DateRangeSelector({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
}: DateRangeSelectorProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">Date Range</Text>
      <Card>
        <View style={styles.dateField}>
          <Text variant="label">Start Date</Text>
          <DateTimePicker
            mode="date"
            value={startDate}
            onChange={onStartDateChange}
          />
        </View>
        <View style={styles.dateField}>
          <Text variant="label">End Date</Text>
          <DateTimePicker
            mode="date"
            value={endDate}
            onChange={onEndDateChange}
          />
        </View>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    marginBottom: 24,
  },
  dateField: {
    marginBottom: 16,
  },
}); 