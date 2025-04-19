import React from 'react';
import { Text as RNText, TextProps as RNTextProps, StyleSheet } from 'react-native';

interface TextProps extends RNTextProps {
  variant?: 'h1' | 'h2' | 'subtitle' | 'body' | 'label';
}

export function Text({ variant = 'body', style, ...props }: TextProps) {
  return (
    <RNText style={[styles[variant], style]} {...props} />
  );
}

const styles = StyleSheet.create({
  h1: {
    fontSize: 34,
    fontWeight: 'bold',
    color: '#000',
  },
  h2: {
    fontSize: 20,
    fontWeight: '600',
    color: '#000',
  },
  subtitle: {
    fontSize: 17,
    color: '#666',
  },
  body: {
    fontSize: 17,
    color: '#000',
  },
  label: {
    fontSize: 15,
    color: '#666',
  },
}); 