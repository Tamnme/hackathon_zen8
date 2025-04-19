import React from 'react';
import { TextInput as RNTextInput, TextInputProps as RNTextInputProps, StyleSheet, View } from 'react-native';
import { Text } from './Text';

interface TextInputProps extends RNTextInputProps {
  label?: string;
}

export function TextInput({ label, style, ...props }: TextInputProps) {
  return (
    <View style={styles.container}>
      {label && <Text variant="label" style={styles.label}>{label}</Text>}
      <RNTextInput
        style={[styles.input, style]}
        placeholderTextColor="#999"
        {...props}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 8,
  },
  label: {
    marginBottom: 4,
  },
  input: {
    borderWidth: 1,
    borderColor: '#E5E5E5',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#fff',
  },
});