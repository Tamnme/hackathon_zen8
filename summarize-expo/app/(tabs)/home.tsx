import { LastRun } from '@/components/home/LastRun';
import { QuickActions } from '@/components/home/QuickActions';
import { SystemStatus } from '@/components/home/SystemStatus';
import { Settings, SettingsPopup } from '@/components/settings/SettingsPopup';
import { Text } from '@/components/ui/Text';
import * as SecureStore from 'expo-secure-store';
import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';

const FIRST_TIME_KEY = 'first_time_app_open';

export default function HomeScreen() {
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState<Settings>({
    email: '',
    schedule_period: 'daily',
    default_channels: [],
    slack_token: '',
    notion_secret: '',
    notion_page_id: '',
  });

  useEffect(() => {
    checkFirstTimeOpen();
  }, []);

  const checkFirstTimeOpen = async () => {
    try {
      const firstTime = await SecureStore.getItemAsync(FIRST_TIME_KEY);
      console.log('firstTime', firstTime);
      if (firstTime === null) {
        setShowSettings(true);
        await SecureStore.setItemAsync(FIRST_TIME_KEY, 'false');
      }
    } catch (error) {
      setShowSettings(true);
      console.error('Error checking first time open:', error);
    }
  };

  const handleSaveSettings = async (newSettings: Settings) => {
    setSettings(newSettings);
    // Here you can also save settings to SecureStore or your backend
    try {
      await SecureStore.setItemAsync('app_settings', JSON.stringify(newSettings));
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  };

  return (
    <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
      <View style={styles.container}>
        <View style={styles.header}>
          <Text variant="h1">Dashboard</Text>
        </View>

        <LastRun />

        <QuickActions
          onSummarizeNow={() => {
            // Handle summarize now
          }}
        />

        <SystemStatus
          onSlackConfigChange={(status) => {
            // Handle Slack config change if needed
            console.log('Slack config status changed:', status);
          }}
          onNotionConfigChange={(status) => {
            // Handle Notion config change if needed
            console.log('Notion config status changed:', status);
          }}
        />

        <SettingsPopup
          visible={showSettings}
          onClose={() => setShowSettings(false)}
          onSave={handleSaveSettings}
          initialSettings={settings}
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
});
