import { userApi } from '@/api/user';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Text } from '@/components/ui/Text';
import { TextInput } from '@/components/ui/TextInput';
import { useAppDispatch, useAppSelector } from '@/store';
import { setLoading, setSlackConfig } from '@/store/slices/userSlice';
import React, { useState } from 'react';
import { Modal, StyleSheet, View } from 'react-native';

interface SlackConfigPopupProps {
  visible: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function SlackConfigPopup({ visible, onClose, onSuccess }: SlackConfigPopupProps) {
  const dispatch = useAppDispatch();
  const { slackConfig, loading } = useAppSelector((state) => state.user);
  const [token, setToken] = useState(slackConfig.token || '');
  const [email, setEmail] = useState(slackConfig.email || '');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!token) {
      setError('Slack token is required');
      return;
    }

    dispatch(setLoading(true));
    setError(null);

    try {
      const result = await userApi.verifySlackConfig({ token, email });
      if (result) {
        dispatch(setSlackConfig({
          token,
          email,
          isVerified: true
        }));
        onSuccess();
        onClose();
      } else {
        setError('Failed to verify Slack configuration');
      }
    } catch (err) {
      setError('An error occurred while verifying Slack configuration');
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
          <Text variant="h2" style={styles.title}>Slack Configuration</Text>

          <TextInput
            label="Slack Token"
            value={token}
            onChangeText={setToken}
            placeholder="Enter your Slack token"
            style={styles.input}
          />

          <TextInput
            label="Email"
            value={email}
            onChangeText={setEmail}
            placeholder="Enter your email"
            keyboardType="email-address"
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