import { AboutSection } from '@/components/settings/AboutSection';
import { AdvancedSettings } from '@/components/settings/AdvancedSettings';
import { ConfigurationSettings } from '@/components/settings/ConfigurationSettings';
import { GeneralSettings } from '@/components/settings/GeneralSettings';
import { useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';

export default function SettingsScreen() {
  const [pushNotifications, setPushNotifications] = useState(true);

  // Mock data - would come from app state/context in real implementation
  const configData = {
    schedule: 'Daily at 9:00 AM',
    defaultChannels: ['#general', '#team-updates'],
    notionTarget: 'Team Updates',
    activityCheck: 'Last 24 hours',
  };

  const handleOpenWebApp = () => {
    // Implementation for opening web app
    console.log('Opening web app...');
  };

  const handleSignOut = () => {
    // Implementation for sign out
    console.log('Signing out...');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <GeneralSettings
          pushNotifications={pushNotifications}
          onPushNotificationsChange={setPushNotifications}
          appearance="System"
        />

        <ConfigurationSettings
          schedule={configData.schedule}
          defaultChannels={configData.defaultChannels}
          notionTarget={configData.notionTarget}
          activityCheck={configData.activityCheck}
        />

        <AdvancedSettings onOpenWebApp={handleOpenWebApp} />

        <AboutSection
          version="1.0.0"
          onSignOut={handleSignOut}
        />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F8F8',
  },
  content: {
    padding: 16,
  },
});