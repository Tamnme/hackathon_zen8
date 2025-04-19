import { ConfigurationSettings } from '@/components/settings/ConfigurationSettings';
import { GeneralSettings } from '@/components/settings/GeneralSettings';
import { useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';

export default function SettingsScreen() {
  const [pushNotifications, setPushNotifications] = useState(true);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <GeneralSettings
          pushNotifications={pushNotifications}
          onPushNotificationsChange={setPushNotifications}
          appearance="System"
        />

        <ConfigurationSettings />

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