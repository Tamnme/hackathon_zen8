import React from 'react';
import { ActivityIndicator, StyleSheet, TouchableOpacity, TouchableOpacityProps } from 'react-native';
import { Text } from './Text';

interface ButtonProps extends TouchableOpacityProps {
  mode?: 'contained' | 'outlined' | 'text';
  textColor?: string;
  loading?: boolean;
  children: React.ReactNode;
}

export function Button({ 
  mode = 'contained',
  style,
  textColor,
  loading = false,
  disabled,
  children,
  ...props 
}: ButtonProps) {
  const buttonStyle = [
    styles.button,
    mode === 'contained' && styles.contained,
    mode === 'outlined' && styles.outlined,
    mode === 'text' && styles.text,
    disabled && styles.disabled,
    style,
  ];

  const textStyle = [
    styles.text,
    mode === 'contained' && styles.containedText,
    mode === 'outlined' && styles.outlinedText,
    mode === 'text' && styles.textText,
    textColor && { color: textColor },
  ];

  return (
    <TouchableOpacity
      style={buttonStyle}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <ActivityIndicator color={mode === 'contained' ? '#fff' : '#000'} />
      ) : (
        <Text style={textStyle}>{children}</Text>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  contained: {
    backgroundColor: '#000',
  },
  outlined: {
    borderWidth: 1,
    borderColor: '#000',
  },
  text: {
    backgroundColor: 'transparent',
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    fontSize: 16,
    fontWeight: '600',
  },
  containedText: {
    color: '#fff',
  },
  outlinedText: {
    color: '#000',
  },
  textText: {
    color: '#000',
  },
}); 