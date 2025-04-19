import { summaryApi } from '@/api/summary';
import { Button } from '@/components/ui/Button';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Text } from '@/components/ui/Text';
import { useAppSelector } from '@/store';
import React, { useCallback, useEffect, useState } from 'react';
import { ActivityIndicator, FlatList, RefreshControl, StyleSheet, View } from 'react-native';
import { SummaryCard } from './SummaryCard';
import { SummaryRun } from './types';

interface HistoryListProps {
  onViewNotionPage: (notionUrl: string) => void;
}

export function HistoryList({ onViewNotionPage }: HistoryListProps) {
  const { slackConfig } = useAppSelector((state) => state.user);
  const [data, setData] = useState<SummaryRun[]>([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const transformSummaryToRun = (summary: any): SummaryRun => ({
    id: summary.id.toString(),
    date: summary.start_time,
    status: summary.status === 'completed' ? 'success' : 'error',
    channels: summary.channels,
    notionUrl: summary.notion_page_url,
  });

  const fetchData = useCallback(async (pageNum: number, isRefreshing: boolean = false) => {
    if (!slackConfig.email) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await summaryApi.getSummaryHistories(slackConfig.email, 10, pageNum);

      const transformedData = response.histories.map(transformSummaryToRun);

      if (isRefreshing) {
        setData(transformedData);
      } else {
        setData(prev => [...prev, ...transformedData]);
      }

      setHasMore(pageNum < response.total);
    } catch (err) {
      setError('Failed to fetch history');
      console.error('Error fetching history:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [slackConfig.email]);

  useEffect(() => {
    fetchData(1);
  }, [fetchData]);

  const handleRefresh = useCallback(() => {
    setRefreshing(true);
    setPage(1);
    fetchData(1, true);
  }, [fetchData]);

  const handleLoadMore = useCallback(() => {
    if (!loading && hasMore && data.length > 0) {
      const nextPage = page + 1;
      setPage(nextPage);
      fetchData(nextPage);
    }
  }, [loading, hasMore, page, fetchData, data.length]);

  const renderItem = ({ item }: { item: SummaryRun }) => (
    <SummaryCard
      id={item.id}
      date={item.date}
      status={item.status}
      channels={item.channels}
      onViewNotionPage={() => onViewNotionPage(item.notionUrl)}
    />
  );

  const renderFooter = () => {
    if (!loading) return null;
    return (
      <View style={styles.footer}>
        <ActivityIndicator size="small" color="#000" />
      </View>
    );
  };

  const renderEmpty = () => {
    if (loading) return null;
    if (error) {
      return (
        <View style={styles.emptyContainer}>
          <IconSymbol name="exclamationmark.triangle" size={48} color="#FF3B30" />
          <Text variant="h2" style={styles.emptyTitle}>Error</Text>
          <Text style={styles.emptyDescription}>{error}</Text>
          <Button
            onPress={handleRefresh}
            style={styles.retryButton}
            mode="contained"
          >
            Try Again
          </Button>
        </View>
      );
    }

    return (
      <View style={styles.emptyContainer}>
        <IconSymbol name="doc.text" size={48} color="#E5E5E5" />
        <Text variant="h2" style={styles.emptyTitle}>No History Yet</Text>
        <Text style={styles.emptyDescription}>
          Your summary history will appear here after runs are completed
        </Text>
        <Button
          onPress={handleRefresh}
          style={styles.retryButton}
          mode="outlined"
        >
          Refresh
        </Button>
      </View>
    );
  };

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={item => item.id}
      contentContainerStyle={styles.list}
      showsVerticalScrollIndicator={false}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={handleRefresh}
        />
      }
      onEndReached={handleLoadMore}
      onEndReachedThreshold={0.5}
      ListFooterComponent={renderFooter}
      ListEmptyComponent={renderEmpty}
    />
  );
}

const styles = StyleSheet.create({
  list: {
    gap: 16,
  },
  footer: {
    paddingVertical: 20,
    alignItems: 'center',
  },
  emptyContainer: {
    padding: 32,
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyTitle: {
    marginTop: 16,
    marginBottom: 8,
    textAlign: 'center',
  },
  emptyDescription: {
    color: '#666',
    textAlign: 'center',
  },
  retryButton: {
    marginTop: 20,
    minWidth: 120,
    borderRadius: 20,
  },
}); 