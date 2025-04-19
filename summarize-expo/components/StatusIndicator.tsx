import React from 'react';
import { StyleSheet, View } from 'react-native';
import { Text } from './ui/Text';

interface StatusIndicatorProps {
  status: 'online' | 'offline' | 'success' | 'error';
  label?: string;
}

export function StatusIndicator({ status, label }: StatusIndicatorProps) {
  const getStatusColor = () => {
    switch (status) {
      case 'online':
      case 'success':
        return '#34C759';
      case 'offline':
      case 'error':
        return '#FF3B30';
      default:
        return '#999';
    }
  };

  return (
    <View style={styles.container}>
      <View style={[styles.dot, { backgroundColor: getStatusColor() }]} />
      {label && (
        <Text style={styles.label}>{label}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F2F2F7',
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 16,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  label: {
    marginLeft: 6,
    fontSize: 13,
  },
});