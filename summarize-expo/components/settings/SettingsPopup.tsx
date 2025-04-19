import { settingsApi } from '@/api/settings';
import { slackConfigApi } from '@/api/slack';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Dropdown } from '@/components/ui/Dropdown';
import { MultiSelect } from '@/components/ui/MultiSelect';
import { Text } from '@/components/ui/Text';
import { TextInput } from '@/components/ui/TextInput';
import { useAppDispatch } from '@/store';
import { setChannels as setChannelsAction, setNotionConfig, setSchedulePeriod, setSlackConfig } from '@/store/slices/userSlice';
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Modal, ScrollView, StyleSheet, View } from 'react-native';

interface SettingsPopupProps {
  visible: boolean;
  onClose: () => void;
  onSave: (settings: Settings) => void;
  initialSettings?: Settings;
}

type SchedulePeriod = '2h' | '3h' | '4h' | 'daily' | 'weekly';

export interface Settings {
  email: string;
  schedule_period: SchedulePeriod;
  default_channels: string[];
  slack_token: string;
  notion_secret: string;
  notion_page_id: string;
}

interface FormErrors extends Partial<Record<keyof Settings, string>> {
  general?: string;
}

const SCHEDULE_OPTIONS = ['2h', '3h', '4h', 'daily', 'weekly'] as const;

