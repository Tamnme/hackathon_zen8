import React from 'react';
import { FlatList, StyleSheet } from 'react-native';
import { SummaryCard } from './SummaryCard';
import { SummaryRun } from './types';

interface HistoryListProps {
  data: SummaryRun[];
  onViewNotionPage: (notionUrl: string) => void;
}

export function HistoryList({ data, onViewNotionPage }: HistoryListProps) {
  const renderItem = ({ item }: { item: SummaryRun }) => (
    <SummaryCard
      id={item.id}
      date={item.date}
      status={item.status}
      channels={item.channels}
      onViewNotionPage={() => onViewNotionPage(item.notionUrl)}
    />
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={item => item.id}
      contentContainerStyle={styles.list}
      showsVerticalScrollIndicator={false}
    />
  );
}

const styles = StyleSheet.create({
  list: {
    gap: 16,
  },
}); 