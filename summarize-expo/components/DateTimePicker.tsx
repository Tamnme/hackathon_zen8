import RNDateTimePicker from '@react-native-community/datetimepicker';
import React, { useState } from 'react';
import { Platform, StyleSheet, TouchableOpacity } from 'react-native';
import { Text } from './ui/Text';

interface DateTimePickerProps {
  mode?: 'date' | 'time';
  value?: Date;
  onChange?: (date: Date | undefined) => void;
}

export default function DateTimePicker({
  mode = 'date',
  value = new Date(),
  onChange,
}: DateTimePickerProps) {
  const [show, setShow] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(value);

  const handleChange = (event: any, date?: Date) => {
    setShow(Platform.OS === 'ios');
    if (date) {
      setSelectedDate(date);
      onChange?.(date);
    }
  };

  const formatDate = (date?: Date) => {
    if (!date) return 'Pick a date';
    return date.toLocaleDateString();
  };

  return (
    <>
      <TouchableOpacity
        style={styles.button}
        onPress={() => setShow(true)}
      >
        <Text>{formatDate(selectedDate)}</Text>
      </TouchableOpacity>

      {show && (
        <RNDateTimePicker
          value={selectedDate || new Date()}
          mode={mode}
          onChange={handleChange}
        />
      )}
    </>
  );
}

const styles = StyleSheet.create({
  button: {
    borderWidth: 1,
    borderColor: '#E5E5E5',
    borderRadius: 8,
    padding: 12,
    marginTop: 8,
  },
});