export function SettingsPopup({ visible, onClose, onSave, initialSettings }: SettingsPopupProps) {
  const dispatch = useAppDispatch();
  const [settings, setSettings] = useState<Settings>({
    email: '',
    schedule_period: 'daily',
    default_channels: [],
    slack_token: '',
    notion_secret: '',
    notion_page_id: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [channels, setChannels] = useState<{ id: string; name: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [verifyingSlack, setVerifyingSlack] = useState(false);
  const [slackVerified, setSlackVerified] = useState(false);
  const [verifyingNotion, setVerifyingNotion] = useState(false);
  const [notionVerified, setNotionVerified] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (initialSettings) {
      setSettings(initialSettings);
    }
  }, [initialSettings]);

  useEffect(() => {
    const verifySlackConfig = async () => {
      if (settings.email && settings.slack_token) {
        setVerifyingSlack(true);
        try {
          const result = await slackConfigApi.verifySlackConfig({
            token: settings.slack_token,
            email: settings.email,
          });
          setSlackVerified(result.success);
          if (!result.success) {
            setErrors(prev => ({
              ...prev,
              slack_token: 'Invalid Slack configuration. Please check your email and token.',
            }));
          } else {
            setErrors(prev => ({
              ...prev,
              slack_token: undefined,
            }));
            const channelsData = await slackConfigApi.getChannels(settings.slack_token);
            setChannels(channelsData);
          }
        } catch (error) {
          setErrors(prev => ({
            ...prev,
            slack_token: 'Failed to verify Slack configuration. Please try again.',
          }));
          setSlackVerified(false);
        } finally {
          setVerifyingSlack(false);
        }
      } else {
        setSlackVerified(false);
      }
    };

    verifySlackConfig();
  }, [settings.email, settings.slack_token]);

  useEffect(() => {
    const verifyNotionConfig = async () => {
      if (settings.notion_secret && settings.notion_page_id) {
        setVerifyingNotion(true);
        try {
          const result = await settingsApi.validateNotionConnection(
            settings.notion_secret,
            settings.notion_page_id
          );
          setNotionVerified(result.success);
          if (!result.success) {
            setErrors(prev => ({
              ...prev,
              notion_secret: 'Invalid Notion configuration. Please check your credentials.',
            }));
          } else {
            setErrors(prev => ({
              ...prev,
              notion_secret: undefined,
              notion_page_id: undefined,
            }));
          }
        } catch (error) {
          setErrors(prev => ({
            ...prev,
            notion_secret: 'Failed to verify Notion configuration. Please try again.',
          }));
          setNotionVerified(false);
        } finally {
          setVerifyingNotion(false);
        }
      } else {
        setNotionVerified(false);
      }
    };

    verifyNotionConfig();
  }, [settings.notion_secret, settings.notion_page_id]);

  const validateFields = () => {
    const newErrors: Partial<Record<keyof Settings, string>> = {};

    if (!settings.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(settings.email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!settings.slack_token) {
      newErrors.slack_token = 'Slack token is required';
    } else if (!slackVerified) {
      newErrors.slack_token = 'Please verify your Slack configuration';
    }

    if (!settings.notion_secret) {
      newErrors.notion_secret = 'Notion secret is required';
    } else if (!notionVerified) {
      newErrors.notion_secret = 'Please verify your Notion configuration';
    }

    if (!settings.notion_page_id) {
      newErrors.notion_page_id = 'Notion page ID is required';
    }

    if (channels.length > 0 && settings.default_channels.length === 0) {
      newErrors.default_channels = 'Please select at least one channel';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (validateFields()) {
      setSaving(true);
      try {
        const apiSettings = {
          ...settings,
          schedule_period: settings.schedule_period === 'daily' || settings.schedule_period === 'weekly'
            ? settings.schedule_period
            : 'daily',
        };
        const result = await settingsApi.updateAppSettings(apiSettings);
        if (result.success) {
          dispatch(setSlackConfig({
            token: settings.slack_token,
            email: settings.email,
            isVerified: true
          }));
          dispatch(setNotionConfig({
            secret: settings.notion_secret,
            pageId: settings.notion_page_id,
            isVerified: true
          }));
          dispatch(setSchedulePeriod(settings.schedule_period));
          dispatch(setChannelsAction(settings.default_channels));

          onSave(settings);
          onClose();
        } else {
          setErrors(prev => ({
            ...prev,
            general: 'Failed to save settings. Please try again.',
          }));
        }
      } catch (error) {
        setErrors(prev => ({
          ...prev,
          general: 'An error occurred while saving settings. Please try again.',
        }));
      } finally {
        setSaving(false);
      }
    }
  };

  const isValid = () => {
    return (
      settings.email &&
      settings.slack_token &&
      slackVerified &&
      settings.notion_secret &&
      settings.notion_page_id &&
      notionVerified &&
      (channels.length === 0 || settings.default_channels.length > 0)
    );
  };

  const renderRequiredLabel = (label: string) => (
    <View style={styles.labelContainer}>
      <Text variant="label">{label}</Text>
      <Text style={styles.requiredStar}>*</Text>
    </View>
  );

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <Card style={styles.modalContent}>
          <ScrollView>
            <Text variant="h2" style={styles.title}>App Settings</Text>

            {errors.general && (
              <Text style={[styles.errorText, styles.generalError]}>{errors.general}</Text>
            )}

            {renderRequiredLabel('Email')}
            <TextInput
              value={settings.email}
              onChangeText={(text) => {
                setSettings(prev => ({ ...prev, email: text }));
                setErrors(prev => ({ ...prev, email: undefined }));
              }}
              placeholder="Enter your email"
              style={[styles.input, errors.email && styles.inputError]}
            />
            {errors.email && <Text style={styles.errorText}>{errors.email}</Text>}

            {renderRequiredLabel('Slack Token')}
            <View style={styles.inputContainer}>
              <TextInput
                value={settings.slack_token}
                onChangeText={(text) => {
                  setSettings(prev => ({ ...prev, slack_token: text }));
                  setErrors(prev => ({ ...prev, slack_token: undefined }));
                }}
                placeholder="Enter Slack token"
                style={[
                  styles.input,
                  styles.inputWithIcon,
                  errors.slack_token && styles.inputError,
                  slackVerified && styles.inputSuccess
                ]}
              />
              {verifyingSlack && (
                <View style={styles.statusContainer}>
                  <ActivityIndicator size="small" color="#666" style={{ marginBottom: 15 }} />
                </View>
              )}
              {!verifyingSlack && slackVerified && (
                <View style={styles.statusContainer}>
                  <Text style={styles.successText}>✓</Text>
                </View>
              )}
            </View>
            {errors.slack_token && <Text style={styles.errorText}>{errors.slack_token}</Text>}

            {channels.length > 0 && (
              <>
                {renderRequiredLabel('Default Channels')}
                <MultiSelect
                  values={settings.default_channels}
                  items={channels.map(channel => ({ label: channel.name, value: channel.name }))}
                  onSelect={(values) => {
                    setSettings(prev => ({ ...prev, default_channels: values }));
                    setErrors(prev => ({ ...prev, default_channels: undefined }));
                  }}
                  placeholder="Select channels"
                  style={[styles.input, errors.default_channels && styles.inputError]}
                />
                {errors.default_channels && <Text style={styles.errorText}>{errors.default_channels}</Text>}
              </>
            )}

            <Text variant="label">Schedule Period</Text>
            <Dropdown
              value={settings.schedule_period}
              items={SCHEDULE_OPTIONS.map(option => ({ label: option, value: option }))}
              onSelect={(value) => setSettings(prev => ({ ...prev, schedule_period: value as SchedulePeriod }))}
              placeholder="Select schedule period"
              style={styles.input}
            />

            {renderRequiredLabel('Notion Secret')}
            <View style={styles.inputContainer}>
              <TextInput
                value={settings.notion_secret}
                onChangeText={(text) => {
                  setSettings(prev => ({ ...prev, notion_secret: text }));
                  setErrors(prev => ({ ...prev, notion_secret: undefined }));
                }}
                placeholder="Enter Notion secret"
                style={[
                  styles.input,
                  styles.inputWithIcon,
                  errors.notion_secret && styles.inputError,
                  notionVerified && styles.inputSuccess
                ]}
              />
              {verifyingNotion && (
                <View style={styles.statusContainer}>
                  <ActivityIndicator size="small" color="#666" style={{ marginBottom: 15 }} />
                </View>
              )}
              {!verifyingNotion && notionVerified && (
                <View style={styles.statusContainer}>
                  <Text style={styles.successText}>✓</Text>
                </View>
              )}
            </View>
            {errors.notion_secret && <Text style={styles.errorText}>{errors.notion_secret}</Text>}

            {renderRequiredLabel('Notion Page ID')}
            <TextInput
              value={settings.notion_page_id}
              onChangeText={(text) => {
                setSettings(prev => ({ ...prev, notion_page_id: text }));
                setErrors(prev => ({ ...prev, notion_page_id: undefined }));
              }}
              placeholder="Enter Notion page ID"
              style={[
                styles.input,
                errors.notion_page_id && styles.inputError
              ]}
            />
            {errors.notion_page_id && <Text style={styles.errorText}>{errors.notion_page_id}</Text>}

            <View style={styles.buttonContainer}>
              <Button
                onPress={handleSave}
                style={styles.button}
                disabled={!isValid() || saving}
              >
                {saving ? 'Saving...' : 'Save'}
              </Button>
            </View>
          </ScrollView>
        </Card>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: '90%',
    maxHeight: '80%',
    padding: 20,
  },
  title: {
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    marginTop: 4,
    marginBottom: 16,
  },
  dropdownContainer: {
    borderWidth: 1,
    borderColor: '#E5E5E5',
    borderRadius: 8,
    marginBottom: 16,
    backgroundColor: '#fff',
  },
  picker: {
    height: 50,
  },
  selectedChannelsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 16,
  },
  selectedChannel: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
    padding: 8,
    borderRadius: 8,
    margin: 4,
  },
  removeChannelButton: {
    marginLeft: 8,
    padding: 4,
  },
  removeChannelText: {
    color: '#FF3B30',
    fontSize: 16,
    fontWeight: 'bold',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 20,
  },
  button: {
    flex: 1,
    marginHorizontal: 8,
  },
  labelContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  requiredStar: {
    color: '#FF3B30',
    marginLeft: 4,
    fontSize: 16,
  },
  inputError: {
    borderColor: '#FF3B30',
  },
  errorText: {
    color: '#FF3B30',
    fontSize: 12,
    marginTop: -12,
    marginBottom: 16,
  },
  inputContainer: {
    position: 'relative',
    width: '100%',
  },
  inputWithIcon: {
    paddingRight: 40,
  },
  statusContainer: {
    position: 'absolute',
    right: 12,
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  inputSuccess: {
    borderColor: '#34C759',
  },
  successText: {
    color: '#34C759',
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  generalError: {
    marginBottom: 16,
    textAlign: 'center',
    fontSize: 14,
  },
});