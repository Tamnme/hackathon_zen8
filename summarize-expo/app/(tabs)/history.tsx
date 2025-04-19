import { HistoryList } from '@/components/history/HistoryList';
import { Text } from '@/components/ui/Text';
import React from 'react';
import { Linking, ScrollView, StyleSheet, View } from 'react-native';

export default function HistoryScreen() {
  const handleViewNotionPage = (notionUrl: string) => {
    Linking.openURL(notionUrl);
  };

  return (
    <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
      <View style={styles.container}>
        <View style={styles.header}>
          <Text variant="h1">History</Text>
          <Text variant="subtitle" style={{ marginTop: 8 }}>Past summary runs</Text>
        </View>

        <HistoryList
          onViewNotionPage={handleViewNotionPage}
        />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollView: {
    flex: 1,
    backgroundColor: '#fff',
  },
  scrollContent: {
    flexGrow: 1,
  },
  container: {
    flex: 1,
    padding: 16,
  },
  header: {
    marginBottom: 24,
  },
});