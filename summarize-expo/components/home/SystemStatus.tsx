import { StatusIndicator } from '@/components/StatusIndicator';
import { Card } from '@/components/ui/Card';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Text } from '@/components/ui/Text';
import { useAppSelector } from '@/store';
import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';
import { NotionConfigPopup } from './NotionConfigPopup';
import { SlackConfigPopup } from './SlackConfigPopup';

interface SystemStatusProps {
  onSlackConfigChange?: (status: 'success' | 'error' | 'unverified') => void;
  onNotionConfigChange?: (status: 'success' | 'error' | 'unverified') => void;
}

export function SystemStatus({ onSlackConfigChange, onNotionConfigChange }: SystemStatusProps) {
  const [showSlackPopup, setShowSlackPopup] = useState(false);
  const [showNotionPopup, setShowNotionPopup] = useState(false);
  const { slackConfig, notionConfig } = useAppSelector((state) => state.user);

  const slackStatus: 'success' | 'error' | 'unverified' =
    !slackConfig.token || !slackConfig.email
      ? 'unverified'
      : slackConfig.isVerified
        ? 'success'
        : 'error';

  const notionStatus: 'success' | 'error' | 'unverified' =
    !notionConfig.secret || !notionConfig.pageId
      ? 'unverified'
      : notionConfig.isVerified
        ? 'success'
        : 'error';

  const getStatusLabel = (status: 'success' | 'error' | 'unverified') => {
    switch (status) {
      case 'success':
        return 'Connected';
      case 'error':
        return 'Not Connected';
      case 'unverified':
        return 'Not Configured';
      default:
        return 'Unknown';
    }
  };

  const handleSlackConfigSuccess = () => {
    onSlackConfigChange?.('success');
  };

  const handleNotionConfigSuccess = () => {
    onNotionConfigChange?.('success');
  };

  return (
    <View style={styles.section}>
      <Text variant="h2">System Status</Text>
      <Card>
        <TouchableOpacity
          disabled
          style={styles.statusRow}
          onPress={() => setShowSlackPopup(true)}
        >
          <IconSymbol name="slash.circle" size={24} color="black" />
          <Text style={styles.statusLabel}>Slack Config</Text>
          <StatusIndicator 
            status={slackStatus} 
            label={getStatusLabel(slackStatus)} 
          />
        </TouchableOpacity>
        <TouchableOpacity
          disabled
          style={styles.statusRow}
          onPress={() => setShowNotionPopup(true)}
        >
          <IconSymbol name="doc.text" size={24} color="black" />
          <Text style={styles.statusLabel}>Notion Config</Text>
          <StatusIndicator 
            status={notionStatus} 
            label={getStatusLabel(notionStatus)} 
          />
        </TouchableOpacity>
      </Card>

      <SlackConfigPopup
        visible={showSlackPopup}
        onClose={() => setShowSlackPopup(false)}
        onSuccess={handleSlackConfigSuccess}
      />

      <NotionConfigPopup
        visible={showNotionPopup}
        onClose={() => setShowNotionPopup(false)}
        onSuccess={handleNotionConfigSuccess}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    marginBottom: 24,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#E5E5E5',
  },
  statusLabel: {
    flex: 1,
    marginLeft: 12,
  },
});