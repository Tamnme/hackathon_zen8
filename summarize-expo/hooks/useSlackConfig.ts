import { slackConfigApi } from '@/api/slack';
import { useAppDispatch, useAppSelector } from '@/store';
import { setError, setLoading, setSlackConfig } from '@/store/slices/userSlice';
import { useEffect } from 'react';

type SlackStatus = 'success' | 'error' | 'unverified';

export function useSlackConfig() {
  const dispatch = useAppDispatch();
  const { slackConfig, loading } = useAppSelector((state) => state.user);

  useEffect(() => {
    const verifyStoredCredentials = async () => {
      if (!slackConfig.token || !slackConfig.email) {
        return;
      }

      try {
        dispatch(setLoading(true));
        const result = await slackConfigApi.verifySlackConfig({
          token: slackConfig.token,
          email: slackConfig.email,
        });

        dispatch(setSlackConfig({
          ...slackConfig,
          isVerified: result ? true : false
        }));
      } catch (error) {
        dispatch(setError('Failed to verify Slack configuration'));
      } finally {
        dispatch(setLoading(false));
      }
    };

    verifyStoredCredentials();
  }, [slackConfig.token, slackConfig.email]);

  const status: SlackStatus = !slackConfig.token || !slackConfig.email
    ? 'unverified'
    : slackConfig.isVerified
      ? 'success'
      : 'error';

  return { status, loading };
}