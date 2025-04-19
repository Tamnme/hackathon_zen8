import { Card } from '@/components/ui/Card';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { StyleSheet, View } from 'react-native';

interface NotionTargetSelectorProps {
  targetPage: string;
}

export function NotionTargetSelector({ targetPage }: NotionTargetSelectorProps) {
  return (
    <View style={styles.section}>
      <Text variant="h2">Notion Target</Text>
      <Card>
        <Text variant="label">Send Summary To</Text>
        <View style={styles.notionTarget}>
          <IconSymbol name="doc.text" size={24} color="#000" />
          <Text style={styles.notionPage}>{targetPage}</Text>
        </View>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    marginBottom: 24,
  },
  notionTarget: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  notionPage: {
    marginLeft: 12,
  },
}); 