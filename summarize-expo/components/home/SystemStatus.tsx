import { StatusIndicator } from '@/components/StatusIndicator';
import { Card } from '@/components/ui/Card';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Text } from '@/components/ui/Text';
import { useAppSelector } from '@/store';
import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';
import { SlackConfigPopup } from './SlackConfigPopup';

interface SystemStatusProps {
  notionStatus: 'success' | 'error' | 'unverified';
  onSlackConfigChange?: (status: 'success' | 'error' | 'unverified') => void;
}

export function SystemStatus({ notionStatus, onSlackConfigChange }: SystemStatusProps) {
  const [showSlackPopup, setShowSlackPopup] = useState(false);
  const { slackConfig } = useAppSelector((state) => state.user);

  console.log('slackConfig', slackConfig);

  const slackStatus: 'success' | 'error' | 'unverified' =
    !slackConfig.token || !slackConfig.email
      ? 'unverified'
      : slackConfig.isVerified
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

  return (
    <View style={styles.section}>
      <Text variant="h2">System Status</Text>
      <Card>
        <TouchableOpacity
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
        <View style={styles.statusRow}>
          <IconSymbol name="doc.text" size={24} color="black" />
          <Text style={styles.statusLabel}>Notion Config</Text>
          <StatusIndicator 
            status={notionStatus} 
            label={getStatusLabel(notionStatus)} 
          />
        </View>
      </Card>

      <SlackConfigPopup
        visible={showSlackPopup}
        onClose={() => setShowSlackPopup(false)}
        onSuccess={handleSlackConfigSuccess}
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