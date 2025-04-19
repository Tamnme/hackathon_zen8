import { settingsApi } from '@/api/settings';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import { TextInput } from '@/components/ui/TextInput';
import { useAppDispatch, useAppSelector } from '@/store';
import { setLoading, setNotionConfig } from '@/store/slices/userSlice';
import React, { useState } from 'react';
import { Modal, StyleSheet, View } from 'react-native';

interface NotionConfigPopupProps {
  visible: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function NotionConfigPopup({ visible, onClose, onSuccess }: NotionConfigPopupProps) {
  const dispatch = useAppDispatch();
  const { notionConfig, slackConfig, loading } = useAppSelector((state) => state.user);
  const [secret, setSecret] = useState(notionConfig.secret || '');
  const [pageId, setPageId] = useState(notionConfig.pageId || '');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!secret || !pageId) {
      setError('Notion secret and page ID are required');
      return;
    }

    if (!slackConfig.email) {
      setError('Please configure Slack first');
      return;
    }

    dispatch(setLoading(true));
    setError(null);

    try {
      const result = await settingsApi.validateNotionConnection(secret, pageId);
      if (result.success) {
        // Update Notion settings in the backend
        await settingsApi.updateNotionSettings(slackConfig.email, secret, pageId);
        
        dispatch(setNotionConfig({
          secret,
          pageId,
          isVerified: true
        }));
        onSuccess();
        onClose();
      } else {
        setError('Failed to verify Notion configuration');
      }
    } catch (err) {
      setError('An error occurred while verifying Notion configuration');
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <Card style={styles.popup}>
          <Text variant="h2" style={styles.title}>Notion Configuration</Text>

          <TextInput
            label="Notion Secret"
            value={secret}
            onChangeText={setSecret}
            placeholder="Enter your Notion secret"
            style={styles.input}
          />

          <TextInput
            label="Page ID"
            value={pageId}
            onChangeText={setPageId}
            placeholder="Enter your Notion page ID"
            style={styles.input}
          />

          {error && (
            <Text style={styles.error}>{error}</Text>
          )}

          <View style={styles.buttons}>
            <Button
              mode="outlined"
              onPress={onClose}
              style={styles.button}
            >
              Cancel
            </Button>
            <Button
              mode="contained"
              onPress={handleSubmit}
              loading={loading}
              style={styles.button}
            >
              Verify
            </Button>
          </View>
        </Card>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  popup: {
    width: '100%',
    maxWidth: 400,
    padding: 20,
  },
  title: {
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    marginBottom: 16,
  },
  error: {
    color: '#FF3B30',
    marginBottom: 16,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 8,
  },
  button: {
    minWidth: 100,
  },
}); 